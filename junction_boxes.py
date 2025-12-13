
class Junction_Boxes:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__boxes = []
        self.__circuits = []
        from logger import Logger
        self.l = Logger(True)

    def analyze_boxes(self):
        with open(self.__file_path) as f:
            self.l.log_event(f"{f.read()}")

    