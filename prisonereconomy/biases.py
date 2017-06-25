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
    score = sum([agent.biases[bias].func(stakes, agent, other)
                 for bias in agent.biases])
    return score

'''
In order to apply each bias indiscriminately with one function,
all factoring  functions must have access to all data available to
_any_  bias, even if the factoring function itself does not use all
of its arguments.

In other words, all factoring functions must include arguments
(stakes, agent, other), as the simulator will try to pass those
arguments in whether you like it or not.
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


'''
The below factors may be referred to as "selfish factors", as they
are primarily used to either take advantage of a naive partner or
to defend against an aggressor. In essence, each of the following
four functions factors the advantage of defecting in various
scenarios.

The comments denoting which values are being subtracted from each
other to determine the "total" value (typically negative) come from
the two tables of possibilities defined below.

Points for Agent
a = agent cooperates, other cooperates
b = agent cooperates, other defects
c = agent defects, other cooperates
d = agent defects, other defects

Points for Other
e = other cooperates, agent cooperates
f = other cooperates, agent defects
g = other defects, agent cooperates
h = other defects, agent defects
'''

def factor_ambition(stakes, agent, other):
    # assumes the opponent cooperates, factors advantage from defecting
    total = stakes.a - stakes.c
    return total * agent.biases["ambition"].value


def factor_caution(stakes, agent, other):
    # assumes the opponent defects, factors disadvantage from cooperating
    total = stakes.b - stakes.d
    return total * agent.biases["caution"].value


def factor_ctr_ambition(stakes, agent, other):
    # assumes own cooperation, factors opponent's advantage from defecting
    total = stakes.e - stakes.g
    return total * agent.biases["ctr_ambition"].value


def factor_ctr_caution(stakes, agent, other):
    # assumes own defection, factors opponent's disadvantage from cooperating
    total = stakes.f - stakes.h
    return total * agent.biases["ctr_caution"].value

'''
To add a bias to the existing structure, simply add it as a
key to the dict below, along with a pair consisting of
the function used to retrieve initial values for randomly
generated agents, as well as the function used to factor
the bias into a decision score.

Both functions in each of these pairs should typically
return values in the range of -1.0 and 1.0.

The global bias dict is represented as an ordered dict
to maintain the order in which the keys were added.
This is useful, for example, when creating new prototypes,
as the order of factors only needs to be defined once.
'''

bias_dict = OrderedDict([])
bias_dict["trust"] = (default_range, factor_trust)
bias_dict["reciprocity"] = (random, factor_reciprocity)
bias_dict["distance"] = (default_range, factor_distance)
bias_dict["similarity"] = (default_range, factor_similarity)
bias_dict["history"] = (random, factor_trust)
bias_dict["ambition"] = (random, factor_ambition)
bias_dict["caution"] = (random, factor_caution)
bias_dict["ctr_ambition"] = (random, factor_ctr_ambition)
bias_dict["ctr_caution"] = (random, factor_ctr_ambition)
