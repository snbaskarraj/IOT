# Simple key-value store with multiple replicas storing the same data
from termcolor import colored


class VectorClockDataStore:
    def __init__(self, kv_dict, name):
        self._kv_dict = kv_dict
        self._name = name
        self._replica_list = []
        self._vector_clock = {name: 0}

    @property
    def kv_dict(self):
        return self._kv_dict

    @property
    def name(self):
        return self._name

    @property
    def vector_clock(self):
        return self._vector_clock

    # Add replicas based on addition of new nodes
    # This will also update the vector clock dict
    def add_replicas(self, replica_list):
        self._replica_list.extend(replica_list)
        for replica in replica_list:
            self._vector_clock[replica.name] = 0

    def reset_vector_clock(self):
        for replica in self._replica_list:
            self._vector_clock[replica.name] = 0
        self._vector_clock[self.name] = 0

    def get_data(self, key):
        return self.kv_dict.get(key)

    def set_data(self, key, value):
        self.kv_dict[key] = value
        self._vector_clock[self.name] += 1

    # Simple add operation on a particular key's value
    def add(self, key, value):
        if self.get_data(key):
            self.set_data(key, self.get_data(key) + value)
        else:
            self.set_data(key, value)

    # Simple multiply operation on a particular key's value
    def multiply(self, key, value):
        if self.get_data(key):
            self.set_data(key, self.get_data(key) * value)
        else:
            self.set_data(key, 0)

    # Event receiver from another replica to update value based on a change done on the caller
    # Normally, this would be called internally from the update on the other store
    def receive_event(self, key, value, caller_vector_clock):
        # compare clocks
        self_clock_ahead = True
        caller_clock_ahead = True
        for node in self.vector_clock:
            if (self.vector_clock[node] < caller_vector_clock[node]):
                self_clock_ahead = False

            if (caller_vector_clock[node] < self.vector_clock[node]):
                caller_clock_ahead = False

        if (self_clock_ahead == False and caller_clock_ahead == False):
            # doSomething(seekConfigPreference)
            print(
                colored(f'No clock is strictly coming later than others - CONCURRENT WRITES DETECTED for key {key} and values {value} and {self.get_data(key)} in receive_event of self.name', 'red'))

        self.set_data(key, value)
        for replica in self._replica_list:
            self.vector_clock[replica.name] = max(self.vector_clock[replica.name], caller_vector_clock[replica.name])