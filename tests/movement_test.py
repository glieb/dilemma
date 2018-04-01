from prisonereconomy.movement import *
import random


def main():
    for i in range(100):
        print("Iteration #{}".format(i+1))

        point_a = Point((random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)))
        point_b = Point((random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)))

        placeholder = distance(point_a, point_b)
        point_a.move(point_b, True)
        assert placeholder >= distance(point_a, point_b)

        placeholder = distance(point_a, point_b)
        point_b.move(point_b, True)
        assert placeholder >= distance(point_a, point_b)

        placeholder = distance(point_a, point_b)
        point_a.move(point_b, False)
        assert placeholder <= distance(point_a, point_b)

        placeholder = distance(point_a, point_b)
        point_b.move(point_a, False)
        assert placeholder <= distance(point_a, point_b)


if __name__ == "__main__":
    main()
    print("Done")