
class Paper_Rolls:
    
    def __init__(self, file_path):
        self.__file_path = file_path
        self.paper_rows, self.paper_cols = 0, 0         #number of rows and cols in workspace
        self.fl = '\u235f'                              #⍟ forklift marker
        self.obj_in_space = ''                          #acts as currently held object with '' signifyin nothing is held
        self.flr, self.flc = 0, 1                       #workspace x and y coordinates
        self.fl_pos = [self.flr,0]                      #⍟ forklift position
        self.ws = []                                    #workspace rows
        self.saved_ws_spots = []                        #workspace spots that were marked will be saved in this list
        self.top_to_bottom = True                       #flag to signal if the bottom of the workspace is reached
        self.fl_reach = [                               #adjacent spots to check relative to the forklift position
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, 1),
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1)
            
        ]
        self.workable_spots = 0                         #the number of paper rolls considered efficient to be moved
        self.total_workable_spots = 0                   #the number total rolls moved in workspace after n iterations
        from logger import Logger                       #The logger to log all statements when debugging
        self.log = Logger(False)                         #log for debugging

    def analyze_workspace(self):                        #analyzing workspace
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

    #displays the workspace to work in
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
    def put_down_obj(self):
        self.log.log_event(f"putting down obj {self.obj_in_space}")
        self.ws[self.get_fly()][self.get_flx()] = self.obj_in_space
        self.obj_in_space = ''
    
    #assigns the parameter marker to the space in the workstation where the forklift is current positioned
    def set_ws_obj_pos(self, marker, x = None, y = None):
        if x == None and y == None:
            x = self.get_fly()
            y = self.get_flx()
            self.ws[x][y] = marker
        else:
            self.ws[y][x] = marker

    #returns the object in the workspace at the current position of the forklift
    def get_ws_obj_pos(self, x = None, y = None):
        ws_obj = ''
        if x == None and y == None:
            x = self.get_fly()
            y = self.get_flx()
            ws_obj = self.ws[x][y]
        else:
            ws_obj = self.ws[y][x]
        self.log.log_debug(1, f"objecte in forklift position is ({ws_obj})")
        return ws_obj

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

    #get the farthest wall from the forklift's position
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
        self.put_down_obj()
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
        self.log.log_debug(1, f"there is no paper in ({self.get_flx()}, {self.get_fly()})")
        return False

    def save_ws_marked_spot(self):
        self.saved_ws_spots.append((self.get_flx(), self.get_fly()))


    def mark_ws_spot_for_work(self):
        self.log.log_debug(1, f"this paper in position ({self.get_flx()}, {self.get_fly()}) is workable, marking paper for work")
        self.put_down_obj()
        self.set_ws_obj_pos('X')
        self.save_ws_marked_spot()
        self.workable_spots += 1
        self.pick_up_obj()

    def how_many_paper_neighbors(self):
        neighbors = 0
        self.log.log_event(f"checking neighboring paper rolls from ({self.get_flx()}, {self.get_fly()})")
        for xx, yy in self.fl_reach:
            x = self.get_flx() + xx
            y = self.get_fly() + yy
            if not (x in range(0, self.paper_cols) and y in range(0, self.paper_rows)):
                self.log.log_debug(0, f"({x}, {y}) are not in workspace range")
                continue
            ws_obj = self.get_ws_obj_pos(x, y)
            if ws_obj == '@' or ws_obj == 'X':
                neighbors += 1
            self.log.log_debug(0, f"neighboring object is {ws_obj}  at ({x}, {y}) totaling to {neighbors} neighbor(s)")
            if neighbors > 3:
                self.log.log_event(f"workspace position ({self.get_flx()}, {self.get_fly()}), has too many neighbors")
                return False
        return True


    #checks current spot for paper, assume that object is picked up here
    def check_space_for_paper(self):
        if self.is_obj_paper():
            #check adjacent areas for paper and sum the amount of paper around obj
            if self.how_many_paper_neighbors():
                self.mark_ws_spot_for_work()


    #drive the forklift from one end to the other
    def drive_to_other_side(self, wall, dir):
        while self.get_flx() != wall:
            self.put_down_obj()
            self.it_flx(dir)
            self.pick_up_obj()
            self.check_space_for_paper()
            self.show_workspace()
        self.log.log_debug(1, f"balls to the wall with the forklift at ({self.get_flx()}, {self.get_fly()})")

    #moves the forklift down the workspace
    def move_fl_down(self):
        if self.get_fly() + 1 >= self.paper_rows:
            self.log.log_debug(1, f"forklift is at the bottom of the workplace and cannot move any further")
            self.top_to_bottom = False
            return None
        self.put_down_obj()
        tmp = f"moving down the workspace from ({self.get_flx()}, {self.get_fly()})"
        self.fl_pos[self.flr] += 1
        self.log.log_event(f"{tmp} to ({self.get_flx()}, {self.get_fly()})")
        self.pick_up_obj()
        self.show_workspace()
        self.check_space_for_paper()

    
    #drives the forklift across and down the workspace
    def drive_through_all_rows(self):
        self.log.log_event(f"Driving through all rows in workspace with the forklift")
        wall = (0, 0, 1)
        max_it = 1000
        i = 0
        while self.get_fly() != self.paper_rows:
            wall = self.get_opposite_wall_pos()
            self.log.log_debug(0, f"the desired location is ({wall[0], wall[1]} with direction {wall[2]})")
            self.drive_to_other_side(wall[0], wall[2])
            self.move_fl_down()
            if self.top_to_bottom == False:
                self.log.log_event(f"Finished optimizing work space for all paper rolls that are workable"+
                f"\nthe amount of workable paper rolls is {self.workable_spots}")
                print(f"Finished optimizing work space for all paper rolls that are workable"+
                f"\nthe amount of workable paper rolls is {self.workable_spots}")
                break
            if i >= max_it:
                self.log.log_debug(1, f"maximum amount of iterations reached, closing challenge")
                print(1, f"maximum amount of iterations reached, closing challenge")
                break
            i += 1
            

     #move forklift to the nearest wall if it is not already there then begin driving
     #through the workspace
    def iterate_fl(self):
        x, y = self.get_nearest_wall_pos()
        self.move_fl_to(x, y)
        self.check_space_for_paper()
        self.drive_through_all_rows()

    #clears the marked spots that have been worked in the workspace with '.'
    def clear_worked_spots(self):
        self.log.log_event(f"clearing the workspace")
        if self.obj_in_space == 'X':
            self.obj_in_space = '.'
        for spot in self.saved_ws_spots:
            self.set_ws_obj_pos('.', spot[0], spot[1])
        self.saved_ws_spots = []
        self.log.log_event(f"workspace in now clear of worked areas")
        self.show_workspace()


    def find_paper_rolls(self): #iterates through the workspace to find paper rolls
        self.iterate_fl()
        it = 0
        while(self.workable_spots != 0):
            self.total_workable_spots += self.workable_spots
            it += 1 
            print(f"the current total of workable paper rolls is {self.total_workable_spots} after {it} iterations")
            self.clear_worked_spots()
            self.workable_spots = 0
            self.move_fl_to(0,0)
            self.show_workspace()
            self.top_to_bottom = True
            self.iterate_fl()
        print(f"the current total of workable paper rolls is {self.total_workable_spots} after {it} iterations")

