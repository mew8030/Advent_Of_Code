from safe import Safe
from invalid_ids import Invalid_ids
class Logger:
    def __init__(self, debug=False):
        print(f"initializing Logger")
        self.__debug = debug
        print(F"logger initialization completed")


    def log_event(self, event):
        if self.__debug:
            print(f"{event} ")
    
    def log_debug(self, num, event):
        if num != 0:
            print(f"{event}")

    def log_sequence(self, rotation, lorR, num):
        print(f"sequence {rotation} turning {lorR} about {num} times")

    def log_turn_dial_initialization(self, safe):
        if self.__debug:
            print(f"dial position is {safe.dial[safe.dial_pos]} turning to the {safe.get_turn_direction()}" + 
            f" {safe.get_turn_cycles()} times")
    
    def log_turn_dial_event(self, safe):
        if self.__debug:
            print(f"Click from {safe.dial[safe.dial_pos]} to {safe.tmp_dial[safe.dial_pos]}")

    def log_turn_dial_completion(self, safe):
        if self.__debug:
            print(f"The dial is rotated {safe.get_turn_direction()}{safe.get_turn_cycles()} to point at " +
            f"{safe.dial[safe.dial_pos]}")
    
    def log_dial_going_pass_limit(self, safe, turn):
        if self.__debug:
            tmp = []
            if safe.dial_pos == 0 and safe.get_turn_direction == 'R':
                tmp = "99 to 0"
            else:
                tmp = "0 to 99"
            print(f"dial went from {tmp} on turn {turn} of {safe.get_turn_cycles()}")