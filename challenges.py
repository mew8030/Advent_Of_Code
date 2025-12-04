from safe import Safe

CONFIG_FILE = "config.txt"

class Challenges:
    def __init__(self, flags):
        self.__flags = flags
        self.__challenges = {
            1: ("Locked Safe", self.locked_safe),
            2: ("Invalid IDs", self.invalid_ids)
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
    
    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = {}
                for line in f:
                    key, value = line.strip().split("=")
                    config[key] = value
                return config
        except FileNotFoundError:
            return {}


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

    def locked_safe(self):
        try:
            path = self.get_input_path("day1_path")
            lock = Safe(path)
            lock.unlock()
        except Exception as e:
            print(f"ERROR: {e}")

    def invalid_ids(self):
        pass