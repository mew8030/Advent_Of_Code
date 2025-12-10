import copy
import textwrap

class Ingredient_Inventory:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__combined_rates = []
        self.__fresh_dates = []
        self.__freshed = []
        self.__spoiled = []
        self.__ingredients = []
        self.__flag_combined = False
        self.__pst_len = 0
        self.__available_ids = 0
        self.__it = 0
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
        self.log.log_debug(0, f"{db}")
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
        self.log.log_debug(0, f"checking ingredient id {ingredient} for freshness")
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
                self.log.log_debug(0, f"{ingredient} is fresh")
                self.__freshed.append(ingredient)
            else:
                self.log.log_debug(0, f"{ingredient} is spoiled")
                self.__spoiled.append(ingredient)

    def how_many_fresh_ingredients_in_database(self):
        return len(self.__freshed)

    def add_to_combined(self, i1, i2):
        if not (i1, i2) in self.__combined_rates:
            self.__combined_rates.append((i1, i2))
        else:
            self.log.log_debug(1, f"nrange {(i1, i2)} already exists")
    
    def check_combinations(self, nrange, ohrange = None):
        n1, n2 = nrange
        if ohrange == None:
            self.log.log_debug(0, f"other range is empty, using self.__combined_rates")
            if len(self.__combined_rates) == 0:
                self.log.log_debug(0, f"self.__combined_rates is also empty")
                return False
            self.log.log_debug(0, f"checking if nrange {nrange} can be attached or combined to self.__combined_rates")
            for combo in self.__combined_rates:
                if nrange == combo:
                    self.log.log_debug(0, f"nrange {nrange} and combo {combo} are the same")
                    if nrange in self.__fresh_dates:
                        while nrange in self.__fresh_dates:
                            self.__fresh_dates.remove(nrange)
                    continue
                i1, i2 = combo
                if n1 in range(i1, i2 + 1) and n2 in range(i1, i2 + 1):
                    self.log.log_debug(1, f"nrange {nrange} is fully envoloped in current combo {combo}")
                    return True
                elif i1 in range(n1, n2 + 1) and i2 in range(n1, n2 + 1):
                    self.log.log_debug(1, f"nrange {nrange} fully surrounds current combo {combo}")
                    self.log.log_debug(0, f"removing combo {combo}")
                    self.__combined_rates.remove(combo)
                    self.log.log_debug(0, f"combo successfully removed")
                    self.add_to_combined(n1, n2)
                    return True
                elif n1 in range(i1, i2 + 1) and not n2 in range(i1, i2 + 1):
                    self.log.log_debug(0, f"removing combo {combo}")
                    self.__combined_rates.remove(combo)
                    self.log.log_debug(0, f"combo successfully removed")
                    self.add_to_combined(i1, n2)
                    self.log.log_debug(1, f"nrange {nrange} combines to the back of combo {combo} and becoomes" +
                        f" {self.__combined_rates[len(self.__combined_rates) - 1]}")
                    return True
                elif n2 in range(i1, i2 + 1) and not n1 in range(i1, i2 + 1):
                    self.log.log_debug(0, f"removing combo {combo}")
                    self.__combined_rates.remove(combo)
                    self.log.log_debug(0, f"combo successfully removed")
                    self.add_to_combined(n1, i2)
                    self.log.log_debug(1, f"nrange {nrange} combines to the front of combo {combo} and becomes" +
                        f" {self.__combined_rates[len(self.__combined_rates) - 1]}")
                    return True
                self.log.log_debug(0, f"nrange {nrange} does not combine into self.__combined_rates {combo}")
            self.log.log_debug(0, f"there are no matches found for nrange {nrange}")
            return False
        else:
            o1, o2 = ohrange
            if n1 in range(o1, o2 + 1) and n2 in range(o1, o2 + 1):
                self.log.log_debug(1, f"nrange {nrange} is fully enveloped in other range ")
                self.__combined_rates.append((o1, o2))
                return True
            elif o1 in range(n1, n2 + 1) and o2 in range(n1, n2 + 1):
                self.log.log_debug(1, f"nrange {nrange} fully surrounds other range {ohrange}")
                self.__combined_rates.append((n1, n2))
                return True
            elif n1 in range(o1, o2 + 1) and not n2 in range(o1, o2 + 1):
                self.__combined_rates.append((o1, n2))
                self.log.log_debug(1, f"nrange {nrange} combines to the back of other range {ohrange} and becomes" + 
                    f" {self.__combined_rates[len(self.__combined_rates) - 1]}")
                return True
            elif n2 in range(o1, o2 + 1) and not n1 in range(o1, o2 + 1):
                self.__combined_rates.append((n1, o2))
                self.log.log_debug(1, f"nrange {nrange} combines to the front of other range {ohrange} and becomes" +
                    f" {self.__combined_rates[len(self.__combined_rates) - 1]}")
                return True
            self.log.log_debug(0, f"nrange {nrange} does not combine into other range {ohrange}")
            return False

    def combine_possible_ids(self):
        self.__pre_len = len(self.__combined_rates)
        while len(self.__fresh_dates) != 0:
            nrange = self.__fresh_dates[0]
            self.log.log_debug(0, f"checking nrange {nrange}")
            if self.check_combinations(nrange):
                self.__flag_combined = True
                try:
                    while nrange in self.__fresh_dates:
                        self.log.log_debug(0, f"nrange {nrange} is not removed from self.__fresh_dates. removing now")
                        self.__fresh_dates.remove(nrange)
                        self.log.log_debug(0, f"nrange {nrange} successfully removed from self.__fresh_dates")
                    continue
                except ValueError as e:
                    print(f" for some reason even though there is a check before removing self.__fresh_dates is still throwing a value error\n{self.__fresh_dates}")
            for other_range in self.__fresh_dates:
                if nrange == other_range:
                    self.log.log_debug(0, f"nrange {nrange} and other_range {other_range} are the same")
                    continue
                if self.check_combinations(nrange, other_range):
                    self.__flag_combined = True
                    self.log.log_debug(0, f"found combination in nrange {nrange} and other range {other_range} delete both")
                    while nrange in self.__fresh_dates:
                        self.__fresh_dates.remove(nrange)
                    self.__fresh_dates.remove(other_range)
                    break
            if nrange in self.__fresh_dates:
                self.log.log_debug(1, f"no match found for {nrange}. adding to self.__combined_rates")
                self.__combined_rates.append(nrange)
                self.__fresh_dates.remove(nrange)
        
        self.__pst_len = len(self.__combined_rates)
       
        self.log.log_debug(1, f"check condition of flag {self.__flag_combined}\n")
        if self.__flag_combined:
            self.__flag_combined = False
            self.__fresh_dates = copy.deepcopy(self.__combined_rates)
            self.combine_possible_ids()

        
        
    def get_possible_fresh_ids(self):
        self.combine_possible_ids()
        message =  f"finished combinations, adding all possible ids of self.__combined_rates {sorted(self.__combined_rates)}"
        wrapped = textwrap.fill(message, width=300)
        self.log.log_debug(1, wrapped)
        for combo in self.__combined_rates:
            self.__available_ids += (combo[1] - combo[0]) + 1
        return self.__available_ids


 