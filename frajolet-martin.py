from math import log
import codecs

NUM_ELEMENTS = 32
LENGTH_OF_BITMAP = int(log(NUM_ELEMENTS, 2))


def get_binary_representation(number):
    binary = "{0:b}".format(number)
    while len(binary) < LENGTH_OF_BITMAP:
        binary = "0" + binary;
    return binary


# returns the position of the least significant bit (counting from left to right)
def get_least_sign_bit(number):
    if number == 0:
        return LENGTH_OF_BITMAP
    if type(number) is str:
        b_number = number
    else:
        b_number = get_binary_representation(number)
    counter = -1
    for index in b_number:
        counter += 1
        if index == "1":
            return counter
    return 0


def my_hash(element):
    return hash(element) % LENGTH_OF_BITMAP


def estimate_f0(stream):
    bitmap = []
    for i in range(0, LENGTH_OF_BITMAP):
        bitmap.append('0')
    for elem in stream:
        h_elem = my_hash(elem)
        if h_elem != 0:
            lsb = get_least_sign_bit(h_elem)
            print "elem " + elem + " with lsb = ", lsb
            if bitmap[lsb] == '0':
                bitmap[lsb] = '1'
            print bitmap
    bitmap = "".join(bitmap)
    estimation = 2 ** (LENGTH_OF_BITMAP - 1 - get_least_sign_bit(bitmap))
    return estimation


def main():
    with codecs.open("input2.txt", 'r') as file_handle:
        result = estimate_f0(file_handle)
    print "The number of estimated different elements is ", result

main()
