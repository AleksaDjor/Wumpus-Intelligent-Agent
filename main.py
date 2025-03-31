# Importing the game
from game import Game

# Setting the path to the wumpus_world.txt file
path_to_file = "C:/Programiranje/wumpus/wumpus_world_1.txt"

# path_to_file = "C:/Programiranje/wumpus/wumpus_world_2.txt"

# path_to_file = "C:/Programiranje/wumpus/wumpus_world_3.txt"

# path_to_file = "C:/Programiranje/wumpus/wumpus_world_4.txt"

# Initializing the game
my_game = Game(path_to_file)

# Playing the game
my_game.play_game()
