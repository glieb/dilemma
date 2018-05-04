import sys
sys.path.append("..")
from dilemma.stakes import generate_stakes
from dilemma.config import lowest_stakes, highest_stakes


def main(iterations):
    try:
        iterations = int(iterations)
    except ValueError:
        print("First argument must be an int")
        exit()
    for _ in range(iterations):
        stakes = generate_stakes(lowest_stakes, highest_stakes)
        # assertions based on comments for generate_stakes()
        assert stakes.c >= stakes.a
        assert stakes.a >= stakes.d
        assert stakes.d >= stakes.b
        assert stakes.g >= stakes.e
        assert stakes.e >= stakes.h
        assert stakes.h >= stakes.f
        assert stakes.c >= 0
        assert stakes.g >= 0
        assert stakes.a >= 0
        assert stakes.e >= 0
        assert stakes[1][1][1] == stakes.a
        assert stakes[1][0][1] == stakes.b
        assert stakes[0][1][1] == stakes.c
        assert stakes[0][0][1] == stakes.d
        assert stakes[1][1][0] == stakes.e
        assert stakes[0][1][0] == stakes.f
        assert stakes[1][0][0] == stakes.g
        assert stakes[0][0][0] == stakes.h
    print("stakes test successful")


if __name__ == "__main__":
    main(10)
