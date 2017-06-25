from random import randint
from itertools import product
import math
import config
from agent import *
from stakes import Stakes, generate_stakes


class Economy:
    def __init__(self):
        self.population = [
                generate_agent() for _ in range(config.starting_population)]
        self.interactions = 0
        self.days = 0
        self.generations = 0
        self.raw_history = []
        self.max_population = config.max_population
        self.lowest_stakes = config.lowest_stakes
        self.highest_stakes = config.highest_stakes
        self.days_per_generation = config.days_per_generation
        self.max_mutation = config.max_mutation
        self.max_movement = config.max_movement
        self.score_cap = config.score_cap
        self.score_min = config.score_min
        self.distance_mod = config.distance_mod

    def kill(self, agent):
        self.population.remove(agent)
        print("agent killed")

    def multiply(self, agent):
        child_a, child_b = agent.get_child(), agent.get_child()
        self.kill(agent)
        self.population.append(child_a)
        self.population.append(child_b)
        print("agent multiplied")

    def distance_function(self, distance):
        if distance == 0:
            return math.inf
        return 1.0 / (distance ** self.distance_mod)

    def interact(self, a, b):
        distance = sqrt(abs(((a.location[0] - b.location[0]) ** 2) -
                            ((a.location[1] - b.location[1]) ** 2)))
        if random() <= self.distance_function(distance):
            stakes = generate_stakes(self.lowest_stakes, self.highest_stakes)
            a_response = get_response(stakes, a, b)
            b_response = get_response(stakes, b, a)
            self.raw_history.append(a_response)
            self.raw_history.append(b_response)
            a.memorize(b, Memory(stakes, a_response, b_response))
            b.memorize(a, Memory(stakes, b_response, a_response))
            a_result = stakes[a_response][b_response][True]
            b_result = stakes[a_response][b_response][False]
            a.score += a_result
            b.score += b_result
            a.move(b, b_response)
            b.move(a, a_response)
            self.interactions += 1

    def pass_day(self):
        for agent, other in product(self.population, repeat=2):
            if agent != other:
                self.interact(agent, other)
        self.days += 1
        print("day passed")

    def pass_generation(self):
        for _ in range(self.days_per_generation):
            self.pass_day()
        for agent in self.population:
            if (agent.score >= self.score_cap
                    and
                    len(self.population) < self.max_population):
                self.multiply(agent)
            elif agent.score <= self.score_min:
                self.kill(agent)
        if len(self.population) >= self.max_population:
            self.purge()
        self.generations += 1
        print("generation passed")

    def purge(self):
        self.population = self.population[(self.max_population / 2):]

    def invade(self, prototype, quantity):
        while len(self.population) + quantity > self.max_population:
            self.purge()
        for _ in range(quantity):
            self.population.append(Agent(prototype))
