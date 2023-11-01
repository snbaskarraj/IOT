class Queue1:
    def __init__(self):
        self.data_list = list() # HAS-A

    def enque(self, new_data):
        self.data_list.insert(0, new_data)

    def dequeue(self):
        return self.data_list.pop()

class Queue2(list): # IS-A
    def __init__(self):
        super().__init__()

    def enque(self, new_data):
        self.insert(0, new_data)

    def dequeue(self):
        return self.pop()
