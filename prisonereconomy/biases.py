from random import uniform, random
from math import sqrt
from collections import OrderedDict
import attr


@attr.s
class Bias:
    value = attr.ib()
    func = attr.ib()


def generate_biases():
    return {bias: Bias(bias_dict[bias][0](), bias_dict[bias][1]) 
            for bias in bias_dict}


def default_range():
    return uniform(-1.0, 1.0)


def get_response(stakes, agent, other):
    return factor_biases(stakes, agent, other) >= 1.0


def factor_biases(stakes, agent, other):
    score = sum([agent.biases[bias].apply(stakes, agent, other) 
                 for bias in agent.biases])
    return score

'''
In order to apply each bias indiscriminately with one function, 
all factoring  functions must have access to all data available to 
_any_  bias, even if the factoring function itself does not use all
of its arguments.
'''


def factor_trust(stakes, agent, other):
    return agent.biases["trust"].value


def factor_reciprocity(stakes, agent, other):
    last_response = False
    if other in agent.memories:
        last_response = agent.memories[other][-1].their_response
    return last_response * agent.biases["reciprocity"].value


def factor_distance(stakes, agent, other):
    distance = sqrt(((agent.location[0] - other.location[0]) ** 2) +
                     (agent.location[1] - other.location[1]) ** 2)
    return distance * agent.biases["distance"].value


def factor_similarity(stakes, agent, other):
    distance = 0.0
    for bias in agent.biases:
        distance += abs(agent.biases[bias].value -
                        other.biases[bias].value)
    return distance * agent.biases["similarity"].value


def factor_history(stakes, agent, other):
    history = 0.0
    if other in agent.memories:
        for memory in agent.memories[other]:
            x = memory.my_response
            y = memory.their_response
            history += (memory.stakes[x][y] - memory.stakes[y][x])
        history /= len(agent.memories[other])
    return history * agent.biases["history"].value


def factor_ambition(stakes, agent, other):
    # assumes the opponent cooperates, factors advantage from defecting
    total = stakes[0][0][0] - stakes[1][0][0]  # a - c
    return total * agent.biases["ambition"].value


def factor_caution(stakes, agent, other):
    # assumes the opponent defects, factors disadvantage from cooperating
    total = stakes[0][1][0] - stakes[1][1][0]  # b - d
    return total * agent.biases["caution"].value


def factor_ctr_ambition(stakes, agent, other):
    # assumes cooperation, factors opponent's advantage from defecting
    total = stakes[0][0][1] - stakes[0][1][1]  # e - f
    return total * agent.biases["ctr_ambition"].value


def factor_ctr_caution(stakes, agent, other):
    # assumes defection, factors opponent's disadvantage from cooperating
    total = stakes[1][0][1] - stakes[1][1][1]  # g - h
    return total * agent.biases["ctr_caution"].value

'''
To add a bias to the existing structure, simply add it as a 
key to the dict below, along with a pair consisting of
the function used to retrieve initial values for randomly 
generated agents, as well as the function used to factor
the bias into a decision score.

Both functions in each of these pairs should typically 
return values in the range of -1.0 and 1.0.
'''

bias_dict = OrderedDict([
    "trust": (default_range, factor_trust),
    "reciprocity": (random, factor_reciprocity),
    "distance": (default_range, factor_distance),
    "similarity": (default_range, factor_similarity),
    "history": (random, factor_trust),
    "ambition": (random, factor_ambition),
    "caution": (random, factor_caution),
    "ctr_ambition": (random, factor_ctr_ambition),
    "ctr_caution": (random, factor_ctr_ambition),
    ])
