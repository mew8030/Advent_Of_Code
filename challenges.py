from safe import Safe
from invalid_ids import Invalid_ids
from power_banks import Power_Banks
CONFIG_FILE = "config.txt"

class Challenges:
    def __init__(self, flags):
        self.__flags = flags
        self.__challenges = {
            1: ("Locked Safe", self.locked_safe),
            2: ("Invalid IDs", self.invalid_ids),
            3: ("Battery Banks", self.battery_banks)
        }

    def show_menu(self):
        print(f"\n====Advent-of-Code====")
        for num, (name, _) in self.__challenges.items():
            print(f"  {num}: {name}")
        
        print("  0: Exit\n")

    def run(self, choice):
        try:
            if choice in self.__challenges:
                self.__challenges[choice][1]()
            else:
                raise Exception(f"{choice} is not a valid choice, please try again")
        except Exception as e:
            print(f"ERROR: {e}")

    def start(self):
        while True:
            self.show_menu()
            try:
                choice = int(input("Enter choice: "))
                if choice == 0:
                    print("Goodby!")
                    break
                self.run(choice)
            except ValueError:
                print("Please enter a number")

    #configuration for challenges
    def save_config(self, config):
        with open(CONFIG_FILE, "w") as f:
            for key, value in config.items():
                f.write(f"{key}={value}\n")

    def get_input_path(self, key):
        config = self.load_config()

        if key in config:
            print(f"Saved path: {config[key]}")
            use_saved = input("Use saved path? (y/n): ")
            if use_saved.lower() == "y":
                return config[key]

        new_path = input("Enter file path: ")
        config[key] = new_path
        self.save_config(config)
        return new_path
    
    #day 1 challenge
    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = {}
                for line in f:
                    key, value = line.strip().split("=")
                    config[key] = value
                return config
        except FileNotFoundError:
            print(f"file not found")
            return {}

    #day 2 challenge part 1
    def locked_safe(self):
        try:
            path = self.get_input_path("day1_path")
            lock = Safe(path)
            lock.unlock()
        except Exception as e:
            print(f"ERROR: {e}")
    #day 2 challenge part 2 final
    def invalid_ids(self):
        try:
            path = self.get_input_path("day2_path")
            identifiers = Invalid_ids(path)
            identifiers.find_invalid_ids()
        except Exception as e:
            print(f"ERROR: {e}")

    #day 3 challenge
    def battery_banks(self):
        try:
            print("starting battery challenge")
            path = self.get_input_path("day3_path")
            battery_pack = Power_Banks(path, 2)
            print("battery pack creation competed")
            battery_pack.get_batteries()
            battery_pack.get_voltages()
        except Exception as e:
            print(f"ERROR: {e}")