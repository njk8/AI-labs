from lab1.liuvacuum import *
from random import randint

DEBUG_OPT_DENSEWORLDMAP = False

AGENT_STATE_UNKNOWN = 0
AGENT_STATE_WALL = 1
AGENT_STATE_CLEAR = 2
AGENT_STATE_DIRT = 3
AGENT_STATE_HOME = 4

AGENT_DIRECTION_NORTH = 0
AGENT_DIRECTION_EAST = 1
AGENT_DIRECTION_SOUTH = 2
AGENT_DIRECTION_WEST = 3

def direction_to_string(cdr):
    cdr %= 4
    return  "NORTH" if cdr == AGENT_DIRECTION_NORTH else\
            "EAST"  if cdr == AGENT_DIRECTION_EAST else\
            "SOUTH" if cdr == AGENT_DIRECTION_SOUTH else\
            "WEST" #if dir == AGENT_DIRECTION_WEST

"""
Internal state of a vacuum agent
"""
class MyAgentState:
		
    def __init__(self, width, height):

        # Initialize perceived world state
        self.world = [[AGENT_STATE_UNKNOWN for _ in range(height)] for _ in range(width)]
        self.world[1][1] = AGENT_STATE_HOME

        # Agent internal state
        self.last_action = ACTION_NOP
        self.second_last_action = ACTION_NOP
        self.direction = AGENT_DIRECTION_EAST
        self.pos_x = 1
        self.pos_y = 1

        # Metadata
        self.world_width = width
        self.world_height = height

    """
    Update perceived agent location
    
    """
    def check_visited(self, visit, visitx, k):
        counter = 0
        for i in range(self.world_height):
            for j in range(self.world_width):
                if (i == k  or j == k or (i == self.world_height - 1 - k) or (j == self.world_height - 1 - k)):
                    if visit[i][j] or visitx[i][j]:
                        print(visit[i][j], end=' ')
                        counter += 1
                else:
                    print(" ", end=' ')
            print()
        print("Counter Value:", counter)
        if counter == ((self.world_height - 2*k) * (self.world_width - 2*k) - (self.world_height - 2 - 2*k) * (self.world_width - 2 - 2*k)) + 8*k:
            print("Final-Counter")
            return True
        else:
            return False
                        
            
                
        
    def update_pos_after_o(self, bump):
        if bump and self.direction == AGENT_DIRECTION_EAST:
            self.direction = AGENT_DIRECTION_NORTH
        elif bump and self.direction == AGENT_DIRECTION_NORTH:
            self.direction = AGENT_DIRECTION_WEST
        elif bump and self.direction == AGENT_DIRECTION_WEST:
            self.direction = AGENT_DIRECTION_SOUTH
        elif bump and self.direction == AGENT_DIRECTION_SOUTH:
            self.direction = AGENT_DIRECTION_EAST
                
    def update_pos_after_b(self, bump):
        if bump and self.direction == AGENT_DIRECTION_EAST:
            self.direction = AGENT_DIRECTION_SOUTH
        elif bump and self.direction == AGENT_DIRECTION_SOUTH:
            self.direction = AGENT_DIRECTION_WEST
        elif bump and self.direction == AGENT_DIRECTION_WEST:
            self.direction = AGENT_DIRECTION_NORTH
        elif bump and self.direction == AGENT_DIRECTION_NORTH:
            self.direction = AGENT_DIRECTION_EAST
                    
                    
    def update_position(self, bump):
        if not bump and self.last_action == ACTION_FORWARD:
            if self.direction == AGENT_DIRECTION_EAST:
                self.pos_x += 1
            elif self.direction == AGENT_DIRECTION_SOUTH:
                self.pos_y += 1
            elif self.direction == AGENT_DIRECTION_WEST:
                self.pos_x -= 1
            elif self.direction == AGENT_DIRECTION_NORTH:
                self.pos_y -= 1	
			        	      		
		
    """
    Update perceived or inferred information about a part of the world
    """	
    def update_world(self, x, y, info):
        self.world[x][y] = info

    """
    Dumps a map of the world as the agent knows it
    """
    def print_world_debug(self):
        for y in range(self.world_height):
            for x in range(self.world_width):
                if self.world[x][y] == AGENT_STATE_UNKNOWN:
                    print("?" if DEBUG_OPT_DENSEWORLDMAP else " ? ", end="")
                elif self.world[x][y] == AGENT_STATE_WALL:
                    print("#" if DEBUG_OPT_DENSEWORLDMAP else " # ", end="")
                elif self.world[x][y] == AGENT_STATE_CLEAR:
                    print("." if DEBUG_OPT_DENSEWORLDMAP else " . ", end="")
                elif self.world[x][y] == AGENT_STATE_DIRT:
                    print("D" if DEBUG_OPT_DENSEWORLDMAP else " D ", end="")
                elif self.world[x][y] == AGENT_STATE_HOME:
                    print("H" if DEBUG_OPT_DENSEWORLDMAP else " H ", end="")

            print() # Newline
        print() # Delimiter post-print

