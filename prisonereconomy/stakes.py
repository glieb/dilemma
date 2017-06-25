'''
The Stakes class can be used as either a container of single-letter
variables denoting the points awarded to a participant of a single
iteration of a dilemma, or as a subscriptable pair of pairs of pairs,
which can accept three boolean values in order to settle on a
corresponding points value.


The single letter variables are defined as follows:

Points for Agent:
a = agent cooperates, other cooperates
b = agent cooperates, other defects
c = agent defects, other cooperates
d = agent defects, other defects

Points for Other
e = other cooperates, agent cooperates
f = other cooperates, agent defects
g = other defects, agent cooperates
h = other defects, agent defects


To subscript a Stakes object instead of referring to its single-letter
variable value, three boolean values are necessary in succession to
finally bring about a number that can be used as a value in calculating
the results of a dilemma.

The order of booleans is defined as follows:

1st = True if agent cooperates, False if agent defects
2nd = True of other cooperates, False if other defects
3rd = True if calculating reward for agent,
      False if calculating reward for other

For example, to find the reward given to the agent when both the
agent and the other cooperate (self.a in the attribute scheme), you
could use self[True,True,True]. This is useful for finding points
values using only the data retrieved from agents about whether or
not they cooperated, as well as whether they are the initiator of
the dilemma in question.
'''

from random import randint

class Stakes(object):
    def __init__(self, a, b, c, d, e, f, g, h):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        self.tuple_form = (((h, d), (f, c)), ((g, b), (e, a)))

    def __repr__(self):
        return str(sorted({
            "a": self.a,
            "b": self.b,
            "c": self.c,
            "d": self.d,
            "e": self.e,
            "f": self.f,
            "g": self.g,
            "h": self.h,
        }))

    def __getitem__(self, i):
        return self.tuple_form.__getitem__(i)


def generate_stakes(lowest, highest):
    # c >= a >= d >= b
    # g > = e >= h >= f
    # c >= 0, g >= 0, a >= 0, e >= 0
    c = randint(0, highest)
    a = randint(0, c)
    d = randint(lowest, a)
    b = randint(lowest, d)
    g = randint(0, highest)
    e = randint(0, g)
    h = randint(lowest, e)
    f = randint(lowest, h)
    return Stakes(a, b, c, d, e, f, g, h)
