import numpy as np
import gym
import random
import time

env = gym.make("FrozenLake-v0")

action_space_size = env.action_space.n
state_space_size = env.observation_space.n

q_table = np.zeros((state_space_size, action_space_size))

num_episodes = 10000
max_steps_per_episode = 100

learning_rate = 0.1
discount_rate = 0.99

exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay = 0.001

rewards_all_episodes = []
success_count = 0
step_count = []

# Q-learning algorithm
for episode in range(num_episodes):
    state = env.reset()
    done = False
    episode_reward = 0

    for step in range(max_steps_per_episode):
        # Exploration-exploitation trade-off
        if random.uniform(0, 1) < exploration_rate:
            action = env.action_space.sample()
        else:
            action = np.argmax(q_table[state, :])

        new_state, reward, done, info = env.step(action)

        # Update Q-table for Q(s,a)
        q_table[state, action] = q_table[state, action] * (1 - learning_rate) + learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))

        state = new_state
        #episode_reward += reward * (1+(-1*(1/(1+2.718**(-(step/10-5))))))  # Logistic function
        episode_reward += reward * (1-(step/max_steps_per_episode))

        if done:
            if episode_reward > 0 and episode >= 9000:
                success_count += 1
                step_count.append(step)

            break

    # Exploration rate decay
    exploration_rate = min_exploration_rate + (1 - min_exploration_rate) * np.exp(-exploration_decay * episode)

    rewards_all_episodes.append(episode_reward)

# Calculate and print the average reward per thousand episodes
rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes), num_episodes/1000)
count = 1000

print("********Average reward per thousand episodes********\n")
for r in rewards_per_thousand_episodes:
    print(count, ": ", str(sum(r/1000)))
    count += 1000

print("********Success rate********")
print(success_count/1000)

print("********Average steps********")
print(sum(step_count)/len(step_count), "\n")

print(q_table)

# Watch our agent play Frozen Lake by playing the best action
# from each state according to the Q-table
for episode in range(0):
    state = env.reset()
    done = False
    print("*****EPISODE ", episode+1, "*****\n\n\n\n")
    time.sleep(1)

    for step in range(max_steps_per_episode):
        env.render()
        time.sleep(0.3)

        action = np.argmax(q_table[state, :])
        new_state, reward, done, info = env.step(action)

        if done:
            env.render()
            if reward == 1:
                print("****You reached the goal!****")
                time.sleep(3)
            else:
                print("****You fell through a hole!****")
                time.sleep(3)
            break

        state = new_state

env.close()
