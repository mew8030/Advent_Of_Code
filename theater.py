
class Theater:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__p = []
        self.__areas = {}
        from logger import Logger
        self.l = Logger(True)

    def scan_theater_floor(self):
        on = True
        self.l.log_debug(on, f"scanning the theater floor")
        with open(self.__file_path) as f:
            for line in f:
                x, y = map(int, line.strip().split(','))
                self.__p.append((x,y))

        for p in self.__p:
            self.l.log_debug(on, f"{p}")
        self.l.log_debug(on, f"scan complete")

    def get_area(self, p, q):
        if p == q:
            self.l.log_debug(on, f"these points are the same")
            return -1
        x = abs(p[0] - q[0]) + 1
        x = 1 if x == 0 else x
        y = abs(p[1] - q[1]) + 1
        y = 1 if y == 0 else y

        return x * y

    def save_largest_area(self):
        on = True
        for i, p in enumerate(self.__p.copy()):
            for j, q in enumerate(self.__p.copy()):
                if i < j:
                    pxq = self.get_area(p, q)
                    self.l.log_debug(False, f"{pxq} from p {p} and q {q}")
                    if p not in self.__areas:
                        self.__areas[p] = ((pxq, (p,q)))
                    elif pxq > self.__areas[p][0]:
                        self.__areas[p] = ((pxq, (p,q)))
                        self.l.log_debug(on, f"p {p} is a contender for self.__areas {self.__areas[p]}")
        self.__areas = dict(sorted(self.__areas.items(), key=lambda area: area[1], reverse=True))
        for p, area in self.__areas.items():
            self.l.log_debug(on, f"{area}")
    
    def get_largest_area(self):
        max = 0
        for _, area in self.__areas.items():
            if max < area[0]:
                max = area[0]
        return max