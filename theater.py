
class Theater:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__p = []
        self.__areas = {}
        self.__border = set()
        self.__interior = set()
        self.__valid = set()
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

        self.l.log_debug(on, f"creating valid zone for decoration")
        self.get_border()
        self.get_interior()
        self.get_valid()

    def get_area(self, p, q):
        if p == q:
            self.l.log_debug(on, f"these points are the same")
            return -1
        x = abs(p[0] - q[0]) + 1
        x = 1 if x == 0 else x
        y = abs(p[1] - q[1]) + 1
        y = 1 if y == 0 else y

        return x * y

    def get_valid(self):
        on = True
        self.l.log_debug(on, f"getting the valid tiles of the redtile and the allowed shape area")
        self.__valid = set(self.__p) | self.__border | self.__interior

    def get_interior(self):
        on = True
        self.l.log_debug(on, f"getting the interior of complex shape")
        xs = [x for x, y in self.__p] #getting all x coordinates
        ys = [y for x, y in self.__p] #getting all y coordinates

        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)
        self.l.log_debug(on, f"min/maxing x and y coordinates minx: {min_x}, miny: {min_y}, maxx: {max_x}, maxy: {max_y}")
        self.l.log_debug(on, f"going through the all encompasing tiles within the area of the min/max coordinates to check boundries")
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):

                if self.point_in_polygon(x, y):
                    self.__interior.add((x,y))

    def get_border(self):
        on = True
        self.l.log_debug(on, f"getting the perimeter of the shape")
        n = len(self.__p)
        for i in range(n):
            self.l.log_debug(on, f"creating edge for points {self.__p[i]} and {self.__p[(i+1)%n]}")
            x1, y1 = self.__p[i]
            x2, y2 = self.__p[(i+1)%n]
            if x1 == x2:
                self.l.log_debug(on, f"this edge is horizontal")
                for y in range(min(y1, y2) + 1, max(y1, y2)):
                    self.__border.add((x1, y))
            if y1 == y2:
                self.l.log_debug(on, f"this edge is vertical")
                for x in range(min(x1, x2) + 1, max(x1, x2)):
                    self.__border.add((x, y1))


    def point_in_polygon(self, x, y):
        on = False
        self.l.log_debug(on, f"using linear interpolation to find intersecting rays, still need to study this more")
        inside = False
        n = len(self.__p)
        for i in range(n):
            x1, y1 = self.__p[i]
            x2, y2 = self.__p[(i + 1) % n]
            if (y1 > y) != (y2 > y):
                crossing_x = x1 + (x2 - x1) * (y-y1) / (y2-y1)
                if crossing_x > x:
                    inside = not inside

        return inside

    def is_rectangle_valid(self, p, q):
        on = False
        self.l.log_debug(on, f"checking points p: {p} and q {q} as a rectangle")
        min_x = min(p[0], q[0])
        max_x = max(p[0], q[0])
        min_y = min(p[1], q[1])
        max_y = max(p[1], q[1])
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (x, y) not in self.__valid:
                    self.l.log_debug(on, f"point {(x,y)} is not valid ")
                    return False
        self.l.log_debug(on, f"p and q checks out.")
        return True

    def save_largest_area(self):
        on = True
        for i, p in enumerate(self.__p.copy()):
            for j, q in enumerate(self.__p.copy()):
                if not self.is_rectangle_valid(p, q):
                    continue
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

    