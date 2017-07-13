import pickle
from biases import bias_dict


def save_prototype(biases, filename):
    open(filename, "w+")  # creates the file
    with open(filename, "wb") as prototype:
        pickle.dump(biases, prototype)


def load_prototype(file):
    with open(file, "rb") as prototype:
        return pickle.load(prototype)


def create_prototype(**kwargs):
    biases = kwargs
    remainder = check_biases(biases)  # list of biases not included
    for bias in remainder:
        biases[bias] = 0  # do not factor unmentioned bases
    return biases


def check_biases(biases):
    return [bias for bias in bias_dict if bias not in biases]



if __name__ == "__main__":
    print("Enter the name of your new prototype, or EXIT to cancel.")
    name = input(">>")
    if name == "EXIT":
        exit()
    filename = "../prototypes/" + name + ".pkl"
    biases = {}
    for bias in bias_dict:
        biases[bias] = float(input(
            "Enter {} value for {}:  ".format(bias, name)))
    save_prototype(biases, filename)
