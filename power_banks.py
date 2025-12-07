import copy

LAYER = 1
class Power_Banks:
    def __init__(self, file_path, digits):
        self.__file_path = file_path
        self.__battery_packs = []
        self.__power_readings = []
        self.__voltages = []
        self.__digits = digits
        from logger import Logger
        self.log = Logger(False)
        self.log.log_event(f"log creation completed")
        self.init_power_readings()
    
    def init_power_readings(self):
        counter = 0
        self.__power_readings = []
        self.log.log_event(f"initializing power readings to 0")
        while len(self.__power_readings) < self.__digits:
            self.__power_readings.append({counter : 0})
            counter += 1
        self.log.log_event(f"{self.__power_readings}")
        
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
            self.log.log_event(f"index and layer will be the same in self.__power_readings[{i}][{i}]" + 
            f" for layer {list(self.__power_readings[i].keys())[0]}" +
            f" with a power reading of {pack_str_flipped[i]}")
            self.__power_readings[i][i] =  pack_str_flipped[i]
        self.log.log_event(f"initial power reading is {self.__power_readings}")

    def iterate_through_pack(self, pack, start_pos, stop_pos):
        self.log.log_event(f"iterating through battery pack")
        strongest_battery = { -1: -1}
        for i in range(start_pos, stop_pos):
            if int(list(strongest_battery.values())[0]) <= int(pack[i]):
                key = list(strongest_battery.keys())[0]
                strongest_battery[i] = pack[i]
                strongest_battery.pop(key)
        self.log.log_event(f"strongest battery in index range {start_pos} and {stop_pos} is: {strongest_battery}")
        return strongest_battery
    
    def get_start_and_stop_pos(self, reading, key, value, pack):
        index1 = self.__power_readings.index(reading)
        index2 = len(self.__power_readings) - 1
        self.log.log_event(f"checking index position in self.__power_readings: i1= {index1} i2= {index2}")
        if index1 < index2 and list(self.__power_readings[index1].keys())[0] + 1 < list(self.__power_readings[index1 + 1].keys())[0]:
            self.log.log_event(f"this index: — {index1} — is behind — {index1 + 1} — with layers ranging from  {key} to {list(self.__power_readings[index1 + 1].keys())[0]}")
            return key, list(self.__power_readings[index1 + 1].keys())[0]
        elif index1 == index2:
            self.log.log_event(f"this index: — {index1} — is the last maximum index: with layer {key} to the end of the pack which is layer {len(pack)}")
            return key, len(pack)
        else:
            return key, key


    def find_stronger_battery(self, reading, key, value, pack):
        strongest_battery = {}
        self.log.log_event(f"locating the strongest battery in pack {pack}")
        start_pos, stop_pos = self.get_start_and_stop_pos(reading, key, value, pack)
        strongest_battery = self.iterate_through_pack(pack, start_pos, stop_pos)
        self.log.log_event(f"the strongest battery found was {strongest_battery}")
        return list(strongest_battery.items())[0]

    def update_power_readings(self, reading, layer, power):
        index = self.__power_readings.index(reading)
        key, value = list(reading.items())[0]
        self.log.log_event(f"updating self.__power_readings index [{index}] from layer:power {key}:{value} to {layer}:{power} ")
        self.__power_readings[index][layer] = power
        if key != layer:
            self.__power_readings[index].pop(key)

    def update_pack(self, pack):
        self.log.log_event(f"updating the current pack {pack} for power readings {self.__power_readings}")
        tmp_dict = []
        tmp_dict = copy.deepcopy(self.__power_readings)
        for reading in reversed(self.__power_readings):

            key, value = list(reading.items())[0]
            self.log.log_event(f"checking if layer {key} power of: {value} is <= any power in pack: {pack}" +
            f" between a specific range")
            layer, power = self.find_stronger_battery(reading, key, value, pack)
            if (int(power) > int(value)) or (int(power) == int(value) and int(layer) > int(key)):
                self.log.log_event("yep")
                self.update_power_readings(reading, layer, power)

        self.log.log_event(f"checking if tmp_dict readings {tmp_dict}\nis the same as power readings {self.__power_readings}")
        if tmp_dict != self.__power_readings:
            self.update_pack(pack)
        self.log.log_event(f"in pack: {pack} there were no greater powers than any of the power readings: {self.__power_readings}")

    def save_voltage(self):
        self.log.log_event(f"saving voltage from power reading{self.__power_readings}")
        tmp = []
        for reading in reversed(self.__power_readings):
            layer,power = list(reading.items())[0]
            tmp.append(power)
            volts = int("".join(x for x in tmp))
        self.log.log_event(f"saving current voltage {volts}")
        self.__voltages.append(volts)
        self.init_power_readings()

    def get_official_power_reading(self, pack):
        self.log.log_event(f"getting official power readings")
        self.update_pack(pack)
        self.save_voltage()
    
    def get_total_voltage(self):
        total_volts = 0
        for volts in self.__voltages:
            total_volts += volts
        return total_volts

    def get_voltages(self):
        for pack in self.__battery_packs:
            if len(pack) != 0:
                pack_str_flipped = self.flip_pack(pack)
                self.log.log_event(f"pack flipped is {pack_str_flipped}")
                self.get_init_power_reading(pack_str_flipped)
                self.get_official_power_reading(pack_str_flipped)
        self.log.log_event(f"Total volatage is {self.get_total_voltage()}")
        print(f"Total volatage is {self.get_total_voltage()}")
