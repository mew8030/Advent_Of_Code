class Power_Banks:
    def __init__(self, file_path, digits):
        self.__file_path = file_path
        self.__battery_packs = []
        self.__power_readings = []
        while len(self.__power_readings) < digits:
            self.__power_readings.append(0)
        self.__voltages = []
        from logger import Logger
        self.log = Logger(True)
    
    def get_batteries(self):
        self.log.log_event(f"obtaining battery_banks")
        with open(self.__file_path) as f:
            self.__battery_packs = f.read().split('\n')
            self.log.log_event(f"battery_banks are\n{self.__battery_packs}")

    def get_voltages(self):
        for pack in self.__battery_packs:
            max1, curr, max10 = 0,0,0
            pack_str = str(pack).split()
            self.log.log_event(f"Getting voltage from {pack_str}")
            pack_str_flipped = str(pack_str)[::-1].replace("[", "").replace("'", "").replace("]", "")
            self.log.log_event(f"pack flipped is {pack_str_flipped}")
            self.log.log_event(f"getting the initial power reading")
            for i in range(0, len(self.__power_readings)):
                self.log.log_event(f"power reading from self.__power_reading is {self.__power_readings[i]}")
                self.log.log_event(f"and power reading from pack_str_flipped is {pack_str_flipped[i]}")
                self.__power_readings[i] = pack_str_flipped[i]
            self.log.log_event(f"power reading is {self.__power_readings}")
            


            """
            while pack != 0:
                curr = pack % 10
                pack //= 10
                self.log.log_event(f"current value is: {curr} max10 value is: {max10}, max1 value is: {max1}")
                if curr > max10:
                    self.log.log_event(f"current value {curr} is greater than max10 value {max10}")
                    self.log.log_event(f"pack // 10 is {pack // 10}")
                    if max10 > max1 and (pack // 10 != 0):
                        self.log.log_event(f"max10: {max10} is greater than max1: {max1}")
                        max1 = max10
                    if curr != max1:
                        max10 = curr
            """
            self.__voltages.append(max10*10 + max1)
        self.log.log_event(f"volatages are {self.__voltages}")