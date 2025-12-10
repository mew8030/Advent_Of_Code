
class Ingredient_Inventory:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__db = []
        self.__fresh_dates = []
        self.__freshed = []
        self.__spoiled = []
        self.__ingredients = []
        from logger import Logger
        self.log = Logger(True)
        self.analyze_database()

    def analyze_range(self, data):
        self.log.log_debug(0, f"analyzing range ({data})")
        x, y = (data.split('-'))
        self.__fresh_dates.append((int(x), int(y)))
    
    def analyze_ingredients(self, data):
        self.log.log_debug(0, f"analyzing ingredients({data})")
        self.__ingredients.append(data)

    
    def analyze_database(self):
        self.log.log_event(f"analyzing the food database")
        with open(self.__file_path) as f:
            db = f.read()
        self.log.log_debug(1, f"{db}")
        self.log.log_debug(1, f"breaking up database")
        for data in db.split('\n'):
            if '-' in data:
                self.analyze_range(data)
            elif data.isdigit():
                self.analyze_ingredients(int(data))
            else:
                continue
        self.log.log_debug(1, f"the ranges are {self.__fresh_dates}")
        self.log.log_debug(1, f"the ingredients to be sorted are {self.__ingredients}")

    def isfresh(self, ingredient):
        self.log.log_debug(1, f"checking ingredient id {ingredient} for freshness")
        flag = False
        for i1, i2 in self.__fresh_dates:
            self.log.log_debug(0, f"{ingredient} in range ({i1} - {i2})?")
            if ingredient in range(i1, i2 + 1):
                self.log.log_debug(0, f"yes")
                flag = True
        return flag


    def sort_the_spoils(self):
        for ingredient in self.__ingredients:
            if self.isfresh(ingredient):
                self.log.log_debug(1, f"{ingredient} is fresh")
                self.__freshed.append(ingredient)
            else:
                self.log.log_debug(1, f"{ingredient} is spoiled")
                self.__spoiled.append(ingredient)

    def how_many_fresh_ingredients_in_database(self):
        return len(self.__freshed)
