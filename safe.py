
class Safe:

    def __init__(self, file_path):
        print(f"creating safe")
        self.dial = []
        self.tmp_dial = []
        self.dial_pos = 50
        self.__sequence = []
        self.__turn_direction = ""
        self.__turn_cycles = 0
        self.__file_path = file_path
        self.counter = 0
        self.clue = 0
        print(f"safe created")
        print(f"creating Logger")
        from logger import Logger
        print(f"creating Logger")
        self.log = Logger(True)
        self.log.log_event("Logger created")
        self.log.log_event("Creating Dial")
        for num in range(0, 100):
            self.dial.append(num)
        self.log.log_event("Dial Created")
        self.log.log_event("Getting Combination")
        self.get_combination()
        self.log.log_event("Combination found")

            

    def turn_dial(self , sequence): # should have at least one character of 'L' or 'R'
        if len(sequence) == 0:
            raise Exception("the sequence list is empty")

    def get_turn_cycles(self):
        return self.__turn_cycles

    def get_turn_direction(self):
        if self.__turn_direction == 'R':
            return "Right"
        return "Left"

    def get_combination(self):
        self.log.log_event("Getting Location of file with combination")
        with open(self.__file_path) as f:
            combination = f.read()

        
        for sequence in combination.split('\n'):
            self.__sequence.append(sequence)
    def iterate_clue(self):
        if self.dial[self.dial_pos] == 0:
            self.clue += 1
            self.log.log_event(f"current clue is : {self.clue}")
        return

    def unlock(self):
        for turn in self.__sequence:
            self.__turn_direction = turn[:1]
            self.__turn_cycles = int(turn[1:])
            self.counter = self.__turn_cycles
            self.log.log_debug(1, f"dial position is {self.dial[self.dial_pos]} turning to the {self.get_turn_direction()}" + 
            f" {self.get_turn_cycles()} times")
            while(self.counter):
                self.counter -= 1
                if self.__turn_direction == 'R':
                    self.tmp_dial = self.dial[1:]
                    self.tmp_dial += self.dial[:1]
                else:
                    self.tmp_dial = self.dial[-1:]
                    self.tmp_dial += self.dial[:-1]
                self.log.log_debug(0, f"Click from {self.dial[self.dial_pos]} to {self.tmp_dial[self.dial_pos]}")
                
                self.log.log_debug(0, f"tmp_dial at 0 is {self.tmp_dial[0]} and tmp_dial at {self.dial_pos} is" +
                    f" {self.tmp_dial[self.dial_pos]}")

                if int(self.tmp_dial[self.dial_pos]) == 0:
                    self.clue += 1
                    self.log.log_debug(1, f"tmp_dial[50] = {self.tmp_dial[self.dial_pos]} total clue = {self.clue}")
                self.dial = self.tmp_dial
                self.tmp_dial = []
            self.log.log_turn_dial_completion(self)

    
    def get_clues(self):
        return self.clue
            
                    
                    
            



        


