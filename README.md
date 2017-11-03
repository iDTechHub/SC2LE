# SC2LE
Work, notes, and code for the upcoming SC2 ML and AI conference.
####1) Download Stuff

To get started you'll need to get files from a couple of different locations.

• [Starcraft 2 Linux Edition, and Ladder Maps](https://github.com/Blizzard/s2client-proto#downloads)

• [PySC2, and Mini Games](https://github.com/deepmind/pysc2)

• [Numpy](http://www.numpy.org/) (I like [Anaconda](https://www.anaconda.com/download/))


----------

####2) Test an Agent
After you have the requisite files you'll want to run a test agent to ensure everything was installed correctly. To test a random agent type the following in your terminal:

 - `python -m pysc2.bin.agent --map Simple64`

You can also test the game and system yourself by running:

- `python -m pysc2.bin.play --map Simple64`

----------

####3) Create a New Map

You can download the CollectMinShards from this GitHub account, or use your own if you have it. 

After downloading or creating your map, 

- Add it to your /Maps folder

Then you'll want to go into your pysc2/maps/mini_games.py file and add your map name to the array. If you used the CollectMinShards map from this GitHub and added it to the end of the list it should look like:

![alt text](https://github.com/iDTechHub/SC2LE/blob/master/Images/sc2conf_006a_maparray.png "map array")

Note: | 
--- | --- | ---
*If you're adding and editing new maps, you'll want to clone or download from git, and then run setup.py to get your new map files in.* | 


----------

####4) Create a no_op script
To create a bot that doesn't do anything, start by importing pysc2 libraries, and create a class that inherits from base_agent. Then 

![alt text](https://github.com/iDTechHub/SC2LE/blob/master/Images/sc2conf_008_noop_v2.PNG "no_op bot code")

- See the no_op.py file on this GitHub.


----------


####5) Run Your Script 


After you have the script, to test it and see it in action, call pysc2.bin.agent, but use your own filename.classname at the end. If you used the no_op file here you would run the following:

- `python -m pysc2.bin.agent --map CollectMinShards --agent no_op.ScriptedTechBot`

----------

####6) Move_screen in available actions

![alt text](https://github.com/iDTechHub/SC2LE/blob/master/Images/sc2conf_010_availactions.png "Available Actions")

_MOVE_SCREEN refers to movement that's happening on the screen, opposed to the minimap. It's not related to moving the camera. You can find more information about the Move_screen functions in the [actions](https://github.com/deepmind/pysc2/blob/master/pysc2/lib/actions.py) section of PYSC2 GitHub.

When you check:

- `if _MOVE_SCREEN in obs.observation["available_actions"]:`

You're essentially checking if you have a movable unit selected. If you don't have a unit selected, then a move (on the screen) command won't be available.

----------

9) Select an Army/Unit/Point

The easiest and quickest way to select a unit is to just select your entire army of units. For this you can add the following constants and function call.

- `_SELECT_ARMY = actions.FUNCTIONS.select_army.id`

- `_SELECT_ALL = [0]`

- `return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])`


Note: | 
--- | --- | ---
*You can see the full code for selecting an army. A good exercise would be to see if you can look through [actions.py](https://github.com/deepmind/pysc2/blob/master/pysc2/lib/actions.py) and figure out how to implement select_rect* | 

----------

10) Move the Army/Unit/Point

To move your selection you can specify a point and move them to that target point. Points can be made as a list so `point = [2,4]` would be a point on the top-left of the screen.

Then to move your army, or selected units, to that point you'd type:

- `return actions.FunctionCall(_MOVE_SCREEN, [[0], point])`

There's a very bare-bones example of this functionality in the  [movement_methods](https://github.com/iDTechHub/SC2LE/blob/master/movement_methods.py) file. Then for a more advanced version you can also reference the [scripted agent](https://github.com/deepmind/pysc2/blob/master/pysc2/agents/scripted_agent.py) from the PYSC2 GitHub.

Note: | 
--- | --- | ---
*You provide points to actions like in the Move_screen function in (x, y) format. However, when you get positions like in the code `neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()` from the scripted agent, you get image data in the (y, x) format.* | 

###Completed Part 1!

----------
