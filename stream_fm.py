import codecs
import utility
import numpy

LENGTH_BITMAP = 64
NUM_HASH_FUNCTIONS = 20
HEX_LEN = LENGTH_BITMAP / 4

def get_binary_representation(number):
    binary = "{0:b}".format(int(number, 16))  # give me the binary form of the hex representation of number
    while len(binary) < LENGTH_BITMAP:
        binary = "0" + binary
    return binary


# least significant one position, it is equal to the length of the tail
def get_least_sign_bit(number):
    if number == 0:
        return LENGTH_BITMAP
    b_number = get_binary_representation(number)
    # print "binary = " + b_number
    return LENGTH_BITMAP - 1 - b_number.rfind("1")


def update_f0(line, max_tail, hash_functions):
    index = 0
    update = False
    for hash_function in hash_functions:
        h_elem = hash_function(line)
        if h_elem != '0' * HEX_LEN:
            tail = get_least_sign_bit(h_elem)
            if tail > max_tail[index]:
                max_tail[index] = tail
                update = True
        index += 1
    if update:
        estimation = []
        for tail in max_tail:
            estimation.append(2 ** tail)
        return estimation