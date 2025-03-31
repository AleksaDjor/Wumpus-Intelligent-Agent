# Defining the agent/player

class Agent:
    '''Properties of the Agent/Player'''

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_alive = True
        self.has_arrow = True
        self.facing = "right"
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.has_gold = False
        self.bump = False
        self.scream = False
        self.score = 1000

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    # Which direction the agent is facing
    def set_facing(self, facing):
        self.facing = facing
    
    def get_facing(self):
        return self.facing

    # Player Arrow
    def set_has_arrow(self, has_arrow):
        self.has_arrow = has_arrow

    def get_has_arrow(self):
        return self.has_arrow

    # Player Gold
    def set_has_gold(self, has_gold):
        self.has_gold = has_gold

    def get_has_gold(self):
        return self.has_gold

    # Player glitter
    def set_glitter(self, glitter):
        self.glitter = glitter

    def get_glitter(self):
        return self.glitter

    # Player being alive
    def get_is_alive(self):
        return self.is_alive

    def set_is_alive(self, alive):
        self.is_alive = is_alive

    # Player Score
    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    # Scream
    def get_scream(self):
        return self.scream

    def set_scream(self, scream):
        self.scream = scream

    def percept(self):
        pass
