import json

class Inventory:
    def __init__(self, items, filepath):
        self.items = items
        self.filepath = filepath

    def add(self, item, qty):
        if item in self.items:
            self.items[item] += qty
        else:
            self.items[item] = qty
        self.save()

    def use(self, item, qty):
        if item not in self.items or self.items[item] < qty:
            raise ValueError("Not enough items")
        self.items[item] -= qty
        self.save()

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.items, f, indent=2)