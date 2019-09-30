import random


def create_gomi(byte_length):
    return bytes([int(random.random()*256) for i in range(byte_length)])

a = create_gomi(8)
print(a)