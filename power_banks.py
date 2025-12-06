class Power_Banks:
    def __init__(self, file_path, digits):
        self.__file_path = file_path
        self.__battery_packs = []
        self.__power_readings = []
        self.tmp_val = -1
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
    
    def flip_pack(self, pack):
        pack_str = str(pack).split()
        self.log.log_event(f"Getting voltage from {pack_str}")
        return str(pack_str)[::-1].replace("[", "").replace("'", "").replace("]", "")

    def get_init_power_reading(self, pack_str_flipped):
        self.log.log_event(f"getting the initial power reading")
        for i in range(0, len(self.__power_readings)):
            self.log.log_event(f"power reading from self.__power_reading is {self.__power_readings[i]}")
            self.log.log_event(f"and power reading from pack_str_flipped is {pack_str_flipped[i]}")
            self.__power_readings[i] = pack_str_flipped[i]
        self.log.log_event(f"initial power reading is {self.__power_readings}")

    def check_pack(self, check, pack):
        self.log.log_event(f"checking if any readings are less than {pack[check]}")
        for reading in self.__power_readings:
            self.log.log_event(f"pack check[{check}]: {pack[check]} > power reading: {reading}")
            if pack[check] > reading:
                self.log.log_event("yep")
                return True
 
        self.log.log_event(f"pack[check]: {pack[check]} was not greater than any of the power readings: {self.__power_readings}")
        return False

    def shove_readings(self, i, check, pack):
        self.log.log_event(f"shoving over power reading index [{i}]")
        if i + 1 < len(self.__power_readings):
            self.shove_readings(i + 1, check, pack)
        else:
            self.log.log_event(f"power reading[{i}] is being shoved to pack[{check}]: {self.__power_readings[i]} -- {pack[check]}")
            self.tmp_val = self.__power_readings[i]
            self.__power_readings[i] = pack[check]
            
        itlen = i
        for j in range(i-1, -1, -1):
            if self.tmp_val != -1 and self.__power_readings[j] < self.tmp_val:
                self.log.log_event(f"index j {j} is {self.__power_readings[j]} and one index up {i - (itlen - (j + 1))} is" +
                f" {self.tmp_val} using tmp_val")
                tmp = self.__power_readings[j]
                self.__power_readings[j] = self.tmp_val
                self.tmp_val = tmp
        self.log.log_event(f"here are the power readings currently { self.__power_readings}")

    def clense(self):
        self.tmp_val = -1

    def adapt_power_readings(self, check, pack):
        i = 0
        self.log.log_event(f"adapting power reading")

        """        
            for i in range(0, len(self.__power_readings)):
            if self.__power_readings[i] < pack[check]:
            if i + 1 < len(self.__power_readings):
        """
        self.shove_readings(i + 1, check, pack)
        self.clense()

    def confirm_power_reading(self):
        self.__voltages.append(int("".join(str(num) for num in self.__power_readings)))
        self.log.log_event(f"Confirming all current power readings { self.__voltages }")

    def get_official_power_reading(self, pack):
        self.log.log_event(f"getting official power readings")
        check = len(self.__power_readings)
        while check < len(pack):
            if self.check_pack(check, pack):
                self.adapt_power_readings(check, pack)
            check += 1

        self.confirm_power_reading()
    
    def get_total_voltage(self):
        sum = 0
        for volts in self.__voltages:
            sum += volts
        return sum

    def get_voltages(self):
        for pack in self.__battery_packs:
            pack_str_flipped = self.flip_pack(pack)
            self.log.log_event(f"pack flipped is {pack_str_flipped}")
            self.get_init_power_reading(pack_str_flipped)
            self.get_official_power_reading(pack_str_flipped)            
        self.log.log_event(f"Total volatage is {self.get_total_voltage()}")