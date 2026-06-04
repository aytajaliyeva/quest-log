import sys
import json
from questlog.quest import Quest
from questlog.inventory import Inventory
from questlog.manager import QuestLogManager


def load_data():
    with open("config.json") as f:
        config = json.load(f)

    with open(config["quest_file"]) as f:
        quests_data = json.load(f)

    with open(config["inventory_file"]) as f:
        inventory_data = json.load(f)

    quests = [Quest(q["name"], q["items"]) for q in quests_data]
    inventory = Inventory(inventory_data, config["inventory_file"])

    return QuestLogManager(quests, inventory, config["report_file"])


def main():
    manager = load_data()

    if len(sys.argv) > 1 and sys.argv[1] == "manage":
        while True:
            command = input("> ").strip()

            if command == "exit":
                print("Goodbye")
                break

            parts = command.split()

            if parts[0] == "quest":
                if parts[1] == "list":
                    manager.quest_list()
                elif parts[1] == "view":
                    manager.quest_view(" ".join(parts[2:]).strip('"'))
                elif parts[1] == "gap":
                    manager.quest_gap(" ".join(parts[2:]).strip('"'))
                elif parts[1] == "complete":
                    manager.quest_complete(" ".join(parts[2:]).strip('"'))

            elif parts[0] == "inventory":
                if parts[1] == "add":
                    manager.inventory.add(parts[2], int(parts[3]))
                elif parts[1] == "use":
                    manager.inventory.use(parts[2], int(parts[3]))
                elif parts[1] == "process":
                    manager.process(parts[2])

            elif parts[0] == "plan":
                manager.plan()

    else:
        print("Run with 'manage'")


if __name__ == "__main__":
    main()