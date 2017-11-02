from pysc2.agents import base_agent

from pysc2.lib import features
from pysc2.lib import actions

# NO_OP's current function id is 0, which you can find at: https://github.com/deepmind/pysc2/blob/master/pysc2/lib/actions.py
# So you *could* write:
# NO_OP = 0 # This would work just fine, but that's probably not a great idea.
_NO_OP = actions.FUNCTIONS.no_op.id

class ScriptedTechBot(base_agent.BaseAgent):

    def step(self, obs):
        super(ScriptedTechBot, self).step(obs)
        
        # If you wanted an unreadable function that gets worse as you go on
        # here you could write:
        # return actions.FunctionCall(0, [])
        return actions.FunctionCall(_NO_OP, [])
