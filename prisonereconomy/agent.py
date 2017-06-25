from biases import *
from config import max_mutation
from movement import Point


# may want to add a mutate-able gene that affects mobility
class Agent:
    def __init__(self, biases):
        self.id = random()
        self.biases = biases
        self.memories = {}
        self.score = 0
        self.location = Point((random(), random()))

    def memorize(self, other, memory):
        if other in self.memories:
            self.memories[other].append(memory)
        else:
            self.memories[other] = [memory]

    def forget(self, agent):
        if agent in self.memories:
            del self.memories[agent]

    def print_biases(self):
        for bias in self.biases:
            print(bias + ": " + str(self.biases[bias].value))

    def mutate(self):
        for bias in self.biases:
            self.biases[bias].value += uniform(-max_mutation, max_mutation)

    def get_child(self):
        child = Agent(self.biases)
        child.location = self.location
        child.mutate()
        return child

    def move(self, other, toward):
        self.location.move(other.location, toward)


class Memory:
    def __init__(self, stakes, my_response, their_response):
        self.stakes = stakes
        self.my_response = my_response
        self.their_response = their_response


def generate_agent():
    return Agent(generate_biases())
