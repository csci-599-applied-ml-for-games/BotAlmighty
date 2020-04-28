# CSCI 599 : Machine Learning for Games Project 

### Project name : Dynamic level Generation of Games
### Team Name : BotAlmighty

<h2>Team Members</h2>
Pavleen Kaur<br>
Pritish Rawal<br>
Shashank Misra<br>
Tridha Chaudhuri<br>

<h3>Overview of the Project</h3>
Games tend to get boring for the players when they are too easy. On the other hand, it can get too frustrating when it’s too hard. Games with the greatest entertainment value are those in which the level matches the skills of the human player. This means that one of the core elements of good game design is to make the game just as difficult as it has to be, so that the player feels challenged enough, but not too much. Moreover, manually creating maps for games is expensive and time-consuming. Delegating map generation to an algorithmic process can save developers time and money, or even allow novel forms of gameplay.     <br>
The goal for our CSCI-599 project is exactly that. To take a childhood game such as Mario, and bring it back to our lives by introducing levels that are interesting, intriguing, and dynamically difficult by automating map generation for levels. 

<h3>About the Repository</h3>
This repository consists of all the code we have used in this project. Since we utilised 3 different models to generate levels, namely RNN, PCG and Markov, one can find the code for all the algorithms in their respective directories.<br>
The Output folder consists of the generated levels from each of the models, which is further converted to JSON files that are finally used by the bot that resides within the PCG model.
The bot uses the A* approach to learn various ways of playing the level in order to reach the end, thereby validating the testability of the created level.
