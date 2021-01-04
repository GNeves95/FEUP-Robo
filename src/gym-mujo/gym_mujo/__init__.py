from gym.envs.registration import register

register(
    id='quadruped-v0',
    entry_point='gym_mujo.envs:QuadrupedeEnv',
    max_episode_steps=1000,
    reward_threshold=4800.0,
)