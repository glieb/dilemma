import sys
sys.path.append("..")
from economy import Economy
import pickle
import config


def main(argv):  # take pkd and int as arguments
    filename = "../savedata/" + argv[1] + ".pkl"
    try:
        with open(filename, "rb") as load_file:
            economy = pickle.load(load_file)
    except FileNotFoundError:
        economy = Economy()
        open(filename, "w+")
    try:
        generations = int(argv[2])
    except ValueError:
        print("Error: Invalid input")
        return
    while generations > 0:
        economy.pass_generation()
        generations -= 1
    with open(filename, "wb") as save_file:
        pickle.dump(economy, save_file)


if __name__ == "__main__":
    sys.setrecursionlimit(config.recursion_limit)
    main(sys.argv)
