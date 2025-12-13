
class Teleporter:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__mani = []
        self.__s = (0,0)
        #self.__beams = set()
        self.__beams = {}
        self.__total_beam_count = 0
        self.__splits = 0
        self.__deep = 0
        from logger import Logger
        self.l = Logger(True)
    
    def analyze_manifold(self):
        self.l.log_event(f"analyzing schematics")
        with open(self.__file_path) as f:
            self.__mani = f.read().splitlines()
        self.l.log_event(f"schematic {self.__file_path} open")
        self.l.log_event(f"reading lines of schematics")
        for i in range(0, len(self.__mani)):
            self.l.log_debug(1, f"{self.__mani[i]}")
        self.l.log_event(f"lines from schematic read")
        self.l.log_event(f"getting starting position")
        i = self.__mani[0].index('S')
        self.__s = (0, i)
        self.l.log_debug(1, f"starting position is self.__mani[0][{i}]: {self.__s}")

    def get_next_pos(self, pos):
        if pos[0] + 1 < len(self.__mani):
            return (pos[0] + 1, pos[1])
        else:
            return pos

    def get_pos_char(self, pos):
        return self.__mani[pos[0]][pos[1]]

    def add_beam(self, pos, v = 1):
        if not pos in self.__beams:
            self.__beams[pos] = v
        else:
            self.__beams[pos] += v

    def split_beam(self, pos):
        on = False
        previous = (pos[0] - 1, pos[1])
        v = self.__beams.get((pos[0] - 1, pos[1]))
        left = (pos[0], pos[1] - 1)
        right = (pos[0], pos[1] + 1)
        self.l.log_debug(on, f"from beam {previous} the value is: {v}")
        self.l.log_debug(on, f"spliting beam into {right} with {v} and {left} with {v}")
        self.add_beam(right, v)
        self.add_beam(left, v)
        
        self.l.log_debug(on, f"removing previous beam path {pos}")
        del self.__beams[previous]
        self.l.log_debug(on, f"removal complete")
        self.l.log_debug(on, f"beam splitting complete with left: {left} having {self.__beams.get(left)} and right: {right} having {self.__beams.get(right)}")
        
        self.__splits += 1

    def beam_behavior(self, c, pos):
        on = False
        if not self.__beams:
            if c != '^':
                self.l.log_debug(on, f"beam needs to be initialized")
                if not pos in self.__beams:
                    self.__beams[pos] = 1
                else:
                    self.__beams[pos] += 1
            else:
                self.split_beam(pos)
        else:
            if c == '^':
                self.l.log_debug(on, f"beam needs to be split at {pos}")
                self.split_beam(pos)
            else:
                self.add_beam(pos, self.__beams.get((pos[0] - 1, pos[1])))
                del self.__beams[(pos[0] - 1, pos[1])]

    def create_beam(self):
        on = True
        self.l.log_event(f"dropping beam from {self.__s} (basically initializing beam)")
        pos = self.__s
        if pos[0] < len(self.__mani):
            pos = self.get_next_pos(pos)
            self.l.log_debug(on, f"getting next position for beam {pos}")
            c = self.get_pos_char(pos)
            self.beam_behavior(c, pos)

    def get_beam_depth(self):
        on = True
        self.l.log_debug(on, f"getting depth from {self.__beams}")
        for depth, _ in self.__beams:
            self.l.log_debug(on, f"depth = {depth}")
            return depth

    def letting_beam_drop(self):
        on = True
        self.l.log_event(f"beam free falling from {self.__beams}")
        i = 0
        while self.__deep != len(self.__beams):
            for beam, overlap in self.__beams.copy().items():
                
                if i > 10000:
                    self.l.log_event(f"too many iterations, stopping program")
                    break
                i += 1
                pos = self.get_next_pos(beam)
                self.l.log_debug(on, f"analyzing beam {beam} with {overlap} overlapping beams")
                if pos == beam:
                    self.l.log_debug(on, f"beam {beam} is at the bottom of the manifold")
                    self.__deep += 1
                    continue
                self.l.log_debug(0, f"beam dropping to {pos}")
                c = self.get_pos_char(pos)
                self.l.log_debug(0, f"character in pos {pos} is {c}")
                self.beam_behavior(c, pos)
            if i > 10000:
                self.l.log_event(f"too many iterations, stopping program")
                break
        self.l.log_event(f"beam splits = {self.__splits}\nbeam drop results\n{self.__beams}")
        for _, beams in self.__beams.items():
            self.__total_beam_count += beams
        self.l.log_event(f"total beam count is {self.__total_beam_count}")