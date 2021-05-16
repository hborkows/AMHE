class Demand:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.paths = []

    def __str__(self):
        return "ID: %s:, Capacity: %s, Admissable paths: %s" % (self.id, self.capacity, self.paths)

    def add_path(self, path):
        self.paths.append(path)
