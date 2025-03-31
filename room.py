# Defining Rooms

class Room:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.has_agent = False
		self.has_wumpus = False
		# self.maybe_wumpus = False
		self.has_stench = False
		self.has_pit = False
		# self.maybe_pit = False
		self.has_breeze = False
		self.has_gold = False
		self.has_glitter = False
		self.has_exit = False

	def properties(self):
		return {
			"x": self.x,
			"y": self.y,
			"has_agent": self.has_agent,
			"has_wumpus": self.has_wumpus,
			"has_stench": self.has_stench,
			"has_pit": self.has_pit,
            "has_breeze": self.has_breeze,
			"has_gold": self.has_gold,
			"has_glitter": self.has_glitter,
			"has_exit": self.has_exit
		}

	# Agent
	def set_agent(self, agent):
		self.has_agent = agent

	def get_agent(self):
		return self.has_agent

    # Wumpus
	def set_wumpus(self, wumpus):
		self.has_wumpus = wumpus

	def get_wumpus(self):
		return self.has_wumpus

    # Stench
	def set_stench(self, stench):
		self.has_stench = stench

	def get_stench(self):
		return self.has_stench

    # Pit
	def set_pit(self, pit):
		self.has_pit = pit

	def get_pit(self):
		return self.has_pit

    # Breeze
	def set_breeze(self, breeze):
		self.has_breeze = breeze

	def get_breeze(self):
		return self.has_breeze

    # Gold
	def set_gold(self, gold):
		self.has_gold = gold

	def get_gold(self):
		return self.has_gold

    # Glitter
	def set_glitter(self, glitter):
		self.has_glitter = glitter

	def get_glitter(self):
		return self.has_glitter

	# Exit
	def set_exit(self, exit):
		self.has_exit = exit

	def get_exit(self):
		return self.has_exit
