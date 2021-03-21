from gym.envs.registration import register

register(
    id='kalaha-v0',
    entry_point='gym_kalaha.envs:KalahaEnv'
)
