import random


def random_byte():
    h = hex(random.randint(0, 255))
    if len(h) == 3:
        num = h[-1]
        h = '0x0' + num

    return h


def mutate_key(individual, indpb):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = random_byte()

    return individual


def generate_2048key():
    key = [random_byte() for i in range(128)]
    key = ''.join([i[2:] for i in key])

    return key

