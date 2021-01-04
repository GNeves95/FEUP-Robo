import gym
import mujoco_py
from time import sleep
import time

import random

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

#env = gym.make('gym_mujo:quadruped-v0')

gym.envs.register(
        id='HalfieCheetah-v2',
        entry_point='gym_mujo.envs:HalfCheetahEnvV2',
    )

env = gym.make('gym_mujo:HalfieCheetah-v2')

states = env.observation_space.shape[0]
print(states)
#actions = env.action_space.n
# print(states)
# for i_episode in range(30):
#     observation = env.reset()
#     for t in range(300):
#         #sleep(1/30)
#         env.render()
#         #printing the observation space
#         print(observation) 
#         #storing the number of possible actions
#         action = env.action_space.sample() 
#         observation, reward, done, info = env.step(action)
#         if done:
#             print("Episode finished after {} timesteps".format(t+1))
#             break
# env.close()

episodes = 10
timeout = 60
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0
    timeout_start = time.time()
    timeout_end = timeout_start + 10
    while (not done) and (time.time() < timeout_end):
        t = timeout_end - time.time()
        #sleep(1/30)
        #env.render()
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
    print ('Episode: {} Score: {}\n Done: {} Time: {}'.format(episode, score, done, time.time() - timeout_end))
env.close()