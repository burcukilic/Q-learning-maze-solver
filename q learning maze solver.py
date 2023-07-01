import math

import pygame
import numpy as np
import random

random.seed(1)
pygame.init()
win = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
run = True
font = pygame.font.Font('freesansbold.ttf', 32)

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

n = 5  # it will be an nxn square grid.

# HYPERPARAMETERS
learning_rate = 0.1
discount_factor = 0.9
epsilon = 1
epsilon_decay = 0.99
epsilon_min = 0.00

goal = [4, 4]
obstacle = [2, 2]


# AGENT CLASS
class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.step = 0
        self.obstacled = False
        self.goalReached = False

    def draw(self):
        done = False
        pygame.draw.circle(win, blue, (self.x * 600 / n + 300 / n, self.y * 600 / n + 300 / n), 10)
        self.step += 1
        if self.x == obstacle[0] and self.y == obstacle[1]:
            self.obstacled = True
            done = True
        elif self.x == goal[0] and self.y == goal[1]:
            self.goalReached = True
            print(f"Goal Reached in {self.step} steps!")
            done = True
        elif self.x < 0 or self.x >= n or self.y < 0 or self.y >= n:
            self.obstacled = True
            done = True
        elif self.step == max_steps:
            done = True

        return done

    def act(self, action):
        if action == 0:
            self.x -= 1
        elif action == 1:
            self.x += 1
        elif action == 2:
            self.y -= 1
        elif action == 3:
            self.y += 1

    def fitness(self):
        return -self.step - 60 * self.obstacled + 60 * self.goalReached - math.sqrt((goal[0]-self.x)**2 + (goal[1]-self.y)**2)


num_actions = 4

Q = np.random.uniform(low=-1, high=1, size=(n, n, num_actions))

max_steps = 10
current_step = 0
episode_fitness = 0
agent = Agent(0, 0)
action = 0
state = [0, 0]
episode = 0

# MAIN LOOP#
while run:
    # GENERAL STUFF#
    win.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.draw.rect(win, green, (goal[0] * 600 // n, goal[1] * 600 // n, 600 // n, 600 // n))
    pygame.draw.rect(win, red, (obstacle[0] * 600 // n, obstacle[1] * 600 // n, 600 // n, 600 // n))

    for i in range(n):
        pygame.draw.line(win, (0, 0, 0), (i * 600 / n, 0), (i * 600 / n, 600))
    for i in range(n):
        pygame.draw.line(win, (0, 0, 0), (0, i * 600 / n), (600, i * 600 / n))

    # ALGORITHM

    if current_step == 1:
        agent = Agent(0, 0)
        episode_fitness = 0
        state = [0, 0]

    if np.random.rand() < epsilon:
        actions = [0, 1, 2, 3]
        if agent.x == 0:
            actions.remove(0)
        elif agent.x == n-1:
            actions.remove(1)
        if agent.y == 0:
            actions.remove(2)
        elif agent.y == n-1:
            actions.remove(3)
        action = random.choice(actions)
    else:
        actions = [0, 1, 2, 3]
        if agent.x == 0:
            actions.remove(0)
        elif agent.x == n - 1:
            actions.remove(1)
        if agent.y == 0:
            actions.remove(2)
        elif agent.y == n - 1:
            actions.remove(3)
        maxValue = -100000
        action = 0
        for i in actions:
            if Q[state[0], state[1], i] > maxValue:
                maxValue = Q[state[0], state[1], i]
                action = i

    agent.act(action)
    done = agent.draw()

    next_state = [agent.x, agent.y]

    Q[state[0], state[1], action] += learning_rate * (agent.fitness() + discount_factor * np.max(
        Q[next_state[0], next_state[1]]) - Q[state[0], state[1], action])

    episode_fitness += agent.fitness()
    state = next_state

    if done:
        current_step = 0

    current_step = current_step % 8 + 1

    if current_step == 1:
        if epsilon > epsilon_min:
            epsilon *= epsilon_decay
        episode += 1
        print(f"Episode {episode}: Reward = {episode_fitness} Epsilon = {epsilon}")

    clock.tick(5)
    pygame.display.update()

pygame.quit()
