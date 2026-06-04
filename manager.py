class QuestLogManager:
    def __init__(self, quests, inventory, report_file):
        self.quests = quests
        self.inventory = inventory
        self.report_file = report_file
    def quest_list(self):
        for i, q in enumerate(self.quests, 1):           
            print(f"{i}. {q.name}")
    def quest_view(self, name):
        for q in self.quests:
            if q.name == name:
                print(f"Quest: {q.name}")
                print("Required Items:")
                for item, qty in q.items.items():
                    print(f"- {item}: {qty}")
                return
        print("Quest not found")
    def quest_gap(self, name):
        for q in self.quests:
            if q.name == name:
                print(f"Missing items for '{name}':")
                for item, qty in q.items.items():
                    have = self.inventory.items.get(item, 0)
                    if have < qty:
                        print(f"- {item}: {qty - have}")
                return
        print("Quest not found")
    def plan(self):
        print("Completable Quests:")
        for q in self.quests:
            ok = True
            for item, qty in q.items.items():
                if self.inventory.items.get(item, 0) < qty:
                    ok = False
            if ok:
                print(f"- {q.name}")
    def quest_complete(self, name):
        for q in self.quests:
            if q.name == name:
                for item, qty in q.items.items():
                    if self.inventory.items.get(item, 0) < qty:
                        print("Not enough items")
                        return

                for item, qty in q.items.items():
                    self.inventory.items[item] -= qty

                self.inventory.save()
                print(f"Completed '{name}'")
                return

        print("Quest not found")
    def process(self, filepath):
        with open(filepath) as f, open(self.report_file, "w") as report:
            for line in f:
                parts = line.strip().split()

                try:
                    cmd = parts[0]

                    if cmd == "ADD":
                        item = parts[1]
                        qty = int(parts[2])
                        self.inventory.add(item, qty)
                        report.write(f"SUCCESS: {line}")

                    elif cmd == "USE":
                        item = parts[1]
                        qty = int(parts[2])
                        self.inventory.use(item, qty)
                        report.write(f"SUCCESS: {line}")

                    else:
                        report.write(f"ERROR: Unknown command '{cmd}'\n")

                except Exception as e:
                    report.write(f"ERROR: {str(e)}\n")

        print("Batch processing complete")