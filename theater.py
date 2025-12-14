
class Theater:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__p = []
        from logger import Logger
        self.l = Logger(True)

    def scan_theater_floor(self):
        on = True
        self.l.log_debug(on, f"scanning the theater floor")
        with open(self.__file_path) as f:
            for line in f:
                x, y = map(int, line.strip().split(','))
                self.__p.append((x,y))

        self.l.log_debug(on, f"scan complete")

                