import gym


class ReactorState:
    def __init__(self, states_df, sep=','):
        self.states_df = states_df
        self.index = 0

    def reset(self):
        self.index = 0

    def next(self):
        if self.index >= len(self.states_df) - 1:
            return None, True

        state = self.states_df.iloc[self.index].values

        self.index += 1

        return state, False

    def shape(self):
        return self.states_df.shape

    def current_price(self):
        return self.df.ix[self.index, 'Close']
