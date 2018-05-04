import pickle
from dilemma.biases import bias_dict


def save_prototype(biases, file):
    with open(file, "wb") as prototype:
        pickle.dump(biases, prototype)


def load_prototype(file):
    with open(file, "rb") as prototype:
        return pickle.load(prototype)


def create_prototype(**kwargs):
    biases = kwargs
    remainder = check_biases(biases)  # list of biases not included in kwargs
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
    filename = "prototypes/" + name + ".pkl"
    biases = {}
    for bias in bias_dict:
        output_string = "Enter {} value for {}:  ".format(bias, name)
        biases[bias] = float(input(output_string))
    save_prototype(biases, filename)
