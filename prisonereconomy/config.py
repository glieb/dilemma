from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
econ = config["DEFAULT"]
adv = config["advanced"]

starting_population = econ.getint("starting_population")
max_population = econ.getint("max_population")
lowest_stakes = econ.getint("lowest_stakes")
highest_stakes = econ.getint("highest_stakes")
days_per_generation = econ.getint("days_per_generation")
max_mutation = econ.getfloat("max_mutation")
max_movement = econ.getfloat("max_movement")
score_cap = econ.getint("score_cap")
score_min = econ.getint("score_min")
distance_mod = econ.getint("distance_mod")

recursion_limit = adv.getint("recursion_limit")