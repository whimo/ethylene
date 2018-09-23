from gym.envs.registration import register

register(
    id='Ethylene-v0',
    entry_point='gym_ethylene.envs:EthyleneEnv',
    kwargs={'datadir': 'ethylene'}
