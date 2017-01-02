from math import log

NUM_ELEMENTS = 512
LENGTH_OF_BITMAP = int(log(NUM_ELEMENTS, 2))
BITMAP = "0" * LENGTH_OF_BITMAP


def get_binary_representation(number):
    binary = "{0:b}".format(number)
    while len(binary) < LENGTH_OF_BITMAP:
        binary = "0" + binary;
    return binary


# returns the position of the least significant bit (counting from left to right)
def get_least_sign_bit(number):
    if number == 0:
        return LENGTH_OF_BITMAP
    b_number = get_binary_representation(number)
    counter = -1
    for index in b_number:
        counter += 1
        if index == "1":
            return counter
    return 0

print BITMAP

