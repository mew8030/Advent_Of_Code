
class Teleporter:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__mani = []
        self.__s = (0,0)
        self.__beams = set()
        self.__tmp_beams = set()
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

    def split_beam(self, pos):
        self.l.log_debug(1, f"spliting beam into {pos[0], pos[1] + 1} and {pos[0], pos[1] - 1}")
        self.__beams.add((pos[0], pos[1] + 1))
        self.__beams.add((pos[0], pos[1] - 1))
        
        self.l.log_debug(1, f"removing previous beam path {pos}")
        self.__beams.remove((pos[0] - 1, pos[1]))
        self.l.log_debug(1, f"removal complete")
        
        self.__splits += 1

    def beam_behavior(self, c, pos):
        if not self.__beams:
            if c != '^':
                self.l.log_debug(1, f"beam needs to be initialized")
                self.__beams.add(pos)
            else:
                self.split_beam(pos)
        else:
            if c == '^':
                self.l.log_debug(1, f"beam needs to be split at {pos}")
                self.split_beam(pos)
                self.l.log_debug(1, f"beam splitting complete")
            else:
                self.__beams.add(pos)
                self.__beams.remove((pos[0] - 1, pos[1]))

    def create_beam(self):
        self.l.log_event(f"dropping beam from {self.__s} (basically initializing beam)")
        pos = self.__s
        if pos[0] < len(self.__mani):
            pos = self.get_next_pos(pos)
            self.l.log_debug(1, f"getting next position for beam {pos}")
            c = self.get_pos_char(pos)
            self.beam_behavior(c, pos)

    def get_beam_depth(self):
        self.l.log_debug(1, f"getting depth from {self.__beams}")
        for depth, _ in self.__beams:
            self.l.log_debug(1, f"depth = {depth}")
            return depth

    def letting_beam_drop(self):
        self.l.log_event(f"beam free falling from {self.__beams}")
        i = 0
        while self.__deep != len(self.__beams):
            for beam in self.__beams.copy():
                if i > 10000:
                    self.l.log_event(f"too many iterations, stopping program")
                    break
                i += 1
                pos = self.get_next_pos(beam)
                self.l.log_debug(1, f"analyzing beam {beam}")
                if pos == beam:
                    self.l.log_debug(1, f"beam {beam} is at the bottom of the manifold")
                    self.__deep += 1
                    continue
                self.l.log_debug(0, f"beam dropping to {pos}")
                c = self.get_pos_char(pos)
                self.l.log_debug(0, f"character in pos {pos} is {c}")
                self.beam_behavior(c, pos)
            if i > 10000:
                self.l.log_event(f"too many iterations, stopping program")
                break
        self.l.log_event(f"beam splits = {self.__splits}\nbeam drop results\n{sorted(self.__beams)}")