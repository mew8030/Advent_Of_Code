
class Junction:
    def __init__(self, boxes = None):
        from logger import Logger
        self.l = Logger(True)
        if boxes == None:
            return
        self.__circuit = {box: box for box in boxes}
        self.__csize = {box: 1 for box in boxes}
    
    def find(self, box):
        on = False
        self.l.log_debug(on, f"looking for box {box} in self.__circuit {self.__circuit}")
        if self.__circuit[box] != box:
           self.__circuit[box] = self.find(self.__circuit[box])
        return self.__circuit[box]

    def merge_jnc(self, b1, b2):
        on = False
        x, y = self.find(b1), self.find(b2)
        if x == y:
            self.l.log_debug(on, f"these junctions are already connected")
            return False
        if self.__csize[x] < self.__csize[y]:
            x, y = y, x
        self.l.log_debug(on, f"adding {y} to {x} with y size {self.__csize[y]} being added to x's size {self.__csize[x]}")
        self.__circuit[y] = x
        self.__csize[x] += self.__csize[y]
        self.l.log_debug(on, f"circuit is now {self.__circuit[x]} with size {self.__csize[x]}")
        return True
    
    def show_sizes(self):
        on = True
        self.l.log_debug(on, f"showing the sizes of the circuits")
        self.l.log_event(f"{dict(sorted(self.__csize.items(), key=lambda value: value[1], reverse = True)).values()}")

    def multiply_boxes(self, quantity):
        on = True
        tmp = list(dict(sorted(self.__csize.items(), key=lambda value: value[1], reverse = True)).values())
        mult = 1
        for i in range(0,quantity):
            mult *= tmp[i]
        self.l.log_debug(on, f"the three biggest circuits multiplied together results in {mult}")
class Junction_Boxes:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__boxes = []
        self.__circuits = {}
        self.__distances = []
        self.__jnc = Junction()
        from logger import Logger
        self.l = Logger(True)

    def get_distance(self, b1, b2):
        return ((b1[0] - b2[0])**2 + (b1[1] - b2[1])**2 + (b1[2] - b2[2])**2)**0.5

    def get_distances(self):
        on = False
        self.l.log_debug(on, f"getting all the distances between boxes")
        for i, b1 in enumerate(self.__boxes):
            for j, b2 in enumerate(self.__boxes):
                if i < j:
                    self.__distances.append((self.get_distance(b1, b2), b1, b2))
        self.l.log_debug(on, f"distance acquisition complete")
        self.__distances = list(sorted(self.__distances))
        for dist in self.__distances:
            self.l.log_debug(on, f"{dist}")



    def analyze_boxes(self):
        on = True
        self.l.log_debug(on, f"reading file {self.__file_path}")
        with open(self.__file_path) as f:
            for line in f:
                x, y, z = map(int, line.strip().split(','))
                self.__boxes.append((x,y,z))
        for box in self.__boxes:
            self.l.log_debug(on, f"{box}")
        
        self.get_distances()
        self.__jnc = Junction(self.__boxes)

    def connect_circuits(self):
        on = True
        connections = 0
        for dist , b1, b2 in self.__distances:
            if connections > 999:
                break
            success = self.__jnc.merge_jnc(b1, b2)
            connections += 1

            current_status = "junctions combined" if success else "nothing happens"
            self.l.log_debug(on, f"connection: {connections} box1: {b1}, box2: {b2}, dist: {dist}, {current_status}")
        self.__jnc.show_sizes()
        self.__jnc.multiply_boxes(3)

