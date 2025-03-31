# Wumpus-Intelligent-Agent
An implementation of the Wumpus world with an intelligent agent. 

Made in: August 2023

## Installing and running the program

The assignment is done in Python 3.11.3 using two additional packages "numpy" and "pandas".

Both can be installed by using the pip installer, in Windows it is done as such, by running: "pip install numpy" and "pip install pandas" in the command prompt.

In order for the wumpus worlds to load correctly, in the file main.py the path to the wumpus_world_1 file (as well as wumpus_world_2, wumpus_world_3 and wumpus_world_4 - different examples of the Wumpus game) needs to be corrected with the variable path_to_file. 

After installing the packages and correcting the path to the wumpus_world files, the program can be started by running the main.py file with any python compiler.

In short:
1. Install Python
2. Install packages numpy and pandas 
3. Change the path to wumpus_world.txt files with variable path_to_file in main.py
4. Compile main.py with Python

## Description of the problem

In this assignment you'll need to implement a variant of the »Wumpus world« game (see: AIMA3e book, chapter 7.2, pp. 236 - 240). The goal of the game is to »safely« traverse the cave and exit with a maximal number of points. The definition of the »Wumpus world« game is the same as that from the book with the following corrections:

The gold is not just one, but there can be many of it scattered on different places of the cave;
The size of the cave is M x N, where M, N, the position of pits, gold and the Wumpus are given in advance in the form of a text file; 
(wumpus_world.txt - the exact format is given later on);
The price of shooting the (only) arrow is -100 points;
The start position of the agent is facing right.
Your assignment is to:

Implement a »smart« agent capable of navigating the cave, avoiding pits and the Wumpus, picking up as much gold as possible (or maximise the number of points), and reach the exit point of the cave - field (x,y) that is defined in advance as the goal field. Agent's input should be the text file wumpus_world.txt. The output should be the »trace« of the agent together with all logical entailments for every move of the agent;

Generate test worlds (at least three) - files »wumpus_world.txt« - that will serve as the input for the agent;

Write a report describing your solution. The report should include: the description of the methods that you tested (can be in pseudocode), the description of the first order logic part of the agent's reasoning, the description of problems that you encountered during the process of implementing your solutions. You'll implement the agent as a hybrid algorithm that integrates logical induction, search and background knowledge (knowledge base). You have to take into consideration the following constraints:

Your agent has to integrate with some knowledge base.
You need to implement a search algorithm (A* or some other search algorithm) to plan a route to a given field and interface it to the agent;
Your agent can read the whole cave map at once, but must not »see« fields, that it didn't yet visit - e.g. it should not know that there's gold on the field (2,3) until it visits that field. The only exceptions are the labels Mxy, Axy and GOxy - see below for »label meaning«. To be sure your agents doesn't »peep«, you'll have to output every move that the agent makes, e.g.:

- Move to field (2,1)
- Breeze sensed
- Move to field (1,1)
- Move to field (1,2)
- Smell sensed
- Found out Wumpus is on field (1,3)
- Found out pit is on field (3,1)
- Move to field (2,2)
- Representation of the Wumpus world:

Example of the wumpus_world.txt file:

- A11

- B21

- P31

- B41

- S12

- B32

- W13

- S23

- G23

- B23

- P33

- B43

- S14

- B34

- P44

- M44

- GO11

Meaning of labels in the above example:
- Axy  = Agent is on the field (x,y)

- Bxy  = The field (x,y) is breezy

- Gxy  = There's gold on the field (x,y)

- GOxy = (x,y) is the goal field - exit from the cave

- Mxy  = The cave is x fields wide and y fields high (map size)

- Pxy  = There's a pit on the field (x,y)

- Sxy  = The field (x,y) is smelly

- Wxy  = There's the Wumpus on the field (x,y)

Example of the Wumpus world (wumpus world 1):

![wumpus](https://github.com/user-attachments/assets/5e2bcf7d-c6e1-43d7-bff7-c311b5d1f46a)

## Programming the Wumpus world

### Initialization

In this assignment we assume the reader is already well informed about what is the Wumpus world and what are its properties/characteristics.

The Wumpus world itself has been programmed by using three classes:

- Room class - forming rooms, elements with properties such as the rooms position, whether the room has the agent/Wumpus/glitter/gold/breeze/pit etc.  and all other possible changes and states to one room/cell in the game. The class has set and get functions for each of those properties.

- Agent class - forming the agent/player, stating all possible properties of the agent, whether he has picked up gold, whether he has shot his arrow, whether he is alive, etc. The class has set and get functions for each of those properties.

- Game class - the main class with all of the "physics" of the game - stored in the class methods. It has also properties to know whether the game is over, whether the game has been won by the agent, whether the Wumpus is dead, what is the trace of the player, etc. all stating properties of the game in hand.   

After getting all of the data from the .txt file and making the wumpus world, we pass on to the logic of the world.

### The logic of the Wumpus world

The output of the Wumpus world is a trace of all visited rooms, alongside all of the percepts of the agent from the rooms it visits and the logic with figuring out where the obstacles (wumpus, pit) are.

The main knowledge base (KB) of the agent consists of three matrices, wumpus_board, pit_board and visited_rooms. 
Each of these matrices has values presented below, for example, for the wumpus/pit board we have: 

- 0 - The room doesn't have a wumpus/pit
- 1 - The room has a wumpus/pit
- 2 - The room maybe has a wumpus/pit
- 3 - The room has stench/breeze
- 4 - There is no info about the room

And for the visited\_rooms we have 	

- 0 - The room has not been visited and we are not sure if it can be visited
- 1 - The room can be visited but is not visited yet
- 2 - The room has been visited

Therefore, using those KB's, the algorithm of the Wumpus world is: see what is the nearest room we didn't visit that has no wumpus or pit in it, find the path to that room using A*, percept information from that room (check also if we feel glitter so we know to pick up gold), update our KB's and repeat finding the next safe room.

The problem comes when we have reached every room available and we have to kill Wumpus in order to move on. We have done this in this way as to obtain as much information as we can before shooting the arrow. After killing Wumpus the algorithm keeps on with updating the KB's and finding safe rooms until there are no more safe rooms available - when the agent goes back home. 

The logic that is programmed that updates our KB's is inside of the "kb" and "update_kb" functions and is as such:

- If we feel no breeze/no stench, all of the surrounding rooms have no pit/Wumpus.
- If we feel breeze/stench, the surrounding rooms have a value of the minimum of the current value of the room (as we don't want to replace our knowledge that there is or there is no pit/Wumpus in that room) and 2 (there is maybe a pit/Wumpus in that location).
- If every room around the breeze/stench has no pit/Wumpus (value 0), then the pit/Wumpus must be in the only unexplored room around the breeze/stench.
- Where there's a pit/Wumpus, there can't be a Wumpus/pit.

### The problems we encountered

The biggest problem was the case where there are actually several golds in the map. Therefore, in order to solve the problem of several golds, I have removed what I initially thought was useful, scoring the agent, so now the agent roams around the map as much as he can as every unexplored reachable room has a chance that it has gold in it (therefore increasing our "score"). This changes the initial algorithm quite a bit, making not just reaching the gold and safely going out as the main goal of the agent, but making the main goal to explore as much territory as possible.

A big problem also is overcomplicating the code. I realized too late that instead of making all of those individual KB's for Wumpus, pits and visited rooms, I could've made just another variable called the agent_board, a copy of a normal MxN board, which has information about the rooms only from the agents percepts. That would cut down a lot on the code and all of the unnecessary matrix manipulations done in it and it would simplify the KB of the agent as well.
