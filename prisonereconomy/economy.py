from random import randint
from prisonereconomy.agent import *
from itertools import product
import math
import prisonereconomy.config as config


class Economy:
    def __init__(self):
        self.population = [generate_agent() for _ in range(config.starting_population)]
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

    def generate_stakes(self):
        # c >= a >= d >= b
        # f > = e >= h >= g
        # c > 0, g > 0, a > 0, e > 0
        c = randint(1, self.highest_stakes)
        a = randint(1, c)
        d = randint(self.lowest_stakes, a)
        b = randint(self.lowest_stakes, d)
        f = randint(1, self.highest_stakes)
        e = randint(1, f)
        h = randint(self.lowest_stakes, e)
        g = randint(self.lowest_stakes, h)
        return stakes_tuple(a, b, c, d, e, f, g, h)

    def distance_function(self, distance):
        if distance == 0:
            return math.inf
        return 1.0 / (distance ** self.distance_mod)

    def interact(self, a, b):
        distance = sqrt(abs(((a.location[0] - b.location[0]) ** 2) -
                            ((a.location[1] - b.location[1]) ** 2)))
        if random() <= self.distance_function(distance):
            stakes = self.generate_stakes()
            a_response = get_response(stakes, a, b)
            b_response = get_response(stakes, b, a)
            self.raw_history.append(a_response)
            self.raw_history.append(b_response)
            a.memorize(b, Memory(stakes, a_response, b_response))
            b.memorize(a, Memory(stakes, b_response, a_response))
            a_result = stakes[a_response][b_response][0]
            b_result = stakes[a_response][b_response][1]
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
            if agent.score >= self.score_cap and len(self.population) < self.max_population:
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


def stakes_tuple(a, b, c, d, e, f, g, h):
    # ordered so that the tuple can be navigated with True/False values
    stakes = (((d, h), (c, g)), ((b, f), (a, e)))
    return stakes


def print_stakes(stakes):
    # update with string.format later
    print("CC: ", stakes[1][1])
    print("CD: ", stakes[1][0])
    print("DC: ", stakes[0][1])
    print("DC: ", stakes[0][0])
