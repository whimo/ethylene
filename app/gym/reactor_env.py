from gym import Env
from gym import spaces
from reactor_state import ReactorState


class ReactorEnv(Env):
    def __init__(self, observations_df, states_df, actions_df, rewards_df, constraints):
        self.state = None
        self.states_df = states_df
        self.observations_df = observations_df
        self.actions_df = actions_df
        self.rewards_df = rewards_df
        self.constraints = constraints
        self.index = 0

        self.observation_ = spaces.Discrete(observations_df.shape[1])
        self.action_space = spaces.Discrete(actions_df.shape[1])

    def _step(self):
        reward = self.rewards_df[self.index]
        state, done = self.state.next()
        action = self.actions_df[self.index]
        self.index += 1

        return state, action, reward, done, None

    def _reset(self):
        self.state = ReactorState(self.states_df)
        self.index = 0

        state, done = self.state.next()
        return state
