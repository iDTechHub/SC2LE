from pysc2.agents import base_agent

from pysc2.lib import features
from pysc2.lib import actions

_NO_OP = actions.FUNCTIONS.no_op.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id

_SELECT_ALL = [0]
_SELECT = [0]

# Reference https://github.com/deepmind/pysc2/blob/master/pysc2/lib/actions.py
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id 

_SELECT_POINT = 2 #writing: actions.FUNCTIONS.select_point.id # would be more sensible
_TERRAN_MARINE = 48
_ZERG_ZERGLING = 105

class ScriptedTechBot(base_agent.BaseAgent):

    def step(self, obs):
        super(ScriptedTechBot, self).step(obs)
        
        # This is pretty slick and also understandable. If you can _MOVE_SCREEN, 
        # you must have a unit selected that you can move, otherwise, you don't 
        # have _MOVE_SCREEN in the available action space.
        if _MOVE_SCREEN in obs.observation["available_actions"]:
            
        	
            return actions.FunctionCall(_NO_OP, [])
            
        else:
            # Again the reference for this is in the actions part of the PYSC2
            # Git account. (https://github.com/deepmind/pysc2/blob/master/pysc2/lib/actions.py)
            # It just selects all your friendly units, so no math or pointing, or rectangles. 
            # Drawbacks include: maybe you don't want to move your entire army every time. 
            return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])

            # Then if you want to select a single point, then uncomment the following.
            #unit_type = obs.observation["screen"][features.SCREEN_FEATURES.unit_type.index]
            #zergling_y, zergling_x = (unit_type == _ZERG_ZERGLING).nonzero()

            # The positional array should be averaged in 9 unit groupings to find a single 
            # unit. so:
            # [10:] in this case would be the second zergling.
            # [:9] would be the first zergling. Although for some reason the second is more 
            # reliable. I'm not sure why.
            #select_x_mean = int(zergling_x[10:].mean())
            #select_y_mean = int(zergling_y[10:].mean())
            
            #select_point = [select_x_mean, select_y_mean]
                
            #return actions.FunctionCall(_SELECT_POINT, [_SELECT, select_point])
