from pysc2.agents import base_agent

from pysc2.lib import features
from pysc2.lib import actions

_NO_OP = actions.FUNCTIONS.no_op.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id

_SELECT_ALL = [0]

###
#_SELECT_POINT = 2 #writing: actions.FUNCTIONS.select_point.id # would be more sensible
# If you are selecting a specific unit, you should find it's unit id.
# Those can be found at: https://github.com/Blizzard/s2client-api/blob/master/include/sc2api/sc2_typeenums.h
# For instance a zergling is 105, a marine is 48
# _ZERG_ZERGLING = 105
###

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
            
            
            ###
            # Let's say you want to select a single unit. You could try:
            # zergling_unit_type = obs.observation["screen"][features.SCREEN_FEATURES.unit_type.index] 
            # zergling_y, zergling_x = (zergling_unit_type == _ZERG_ZERGLING).nonzero()
            # On a map with two zerglings zergling_x could provide:
            # print(zergling_x)
            # [72 73 74 72 73 74 72 73 74 19 20 21 19 20 21 19 20 21] 
            # print(zergling_y)
            # [ 3  3  3  4  4  4  5  5  5  8  8  8  9  9  9 10 10 10]
            # So the first ~9 elements are the 1st unit, and the second 
            # set of elements is the second unit. So if you want to select 
            # a point that is the second unit you could reference unit 10
            # or higher in your x/y arrays like:
            # select_point = [zergling_x[10], zergling_y[10]]
            # return actions.FunctionCall(_SELECT_POINT, [[0], select_point]
            ###
