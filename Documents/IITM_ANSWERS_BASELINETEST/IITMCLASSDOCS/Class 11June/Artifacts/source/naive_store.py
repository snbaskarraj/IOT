# Simple key-value store with multiple replicas storing the same data
class DataStore:
    def __init__(self, kv_dict):
        self._kv_dict = kv_dict

    @property
    def kv_dict(self):
        return self._kv_dict

    def get_data(self, key):
        return self.kv_dict.get(key)

    def set_data(self, key, value):
        self.kv_dict[key] = value

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
    def receive_event(self, key, value):
        self.set_data(key, value)