"""
Vacuum agent
"""
class MyVacuumAgent(Agent):

    def __init__(self, world_width, world_height, log):
        super().__init__(self.execute)
        self.WH = world_height
        self.WW = world_width
        self.visited = [[AGENT_STATE_UNKNOWN for _ in range(world_height)] for _ in range(world_width)]
        self.visited2 = [[AGENT_STATE_UNKNOWN for _ in range(world_height)] for _ in range(world_width)]
        self.k = 1
        self.initial_random_actions = 0
        self.iteration_counter = self.WH * self.WW * 2
        self.state = MyAgentState(world_width, world_height)
        self.log = log

    def move_to_random_start_position(self, bump):
        action = random()

        self.initial_random_actions -= 1
        self.state.update_position(bump)

        if action < 0.1666666:   # 1/6 chance
            self.state.direction = (self.state.direction + 3) % 4
            self.state.last_action = ACTION_TURN_LEFT
            return ACTION_TURN_LEFT
        elif action < 0.3333333: # 1/6 chance
            self.state.direction = (self.state.direction + 1) % 4
            self.state.last_action = ACTION_TURN_RIGHT
            return ACTION_TURN_RIGHT
        else:                    # 4/6 chance
            self.state.last_action = ACTION_FORWARD
            return ACTION_FORWARD

    def execute(self, percept):

        ###########################
        # DO NOT MODIFY THIS CODE #
        ###########################

        bump = percept.attributes["bump"]
        dirt = percept.attributes["dirt"]
        home = percept.attributes["home"]

        # Move agent to a randomly chosen initial position
        if self.initial_random_actions > 0:
            self.log("Moving to random start position ({} steps left)".format(self.initial_random_actions))
            return self.move_to_random_start_position(bump)

        # Finalize randomization by properly updating position (without subsequently changing it)
        elif self.initial_random_actions == 0:
            self.initial_random_actions -= 1
            self.state.update_position(bump)
            self.state.last_action = ACTION_SUCK
            self.log("Processing percepts after position randomization")
            for i in range(self.WH):
                for j in range(self.WW):
                    if i == 0 or i == (self.WH - 1) or j == 0 or j == (self.WW - 1):
                        self.visited[i][j] = 4
                        self.visited2[i][j] = 4
            self.visited2[1][1] = self.visited[1][1] = 1
            return ACTION_SUCK


        ########################
        # START MODIFYING HERE #
        ########################
        
     
        # Max iterations for the agent  ---- Change the No. of Iterations here -----
        if self.iteration_counter < 1:
            if self.iteration_counter == 0:
                self.log("Iteration counter is now 0. Halting!")
                self.log("Performance: {}".format(self.performance))
                self.iteration_counter -= 1
            self.state.last_action = ACTION_NOP    
            return ACTION_NOP

        self.log("Position: ({}, {})\t\tDirection: {}".format(self.state.pos_x, self.state.pos_y,
                                                              direction_to_string(self.state.direction)))

        self.iteration_counter -= 1

        # Track position of agent ---- updates to NONE ---
        
        self.state.update_position(bump)
        
        
      
        if bump:
            # Get an xy-offset pair based on where the agent is facing
            offset = [(0, -1), (1, 0), (0, 1), (-1, 0)][self.state.direction]

            # Mark the tile at the offset from the agent as a wall (since the agent bumped into it)
            self.state.update_world(self.state.pos_x + offset[0], self.state.pos_y + offset[1], AGENT_STATE_WALL)

        # Update perceived state of current tile
        if dirt:
            self.state.update_world(self.state.pos_x, self.state.pos_y, AGENT_STATE_DIRT)
        else:
            self.state.update_world(self.state.pos_x, self.state.pos_y, AGENT_STATE_CLEAR)

        # Debug
        ##self.state.print_world_debug()

        # Decide action
        
        print("xxx200xxx")
        print(self.state.pos_x, self.state.pos_y, self.state.direction)
        print("xxx200xxx")
        
        print("This is", self.WH,"x" ,self.WW, "Iteration: ", self.iteration_counter)
        for i in range(self.WH):
            for j in range(self.WW):
                print(self.visited[i][j], end=' ')
            print()    

        print("$$$$$$$$$")
        print("$$$$$$$$$")
        #self.state.check_visited(self.visited2, self.visited, self.k)       

        
        
        if(self.state.check_visited(self.visited2, self.visited, self.k)):
            self.visited[self.k][self.k] = 4
            if(self.state.pos_x != self.k and (self.state.pos_x != self.WH - self.k - 1) and self.state.pos_y != self.k and (self.state.pos_y != self.WW - self.k - 1)):
                print("#$# OUT #$#")
                for i in range(self.WH):
                    for j in range(self.WW):
                        if (i == self.k  or j == self.k or (i == self.WH - 1 - self.k) or (j == self.WW - 1 - self.k)):
                            self.visited[i][j] = 4
                self.k += 1
             

        f = [(0, -1), (1, 0), (0, 1), (-1, 0)][self.state.direction]
        l = [(-1, 0), (0, -1), (1, 0), (0, 1)][self.state.direction]
        
        
        #self.state.second_last_action =  self.state.last_action
        print("****State****:", str(self.state.last_action))
        print("****bump****:", bump)
        
        
                 
        if dirt:
            self.log("DIRT -> choosing SUCK action!")
            self.state.last_action = ACTION_SUCK
            return ACTION_SUCK
        elif (self.state.last_action != ACTION_TURN_LEFT) and (self.visited2[self.state.pos_y + l[1]][self.state.pos_x + l[0]] == 0):
            self.state.update_pos_after_o(True)
            self.state.last_action = ACTION_TURN_LEFT
            return ACTION_TURN_LEFT
        elif bump or self.visited[self.state.pos_y + f[1]][self.state.pos_x + f[0]]:
            self.visited[self.state.pos_y + f[1]][self.state.pos_x + f[0]] = 4
            self.visited2[self.state.pos_y + f[1]][self.state.pos_x + f[0]] = 4
            self.state.update_pos_after_b(True)
            self.state.last_action = ACTION_TURN_RIGHT
            return ACTION_TURN_RIGHT
        else:
            self.visited2[self.state.pos_y][self.state.pos_x] = 1
            self.state.last_action = ACTION_FORWARD
            return ACTION_FORWARD
