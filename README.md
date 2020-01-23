# ATTACK ON STRONGHOLD

### OBJECTIVES
Attack on Stronghold is a single-player roguelike game where the goal is to go through multiple layers of a dungeon, defeating monsters, and beating the final boss without dying. A tutorial world will instruct the player how to interact with the game world. Each of the 4 levels, including the final boss stage, will introduce players to different enemy types.  A death in any of the levels will end the run of the game but the player's health does reset after each stage. The final objective is to defeat the final boss and escape the dungeon. 


### GAMEPLAY INSTRUCTIONS

#### CONTROLS
Player will move the character around the screen using the arrow keys. A short attack will be made by the character when pressing space and it is possible to spam the attack with no cooldown

#### MECHANICS

##### Player
The player's character has 100 health, which will reset after each completed stage. The attack of the character will deal 10 damage to all enemies, and has a limted range. The speed of the character allows it to outrun all enemies execpt for the slime, which is equal. 

##### Environmental Obstacles
Throughout each stage, there will be 3 distinct obstacles on the map. The border of the map itself is made up of a wall tile that the player cannot pass through. Additionaly, there will be wooden post tiles in the map that will also not allow the player to go through. These direct the flow of the combat and the enemy's pathfinding. Finally, each level has pools of lava around the map, that when the player steps in it, a constant rate of damage will hit the player. Enemies will treat the lava as a wall and will therefore not walk through it.

##### Enemy Types
There are 3 main enemy types in Attack on Stronghold, the Slime, Executioner, and Mage.

* Mage: A non moving enemy and always faces toward the player. Attack is a ranged fireball which deals 10 damage and has a cooldown of 1 second after the fireball is either destroyed by the player attack or it hits a wall. Cannot be killed.

* Executioner: A slow moving enemy and always moves towards the player. Attack is a heavy hitting axe slash which deals 3 damage on hit. Each attack has a 2 second cooldown

* Slime: A fast moving enemy which always chases the player. Attack is a light melee attack when the smile is in contact with the player. Attack deals 1 damage but has no cooldown.


### SCORING
There is no formal scoring system in Attack on Stronghold. The success of a game is determined by how far does the player progress through the stages. On the event that the player dies, the game ends and the player must start from the begining. The difficulty of each stage increases as the player progresses. Each game either ends with a completion or failure. 


### FUNCTIONALITY AND LIMITATIONS
The Arcade library, while useful, has several limitations. Due to how the sprite class works, detailed movement animations cannot be made if collision is to work properly. Addititonally, due to Python's slower execution time, not to many animated sprites can be put on the screen. Rapid key presses or jitter movements will overload Arcade's built-in user input module and cause glitches. Arcade has no built in timer so some elements need to be sequenced manually.
