# Imports

import room
import numpy as np
import pandas as pd
from room import Room
from agent import Agent

# the score wasn't used as it wasn't needed for the algorithm
GOLD_REWARD = 1000
WUMPUS_REWARD = 500

WALK_PUNISHMENT = -1
ARROW_PUNISHMENT = -100

class Game:

	'''
	Defining our board using rooms.
	
	This is the main class of the game. It contains all the methods that are used to play the game.
	'''
	def __init__(self, path_to_file):
		self.path_to_file = path_to_file
		self.board = []
		self.trace = [(1,1)]
		self.game_over = False
		self.game_won = False
		self.num_moves = 0
		self.wumpus_dead = False
		self.exit = (1,1)

		self.percepts = {
			"breeze": False,
			"stench": False,
			"glitter": False,
			"bump": False,
			"scream": False
		}


	def read_game_data(self):
		'''
		Reads the game data from the txt document
		'''
		self.X = pd.read_csv(self.path_to_file, sep="\t", header=None)
		self.game_data = list(self.X[0][:])
		return self.game_data

	def create_board(self, game_data):
		'''
		Creates a board with correct dimensions for the game
		'''
		self.game_size = [i for i in self.game_data if i[0] == "M"][0]
		self.length, self.height = int(self.game_size[1]),int(self.game_size[2])
		
		for i in range(self.length):
			row = []
			for j in range(self.height):
				row.append(room.Room(i,j))
			self.board.append(row)
		return self.board

	def fill_board(self, board):
		'''
		Fills the board with data from the txt file
		(the indexing is weird because we get all data starting from 1 and not 0)
		'''
		for i in self.game_data:
			self.coordinates = i[-2:]
			x, y = int(self.coordinates[0]) - 1, int(self.coordinates[1]) - 1
			self.contents = i[:-2]

			# Setting the agent
			if self.contents == "A": 
				self.board[x][y].set_agent(True)
				self.agent = Agent(x,y)

			# Setting the wumpus and stench in adjacent rooms
			if self.contents == "W":
				self.board[x][y].set_wumpus(True)

			if self.contents == "S":
				self.board[x][y].set_stench(True)

			# Setting the pits and breeze in adjacent rooms
			if self.contents == "P":
				self.board[x][y].set_pit(True)

			if self.contents == "B":
				self.board[x][y].set_breeze(True)

			# Setting the gold and glitter
			if self.contents == "G":
				self.board[x][y].set_gold(True)
				self.board[x][y].set_glitter(True)

			# Setting the exit
			if self.contents == "GO":
				self.board[x][y].set_exit(True)
				self.exit = (x,y)

		return self.board

	def move_forward(self):
		'''
		Moves forward one room, depending on the direction the agent is facing
		'''
		self.x, self.y = self.agent.get_position()
		if self.agent.facing == "right":

			if self.x < self.length-1:
				self.bump = False                
				self.x += 1
				self.num_moves += 1
				self.agent.set_position(self.x,self.y)
				self.trace.append((self.x + 1,self.y + 1))
				print('Moved to ({0},{1})'.format(str(self.x + 1), str(self.y + 1)))
			else:
				self.bump = True
				self.num_moves += 1
				print("You have bumped into a wall!")

		elif self.agent.facing == "left":
			if self.x > 0:
				self.bump = False
				self.x -= 1
				self.num_moves += 1
				self.agent.set_position(self.x,self.y)
				self.trace.append((self.x+ 1,self.y+ 1))
				print('Moved to ({0},{1})'.format(str(self.x+ 1), str(self.y+ 1)))
			else:
				self.bump = True
				self.num_moves += 1
				print("You have bumped into a wall!")

		elif self.agent.facing == "up":
			if self.y < self.height-1:
				self.bump = False                
				self.y += 1
				self.num_moves += 1
				self.agent.set_position(self.x,self.y)
				self.trace.append((self.x+ 1,self.y+ 1))
				print('Moved to ({0},{1})'.format(str(self.x+ 1), str(self.y+ 1)))
			else:
				self.bump = True
				self.num_moves += 1
				print("You have bumped into a wall!")

		elif self.agent.facing == "down":
			if self.y > 0:
				self.bump = False                
				self.y -= 1
				self.num_moves += 1
				self.agent.set_position(self.x,self.y)
				self.trace.append((self.x+ 1,self.y+ 1))
				print('Moved to ({0},{1})'.format(str(self.x+ 1), str(self.y+ 1)))
			else:
				self.bump = True
				self.num_moves += 1
				print("You have bumped into a wall!")

	def change_facing_cwise(self):
		''' 
		This changes the direction of the agent by 90 degrees, clockwise
		'''
		facing = ["right","down","left","up"]
		agent_facing = self.agent.get_facing()
		new_facing = facing[(facing.index(agent_facing) + 1) % 4]
		self.agent.set_facing(new_facing)
		self.num_moves += 1
		print("Changed direction to {}".format(str(new_facing)))

	def change_facing_ccwise(self):
		''' 
		This changes the direction of the agent by 90 degrees, counterclockwise
		'''
		facing = ["right","up","left","down"]
		agent_facing = self.agent.get_facing()
		new_facing = facing[(facing.index(agent_facing) + 1) % 4]
		self.agent.set_facing(new_facing)
		self.num_moves += 1
		print("Changed direction to {}".format(str(self.agent.get_facing())))

	def generate_wumpus_kb(self):
		'''
		Generates a knowledge base for the wumpus from the percepts of the rooms we visited:

		0 - The room doesn't have a wumpus
		1 - The room has a wumpus
		2 - The room maybe has a wumpus
		3 - The room has stench
		4 - There is no info about the room
		'''

		self.wumpus_kb_zeros = np.zeros([self.length, self.height])
		self.wumpus_board = np.full_like(self.wumpus_kb_zeros, 4)
		return self.wumpus_board
	
	def generate_pit_kb(self):
		'''
		Generates a knowledge base for the pit from the percepts of the rooms we visited:

		0 - The room doesn't have a pit
		1 - The room has a pit
		2 - The room maybe has a pit
		3 - The room has breeze
		4 - There is no info about the room
		'''

		self.pit_kb_zeros = np.zeros([self.length, self.height])
		self.pit_board = np.full_like(self.pit_kb_zeros, 4)
		return self.pit_board

	def generate_visited_rooms(self):
		''' 
		Generates a knowledge base of visited rooms from the rooms we visited:

		0 - The room has not been visited and we are not sure if can be visited
		1 - The room can be visited but is not visited yet
		2 - The room has been visited
		'''
		self.visited_rooms = np.zeros([self.length, self.height])
		return self.visited_rooms

	def adjacent_rooms(self):
		'''
		Generating adjacent rooms to the players position
		'''
		x, y = self.agent.get_position()
		array = []
		if x > 0:
			array.append(self.board[x-1][y])
		if x < self.length:
			array.append(self.board[x+1][y])
		if y > 0:
			array.append(self.board[x][y-1])
		if y < self.height:
			array.append(self.board[x][y+1])
		return array

	def adjacent_matrix_elements(self, matrix, x, y):
		'''
		Generates all adjacent elements to a matrix element (up,down,left,right)
		'''
		array = []
		if x > 0:
			array.append(int(matrix[x-1][y]))
		if x < self.length-1:
			array.append(int(matrix[x+1][y]))
		if y > 0:
			array.append(int(matrix[x][y-1]))
		if y < self.height-1:
			array.append(int(matrix[x][y+1]))
		return array

	def astar_adj_matrix_elements(self, element):
		'''
		Generates all adjacent elements that are walkable (no pit, no wumpus) to a matrix element (up,down,left,right)		
		'''
		array = []
		x = element[0]
		y = element[1]
		if x > 0:
			# if there is no wumpus and there is no pit or just breeze then we are safe to move
			if (self.wumpus_board[x-1,y] == 0 or self.wumpus_board[x-1,y] == 3) and self.pit_board[x-1,y] == 0 or self.pit_board[x-1,y] == 3:
				array.append((x-1,y))
		if x < self.length-1:
			if (self.wumpus_board[x+1,y] == 0 or self.wumpus_board[x+1,y] == 3) and self.pit_board[x+1,y] == 0 or self.pit_board[x+1,y] == 3:
				array.append((x+1,y))
		if y > 0:
			if (self.wumpus_board[x,y-1] == 0 or self.wumpus_board[x,y-1] == 3) and self.pit_board[x,y-1] == 0 or self.pit_board[x,y-1] == 3:
				array.append((x,y-1))
		if y < self.height-1:
			if (self.wumpus_board[x,y+1] == 0 or self.wumpus_board[x,y+1] == 3) and self.pit_board[x,y+1] == 0 or self.pit_board[x,y+1] == 3:
				array.append((x,y+1))
		return array

	def percept(self):
		'''
		Agent percepting effects in the room he's at
		'''
		x, y = self.agent.get_position()
		room = self.board[x][y]

		# percepting gold and glitter
		if room.get_glitter():
			self.agent.set_glitter(True)
			self.agent.glitter = True
			print("I sense glitter!")

		# percepting breeze
		if room.get_breeze():
			self.agent.breeze = True
			print("I sense a breeze!")

		# percepting pit
		if room.get_pit():
			self.agent.is_alive = False
			self.game_over = True
			self.game_won = False
			print("I've fallen in a pit!")

		# percepting stench
		if room.get_stench():
			self.agent.stench = True
			print("I sense stench!")

		# percepting wumpus
		if room.get_wumpus():
			self.agent.is_alive = False
			self.game_over = True
			self.game_won = False
			print("Wumpus got me!")

		# percepting exit
		if room.get_exit() and self.agent.get_has_gold():
			self.agent.exit = True
			print("I'm at the exit!")

	def kb(self, wumpus_board, pit_board):
		'''
		Updating wumpus and pit board based on percepts from the current room
		'''
		x, y = self.agent.get_position()
		room = self.board[x][y]

		# percepting breeze
		if room.get_breeze():
			self.pit_board[x][y] = 3
			if x > 0:
				self.pit_board[x-1][y] = min(2, self.pit_board[x-1][y])
			if x < self.length-1:
				self.pit_board[x+1][y] = min(2, self.pit_board[x+1][y])			
			if y > 0:
				self.pit_board[x][y-1] = min(2, self.pit_board[x][y-1])
			if y < self.height-1:
				self.pit_board[x][y+1] = min(2, self.pit_board[x][y+1])

		# percepting no breeze
		if room.get_breeze() == False:
			self.pit_board[x][y] = 0
			if x > 0:
				if self.pit_board[x-1][y] != 3:
					self.pit_board[x-1][y] = 0
			if x < self.length-1:
				if self.pit_board[x+1][y] != 3:
					self.pit_board[x+1][y] = 0		
			if y > 0:
				if self.pit_board[x][y-1] != 3:
					self.pit_board[x][y-1] = 0
			if y < self.height-1:
				if self.pit_board[x][y+1] != 3:
					self.pit_board[x][y+1] = 0

		# percepting stench
		if room.get_stench():
			self.wumpus_board[x][y] = 3
			
			# We have x from 1 to the length of the cave
			if x > 1:
				self.wumpus_board[x-1][y] = min(2, self.wumpus_board[x-1][y])
			if x < self.length-1:
				self.wumpus_board[x+1][y] = min(2, self.wumpus_board[x+1][y])				
			if y > 1:
				self.wumpus_board[x][y-1] = min(2, self.wumpus_board[x][y-1])
			if y < self.height-1:
				self.wumpus_board[x][y+1] = min(2, self.wumpus_board[x][y+1])

		# percepting no stench
		if room.get_stench() == False:
			self.wumpus_board[x][y] = 0
			
			# We have x from 1 to the length of the cave
			if x > 1:
				if self.wumpus_board[x-1][y] != 3:
					self.wumpus_board[x-1][y] = 0
			if x < self.length-1:
				if self.wumpus_board[x+1][y] != 3:
					self.wumpus_board[x+1][y] = 0				
			if y > 1:
				if self.wumpus_board[x][y-1] != 3:
					self.wumpus_board[x][y-1] = 0
			if y < self.height-1:
				if self.wumpus_board[x][y+1] != 3:
					self.wumpus_board[x][y+1] = 0

		return self.pit_board, self.wumpus_board

	def update_kb(self, wumpus_board, pit_board):
		'''
		Updating our KB's (wumpus and pit_board) with logic:
		
		If every room around breeze has no pit 100% then we know where the pit is

		If every room around stench has no wumpus 100% then we know where the wumpus is
		'''
		for x in range(self.length):
			for y in range(self.height):
				'''
				UPDATING THE PIT KB
				'''
				if pit_board[x][y] == 3:
					# Updating that there can't be a pit where there's a wumpus
					if x > 0 and wumpus_board[x-1][y] == 1:
						pit_board[x-1][y] = 0
					if x < self.length-1 and wumpus_board[x+1][y] == 1:
						pit_board[x+1][y] = 0
					if y > 0 and wumpus_board[x][y-1] == 1:
						pit_board[x][y-1] = 0
					if y < self.height-1 and wumpus_board[x][y+1] == 1:
						pit_board[x][y+1] = 0

					adjacent_breeze = np.array(self.adjacent_matrix_elements(pit_board, x, y))
					if 2 in adjacent_breeze:
						index_to_remove = np.where(adjacent_breeze == 2)[0][0]
						adjacent_no_pit = np.delete(adjacent_breeze, index_to_remove)

						if np.all(adjacent_no_pit == 0):
							if x > 0:
								if pit_board[x-1][y] == 2:
									pit_board[x-1][y] = 1
									print("We have a pit at ({0},{1})".format(x-1 + 1,y + 1))
							if x < self.length-1:
								if pit_board[x+1][y] == 2:
									pit_board[x+1][y] = 1
									print("We have a pit at ({0},{1})".format(x+1+ 1,y+ 1))
							if y > 0:
								if pit_board[x][y-1] == 2:
									pit_board[x][y-1] = 1
									print("We have a pit at ({0},{1})".format(x+ 1,y-1+ 1))
							if y < self.height-1:
								if pit_board[x][y+1] == 2:
									pit_board[x][y+1] = 1
									print("We have a pit at ({0},{1})".format(x+ 1,y+1+ 1))

				if wumpus_board[x][y] == 3:
					'''
					UPDATING THE WUMPUS KB
					'''

					# Updating that there can't be wumpus where there's a pit
					if x > 0 and pit_board[x-1][y] == 1:
						wumpus_board[x-1][y] = 0
					if x < self.length-1 and pit_board[x+1][y] == 1:
						wumpus_board[x+1][y] = 0
					if y > 0 and pit_board[x][y-1] == 1:
						wumpus_board[x][y-1] = 0
					if y < self.height-1 and pit_board[x][y+1] == 1:
						wumpus_board[x][y+1] = 0

					adjacent_stench = np.array(self.adjacent_matrix_elements(wumpus_board, x, y))
					if 2 in adjacent_stench:
						index_to_remove = np.where(adjacent_stench == 2)[0][0]
						adjacent_no_wumpus = np.delete(adjacent_stench, index_to_remove)

						if np.all(adjacent_no_wumpus == 0):
							if x > 0:
								if wumpus_board[x-1][y] == 2:
									wumpus_board[x-1][y] = 1
									print("We have a wumpus at ({0},{1})".format(x-1+ 1,y+ 1))
							if x < self.length-1:
								if wumpus_board[x+1][y] == 2:
									wumpus_board[x+1][y] = 1
									print("We have a wumpus at ({0},{1})".format(x+1+ 1,y+ 1))
							if y > 0:
								if wumpus_board[x][y-1] == 2:
									wumpus_board[x][y-1] = 1
									print("We have a wumpus at ({0},{1})".format(x+ 1,y-1+ 1))
							if y < self.height-1:
								if wumpus_board[x][y+1] == 2:
									wumpus_board[x][y+1] = 1
									print("We have a wumpus at ({0},{1})".format(x+ 1,y+1+ 1))

	def update_visited_rooms(self, visited_rooms):
		'''
		Updates our visited rooms matrix when we change positions
		'''
		x, y = self.agent.get_position()
		visited_rooms[x][y] = 2
		if x > 0:
			visited_rooms[x-1][y] = max(visited_rooms[x-1][y],1)
		if x < self.length-1:
			visited_rooms[x+1][y] = max(visited_rooms[x+1][y],1)
		if y > 0:
			visited_rooms[x][y-1] = max(visited_rooms[x][y-1],1)
		if y < self.height-1:
			visited_rooms[x][y+1] = max(visited_rooms[x][y+1],1)
		return visited_rooms

	def calculate_manhattan_distance(self, x1, y1, x2, y2):
		'''
		Calculates manhattan distance between two points (x1,y1) and (x2,y2)
		'''
		self.result = abs(x1-x2) + abs(y1-y2)
		return self.result

	def find_nearest_safe_room(self, visited_rooms, wumpus_board, pit_board):
		'''
		Finds nearest room (by manhattan distance) that we have not visited and that is safe 
		'''
		self.index_locations_we_can_visit = []
		self.all_distances = []
		x, y = self.agent.get_position()
		for i in range(len(visited_rooms)):
			for j in range(len(visited_rooms[0])):
				if visited_rooms[i][j] == 1 and (wumpus_board[i][j] == 0 or wumpus_board[i][j] == 3) and (pit_board[i][j] == 0 or pit_board[i][j] == 3):
					self.index_locations_we_can_visit.append((i,j))
					self.all_distances.append(self.calculate_manhattan_distance(x,y,i,j))

		# there are no rooms we can visit or we need to shoot our arrow
		if len(self.index_locations_we_can_visit) == 0:
			return self.try_and_shoot(visited_rooms,wumpus_board,pit_board)
		# if there is only one location we can visit, go there
		elif len(self.index_locations_we_can_visit) == 1:
			return self.index_locations_we_can_visit[0][0], self.index_locations_we_can_visit[0][1]
		else:
			# If there are more locations we can visit, go to the one with the least cost
			self.location = self.index_locations_we_can_visit[self.all_distances.index(min(self.all_distances))]
			return self.location[0],self.location[1]

	def find_nearest_wumpus_room(self, visited_rooms, wumpus_board, pit_board):
		'''
		Finding the nearest room by manhattan distance, that has stench
		'''
		self.index_locations_we_can_visit = []
		self.all_distances = []
		x, y = self.agent.get_position()
		# print(wumpus_board)
		# print(pit_board)
		for i in range(len(visited_rooms)):
			for j in range(len(visited_rooms[0])):
				if wumpus_board[i][j] == 3 and (pit_board[i][j] == 0 or pit_board[i][j] == 3):
					self.index_locations_we_can_visit.append((i,j))
					self.all_distances.append(self.calculate_manhattan_distance(x,y,i,j))

		# There is no location where we have stench and no pit (we have only pits around us)
		if len(self.index_locations_we_can_visit) == 0:
			return None
		# There is only one location where we have stench and no pit
		if len(self.index_locations_we_can_visit) == 1:
			return self.index_locations_we_can_visit[0][0], self.index_locations_we_can_visit[0][1]
		else:
			self.location = self.index_locations_we_can_visit[self.all_distances.index(min(self.all_distances))]
			return self.location[0],self.location[1]

	def point_towards_wumpus(self, visited_rooms, wumpus_board, pit_board):
		'''
		Points towards a room with a wumpus.
		If there is no wumpus in that room for sure, it aims towards a stench-emitting room
		'''	
		x, y = self.agent.get_position()

		if x > 0 and wumpus_board[x-1][y] == 1:
			self.change_facing_towards((x-1,y))
		if x < self.length-1 and wumpus_board[x+1][y] == 1:
			self.change_facing_towards((x+1,y))
		if y > 0 and wumpus_board[x][y-1] == 1:
			self.change_facing_towards((x,y-1))
		if y < self.height-1 and wumpus_board[x][y+1] == 1:
			self.change_facing_towards((x,y+1))
		
	def try_and_shoot(self, visited_rooms, wumpus_board, pit_board):
		'''
		If there is nowhere to go, we go to stench-room and shoot the wumpus
		'''
		
		# Testing if we killed the wumpus to know if to shoot the arrow
		if self.wumpus_dead == True:
			return None

		# Otherwise shoot an arrow
		x, y = self.agent.get_position()
		nearest_wumpus_room = self.find_nearest_wumpus_room(visited_rooms, wumpus_board, pit_board)
		if nearest_wumpus_room == None:
			return None
		route_to_wumpus_room = self.a_star_function((x,y), nearest_wumpus_room)
		
		for room in route_to_wumpus_room[1:]:
			self.move_towards(room)
			self.percept()
			self.kb(wumpus_board, pit_board)
			self.update_kb(wumpus_board, pit_board)
			self.update_visited_rooms(visited_rooms)
		
		self.point_towards_wumpus(visited_rooms, wumpus_board, pit_board)
		self.shoot_arrow()
		self.kb(wumpus_board, pit_board)
		self.update_kb(wumpus_board, pit_board)
		self.update_visited_rooms(visited_rooms)
		return self.find_nearest_safe_room(visited_rooms, wumpus_board, pit_board)

	def interact(self):
		'''
		Interacts with the room - picking up gold
		'''
		x, y = self.agent.get_position()
		if self.board[x][y].has_gold:
			self.board[x][y].set_gold(False)
			self.board[x][y].set_glitter(False)
			self.agent.set_has_gold(True)
			self.agent.set_glitter(False)
			self.agent.has_gold = True
			self.agent.glitter = False
			self.agent.set_score(self.agent.get_score() + GOLD_REWARD)
			print("The agent picked up gold!")
		else:
			print("There is no gold here!")
	
	def kill_wumpus(self, x, y):
		'''
		What happens when we kill wumpus
		'''
		if self.board[x][y].get_wumpus():
			self.board[x][y].set_wumpus(False)
			self.wumpus_dead = True
			self.agent.set_scream(True)
			self.agent.set_score(self.agent.get_score() + WUMPUS_REWARD)
			print("Wumpus is dead!")

			# Updating so that there is no pit where the wumpus was
			self.pit_board[x][y] = 0

			# Removing stench from the board and the wumpus kb
			if x > 1:
				self.board[x-1][y].set_stench(False)
				self.wumpus_board[x-1][y] == 0
			if x < self.length-1:
				self.board[x+1][y].set_stench(False)
				self.wumpus_board[x+1][y] == 0					
			if y > 1:
				self.board[x][y-1].set_stench(False)
				self.wumpus_board[x][y-1] == 0
			if y < self.height-1:
				self.board[x][y+1].set_stench(False)
				self.wumpus_board[x][y+1] == 0

	def shoot_arrow(self):
		''' 
		Shooting the arrow
		'''
		x, y = self.agent.get_position()
		facing = self.agent.get_facing()
		self.agent.set_has_arrow(False)
		print("I'm shooting an arrow!")

		arrow_rooms = []

		# getting all rooms the arrow visits
		if facing == "up":
			for i in range(y,self.height):
				arrow_rooms.append((x,i))
		if facing == "down":
			for i in range(y,-1,-1):
				arrow_rooms.append((x,i))
		if facing == "right":
			for i in range(x,self.length):
				arrow_rooms.append((i,y))
		if facing == "left":
			for i in range(x,-1,-1):
				arrow_rooms.append((i,y))

		# checking if it kills the wumpus
		for room in arrow_rooms:
			# print("Arrow passes by ({},{})".format(room[0],room[1]))
			if self.board[room[0]][room[1]].get_wumpus():
				self.kill_wumpus(room[0], room[1])

		if self.wumpus_dead == False:
			print("The arrow hit the wall, wumpus is still alive!")

	def h(self, start_node, end_node):
		'''
		H is defined as the heuristic value of a nodes distance from the end node
		The heuristic used is the manhattan distance
		'''
		# x, y = self.agent.get_position()
		# print((x,y))
		# print(start_node)
		# print(end_node)
		result = abs(start_node[0] - end_node[0]) + abs(start_node[1] - end_node[1])
		return result

	def a_star_function(self, start_node, end_node):
		'''
		Runs the a_star algorithm in order to find the optimal path from the start node to the end node, 
		the heuristic used is the manhattan distance.

		The main code for the function is taken from: https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/a-star-search-algorithm/
		The code has been modified to suit the problem we have in hand.

		'''
		open_list = set([start_node])
		closed_list = set()
		node = None

		# g contains current distances from start_node to all other nodes
		g = {}
		g[start_node] = 0


		# parents contains an adjacency map of all nodes
		parents = {}
		parents[start_node] = start_node

        # h is the manhattan distance
		while len(open_list) > 0:
			node = None
			# selecting the minimum f = g + h value node from the open list
			for vertex in open_list:
				if node == None or g[vertex] + self.h(vertex, end_node) < g[node] + self.h(node, end_node):
					node = vertex

			# if node is end node
			if node == end_node:
				path = []
				while parents[node] != node:
					path.append(node)
					node = parents[node]

				path.append(start_node)

				path.reverse()

				print_path = [(x + 1, y + 1) for x, y in path]

				print('Path found: {}'.format(print_path))
				return path

            # Looking at adjacent nodes/rooms
			adjacent_elements = self.astar_adj_matrix_elements(node)

			for element in adjacent_elements:
				#estimated cost from current to end node 
				weight = self.h(element, end_node)
				if element not in closed_list and element not in open_list:
					open_list.add(element)
					parents[element] = node
					g[element] = g[node] + weight


				elif g[element] > g[node] + weight:
					parents[element] = node
					if element in closed_list:
						closed_list.remove(element)
						open_list.add(element)

			# remove node from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
			open_list.remove(node)
			closed_list.add(node)

		print("Path does not exist")
		return None

	def change_facing_towards(self, next_room):
		'''
		We change the direction we're facing to the next room
		'''
		x1, y1 = self.agent.get_position()
		x2, y2 = next_room
		facing = self.agent.get_facing()

		# The agent needs to face right
		if x2>x1:
			if facing == "down":
				self.change_facing_ccwise()
			elif facing == "left":
				self.change_facing_cwise()
				self.change_facing_cwise()
			elif facing == "right":
				pass
			else:
				self.change_facing_cwise()

		# The agent needs to face left
		elif x2<x1:
			if facing == "up":
				self.change_facing_ccwise()
			elif facing == "right":
				self.change_facing_cwise()				
				self.change_facing_cwise()
			elif facing == "left":
				pass
			else:
				self.change_facing_cwise()

		# The agent needs to face up
		elif y2>y1:
			if facing == "right":
				self.change_facing_ccwise()
			elif facing == "down":
				self.change_facing_cwise()
				self.change_facing_cwise()
			elif facing == "up":
				pass
			else:
				self.change_facing_cwise()
		# The agent needs to face down
		elif y2<y1:
			if facing == "left":
				self.change_facing_ccwise()
			elif facing == "up":
				self.change_facing_cwise()
				self.change_facing_cwise()
			elif facing == "down":
				pass
			else: 
				self.change_facing_cwise()

	def move_towards(self, next_room):
		'''
		Moves agent from the position he's at to the next node (fixing the direction so that he's facing correctly)
		It also checks so that the agent doesn't turn around 3 times, only turning the smallest amount necessary
		'''
		self.change_facing_towards(next_room)
		# When you have the correct facing, move towards that direction
		self.move_forward()

	def play_game(self):
		'''
		Main function for playing the game
		'''
		# Initializing all boards
		data = self.read_game_data()
		xboard = self.create_board(data)
		board = self.fill_board(xboard)
		wumpus_board = self.generate_wumpus_kb()
		pit_board = self.generate_pit_kb()
		visited_rooms = self.generate_visited_rooms()

		# Updating the KB
		self.percept()
		self.kb(wumpus_board, pit_board)
		self.update_kb(wumpus_board, pit_board)
		self.update_visited_rooms(visited_rooms)

		#Saying where we are at the start
		x, y = self.agent.get_position()
		print("I'm starting from ({0},{1})".format(x + 1,y + 1))

		# Making the first move, always moving one to the right, and updating the KB
		self.move_forward()
		self.percept()
		self.kb(wumpus_board, pit_board)
		self.update_kb(wumpus_board, pit_board)
		self.update_visited_rooms(visited_rooms)

		# Main while loop
		while self.game_over == False:
			
			nearest_safe_room = self.find_nearest_safe_room(visited_rooms, wumpus_board, pit_board)
			x, y = self.agent.get_position()

			# If there is no safe path to take, just go home
			if nearest_safe_room == None and self.agent.has_gold == False:
				print("I'd rather go home, there are only pits around me, and it's not worth it to jump!")
				route_back_home = self.a_star_function((x,y), self.exit) 
				for room in route_back_home[1:]:
					self.move_towards(room)
					self.percept()
					self.kb(wumpus_board, pit_board)
					self.update_kb(wumpus_board, pit_board)
					self.update_visited_rooms(visited_rooms)
				print("I have exited the cave but didn't find any gold :(")				
				print("My path was: {}".format(self.trace))
				break
			
			# If you get gold and have searched as much as you can of the world, go back home
			if nearest_safe_room == None and self.agent.has_gold == True:
				print("I have searched everything i can, i'm going home!")
				route_back_home = self.a_star_function((x,y),self.exit) 
				for room in route_back_home[1:]:
					self.move_towards(room)
					self.percept()
					self.kb(wumpus_board, pit_board)
					self.update_kb(wumpus_board, pit_board)
					self.update_visited_rooms(visited_rooms)
				print("I have exited the cave with the gold!")
				print("My path was: {}".format(self.trace))
				break

			# finding the route to the nearest safe room
			route_to_safe_room = self.a_star_function((x,y), nearest_safe_room)

			# If there is a safe path to take, move there
			for room in route_to_safe_room[1:]:
				self.move_towards(room)
				self.percept()
				# print(my_game.agent.glitter == True)
				if self.agent.glitter == True:
					self.interact()
				self.kb(wumpus_board, pit_board)
				self.update_kb(wumpus_board, pit_board)
				self.update_visited_rooms(visited_rooms)

		