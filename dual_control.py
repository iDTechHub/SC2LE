from pysc2.agents import base_agent

from pysc2.lib import features
from pysc2.lib import actions

import numpy as np
import time

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_SELECTED = features.SCREEN_FEATURES.selected.index

_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals

_NO_OP = actions.FUNCTIONS.no_op.id
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_SELECT_UNIT = actions.FUNCTIONS.select_unit.id
_SELECT_CONTROL_GROUP = actions.FUNCTIONS.select_control_group.id

#Parameter readability
_SINGLE_SELECT = [0]

_CONTROL_GROUP_RECALL = [0]
_CONTROL_GROUP_SET = [1]

_NOT_QUEUED = [0]
_SELECT_ALL = [0]

NO_SELECTION = 'noselection'
MARINE_1_SETUP = 'marine1'
MARINE_2_SETUP = 'marine2'
PLAYING = 'playing'

class SelectorBot(base_agent.BaseAgent):

    state = NO_SELECTION
    marine_1_setup = False
    marine_2_setup = False

    #which marine's turn is it (1 or 2)?
    turn = 1
    select_swap = True

    def step(self, obs):
        super(SelectorBot, self).step(obs)
        
        # uncomment this sleep function to see it animate and visualize the
        # steps a little better.
        #time.sleep(.15)

        #if we've got no control groups, set them up again:
        group_type, group_count = obs.observation["control_groups"].nonzero()
        if self.state == PLAYING and not group_type.any():
            self.marine_1_setup = False
            self.marine_2_setup = False
            self.state = NO_SELECTION
         # 4 states - no selection, marine 1, marine 2, playing.

        if self.state == NO_SELECTION:
            if not self.marine_1_setup:
                self.state = MARINE_1_SETUP
            elif not self.marine_2_setup:
                self.state = MARINE_2_SETUP
            else:
                self.select_swap = True
                self.state = PLAYING
            return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])
        elif self.state == MARINE_1_SETUP:
            # Select unit is only possible with multiple, so we must have the army selected
            if _SELECT_UNIT in obs.observation["available_actions"]:
                # select unit in position 0 of our selection
                return actions.FunctionCall(_SELECT_UNIT, [_SINGLE_SELECT, [0]])
            else:
                self.marine_1_setup = True
                self.state = NO_SELECTION
                # save control group with our marine
                return actions.FunctionCall(_SELECT_CONTROL_GROUP, [_CONTROL_GROUP_SET, [1]])
        elif self.state == MARINE_2_SETUP:
            if _SELECT_UNIT in obs.observation["available_actions"]:
                return actions.FunctionCall(_SELECT_UNIT, [_SINGLE_SELECT, [1]])
            else:
                self.marine_2_setup = True
                self.state = NO_SELECTION
                return actions.FunctionCall(_SELECT_CONTROL_GROUP, [_CONTROL_GROUP_SET, [2]])

        # If we got here, we're playin!

        if self.select_swap:
            # select the one whose turn it is!
            self.select_swap = False
            return actions.FunctionCall(_SELECT_CONTROL_GROUP, [_CONTROL_GROUP_RECALL, [self.turn]])
        else:
            # find closest mineral shard

            # Use the player relative layer to find mineral shards
            player_relative = obs.observation["screen"][_PLAYER_RELATIVE]

            # Use the selected layer to find our selected marine's position
            selected = obs.observation["screen"][_SELECTED]

            # Get all pixels that our marine is in
            player_y, player_x = (selected == 1).nonzero()
            # average position of selected marine
            player = [int(player_x.mean()), int(player_y.mean())]

            # Get all the pixels that have a mineral shard
            neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()

            # If we don't have marines or shards, don't do anything
            if not neutral_y.any() or not player_y.any():
                return actions.FunctionCall(_NO_OP, [])

            # Find the closest mineral shard
            closest, min_dist = None, None
            for p in zip(neutral_x, neutral_y):
                dist = np.linalg.norm(np.array(player) - np.array(p))
                if not min_dist or dist < min_dist:
                    closest, min_dist = p, dist

            # set up to swap marines
            self.select_swap = True
            self.turn = 1 if self.turn == 2 else 2
            return actions.FunctionCall(_MOVE_SCREEN, [_NOT_QUEUED, closest])





        # no op if we somehow get here with nothing to do
        return actions.FunctionCall(_NO_OP, [])
