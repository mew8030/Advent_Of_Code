
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
        tmp = ""
        for i in range(0, self.paper_cols):
            tmp += "==+=="
        self.log.log_debug(1, tmp)
        for row in self.ws:
            self.log.log_debug(1, f"{row}")
        self.log.log_debug(1, tmp)
    
    #get the position of the x coordinate for the forklift
    def get_flx(self):
        return self.fl_pos[self.flc]

    #get the position of the y corrdinate for the forklift
    def get_fly(self):
        return self.fl_pos[self.flr]

    #puts down the currently held obj which should be either '.', '@', or 'X'
    def put_putdown_obj(self):
        self.log.log_event(f"putting down obj {self.obj_in_space}")
        self.ws[self.get_fly()][self.get_flx()] = self.obj_in_space
        self.obj_in_space = ''
    
    #assigns the parameter marker to the space in the workstation where the forklift is current positioned
    def set_ws_obj_pos(self, marker):
        self.ws[self.get_fly()][self.get_flx()] = marker

    #returns the object in the workspace at the current position of the forklift
    def get_ws_obj_pos(self):
        return self.ws[self.get_fly()][self.get_flx()]

    #picks up the object in the current forklift position marks that area with the forklift marker
    def pick_up_obj(self):
        self.obj_in_space = self.get_ws_obj_pos()
        self.log.log_event(f"picking up object {self.obj_in_space} in space ({self.get_flx()}, {self.get_fly()})")
        self.set_ws_obj_pos(self.fl)

    #gets the nearest wall position
    def get_nearest_wall_pos(self):
        wc_center = 0
        posx, posy = 0, 0
        ws_center = self.paper_cols // 2
        if self.fl_pos[self.flc] > wc_center:
            posx, posy = self.fl_pos[self.flr], self.paper_cols - 1
        else:
            posx, posy =  self.fl_pos[self.flr], 0
        self.log.log_event(f"moving to nearest wall ({posx}, {posy})")
        return posx, posy

    def get_opposite_wall_pos(self):
        posx, posy = 0, 0
        ws_center = (self.paper_cols - 1) // 2

        if self.get_flx() < ws_center:
            self.log.log_debug(0, f"the x coord self.fl_pos x = {self.get_flx()} is less than wcenter = {ws_center}")
            posx, posy, direction = self.paper_cols - 1, self.get_fly(), 1
        else:
            self.log.log_debug(0, f"the x coord {self.get_flx()} is greater than {ws_center}")
            posx, posy, direction =  0, self.get_fly(), -1
        self.log.log_debug(0, f"the wall opposite of forklift is ({posx}, {posy})")
        return posx, posy, direction

    #moves the forklift to the desired position
    def move_fl(self, x, y):
        self.log.log_debug(0, f"moving forklift to ({x}, {y})")
        self.fl_pos[self.flr] = x
        self.fl_pos[self.flc] = y

    #swaps the position of the fl and the object in place
    def move_fl_to(self, x, y):
        self.put_putdown_obj()
        self.move_fl(x, y)
        self.pick_up_obj()

    #move forklift to the left or right by i amount
    def it_flx(self, i):
        self.fl_pos[self.flc] += i
        self.log.log_debug(0, f"moving forklift to ({self.get_flx()}, {self.get_fly()}) in iteration")

    def is_obj_paper(self):
        if self.obj_in_space == '@':
            self.log.log_debug(1, f"found paper in ({self.get_flx()}, {self.get_fly()})")
            return True
        self.log.log_debug(1, f"there is no papwer in ({self.get_flx()}, {self.get_fly()})")
        return False
    #checks current spot for paper, assume that object is picked up here
    def check_space_for_paper(self):
        if self.is_obj_paper():
            #check adjacent areas for paper and sum the amount of paper around obj
            return

    #drive the forklift from one end to the other
    def drive_to_other_side(self, wall, dir):
        while self.get_flx() != wall:
            self.put_putdown_obj()
            self.it_flx(dir)
            self.pick_up_obj()
            self.show_workspace()
        self.log.log_debug(1, f"balls to the wall with the forklift at ({self.get_flx()}, {self.get_fly()})")

    #moves the forklift down the workspace
    def move_fl_down(self):
        self.put_putdown_obj()
        tmp = f"moving down the workspace from ({self.get_flx()}, {self.get_fly()})"
        self.fl_pos[self.flr] += 1
        self.log.log_event(f"{tmp} to ({self.get_flx()}, {self.get_fly()})")
        self.pick_up_obj()
        self.show_workspace()
        self.check_space_for_paper()

    def drive_through_all_rows(self):
        self.log.log_event(f"Driving through all rows in workspace with the forklift")
        wall = (0, 0, 1)
        max_it = 100
        i = 0
        while self.get_fly() != self.paper_rows - 1:
            wall = self.get_opposite_wall_pos()
            self.log.log_debug(0, f"the desired location is ({wall[0], wall[1]} with direction {wall[2]})")
            self.drive_to_other_side(wall[0], wall[2])
            self.move_fl_down()
            if i >= max_it:
                break
            i += 1
            

     #move forklift to the nearest wall if it is not already there then begin driving
     #through the workspace
    def iterate_fl(self):
        x, y = self.get_nearest_wall_pos()
        self.move_fl_to(x, y)
        self.check_space_for_paper()
        self.drive_through_all_rows()

    def find_paper_rolls(self): #iterates through the workspace to find paper rolls
        self.iterate_fl()