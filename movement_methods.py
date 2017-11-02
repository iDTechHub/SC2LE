from pysc2.agents import base_agent

from pysc2.lib import features
from pysc2.lib import actions

_SELECT_ARMY = actions.FUNCTIONS.select_army.id

_SELECT_ALL = [0]
_SCREEN = [0]

_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id 

class ScriptedTechBot(base_agent.BaseAgent):

    def step(self, obs):
        super(ScriptedTechBot, self).step(obs)
        
        if _MOVE_SCREEN in obs.observation["available_actions"]:
            
            # Pick a point between [0,0] and [83,83]
            # [2, 4] is a point at the top left of the screen.
            point = [2,4]
         	
         	# Make a movement on the screen and set the point var
         	# from above as the target location.
            return actions.FunctionCall(_MOVE_SCREEN, [[0], point])
            
        else:
            return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])
