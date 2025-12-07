
class Paper_Rolls:
    
    def __init__(self, file_path):
        self.__file_path = file_path
        self.paper_rows, self.paper_cols = 0, 0 #number of rows and cols in workspace
        self.fl = '\u235f'                      #⍟ forklift marker
        self.obj_in_space = ''
        self.flr, self.flc = 0, 1
        self.fl_pos = [self.flr,0]                     #⍟ forklift position
        self.ws = []                            #workspace rows
        from logger import Logger
        self.log = Logger(True)                 #log for debugging

    def analyze_workspace(self):                #analyzing workspace
        self.log.log_event("""
                analyzing workspace for forklift to access paper rolls 
                with fewer than 4 adjacent paper rolls in the 8 adjacent
                areas around said roll
            """)
        with open(self.__file_path) as f:
            ws = f.read().split('\n')
            tmp_ws = []
            for row_space in ws:
                tmp_ws.append(row_space)

            for row in tmp_ws:
                self.ws.append([])
                for col in row:
                    self.log.log_debug(0,f"creating column {len(self.ws[self.paper_rows]) + 1} for row {self.paper_rows}")
                    self.ws[self.paper_rows].append(col)
                self.paper_rows += 1
            self.paper_cols = len(self.ws[0])
            self.log.log_debug(1, f"the dimensions of the workspace are rows x cols {self.paper_rows} x {self.paper_cols}")
            self.initialize_forklift()
            self.show_workspace()

    def initialize_forklift(self):
        self.log.log_event("placing the forklift in the workspace")
        while self.ws[self.fl_pos[self.flr]][self.fl_pos[self.flc]] != '.':
            if self.fl_pos[self.flc] < self.paper_rows:
                self.fl_pos[self.flc] += 1
            elif self.fl_pos[self.flr] < self.paper_cols:
                self.fl_pos[self.flc] = 0
                self.fl_pos[self.flr] += 1
            else:
                self.log.log_debug(1, f"there is no space in the workspace for the forklift")
                self.fl_pos[self.flr] = 0
                self.fl_pos[self.flc] = 0
                return
        self.log.log_debug(1, f"forklift position is {self.fl_pos[self.flr]}, {self.fl_pos[self.flc]}")
        self.obj_in_space = self.ws[self.fl_pos[self.flr]][self.fl_pos[self.flc]]
        self.ws[self.fl_pos[self.flr]][self.fl_pos[self.flc]] = self.fl
    def show_workspace(self):
        for row in self.ws:
            self.log.log_event(f"{row}")