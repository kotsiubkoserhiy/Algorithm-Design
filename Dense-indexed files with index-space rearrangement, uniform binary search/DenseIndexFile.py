import os
from bisect import bisect_left

class DenseIndexFile:
    def __init__(self, filename):
        self.filename = filename
        self.index = []
        if os.path.exists(filename):
            self.load()

    def load(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                key, _ = line.strip().split(',', 1)
                self.index.append(int(key))

    def add(self, key, data):
        if key in self.index:
            raise ValueError("Key already exists")
        with open(self.filename, 'a') as file:
            file.write(f"{key},{data}\n")
        self.index.append(key)
        self.index.sort()

    def search(self, key):
        position = bisect_left(self.index, key)
        if position == len(self.index) or self.index[position] != key:
            return None
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                k, data = line.strip().split(',', 1)
                if int(k) == key:
                    return data
        return None

    def delete(self, key):
        if key not in self.index:
            return
        lines = []
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        with open(self.filename, 'w') as file:
            for line in lines:
                k, _ = line.strip().split(',', 1)
                if int(k) != key:
                    file.write(line)
        self.index.remove(key)

    def edit(self, key, new_data):
        self.delete(key)
        self.add(key, new_data)