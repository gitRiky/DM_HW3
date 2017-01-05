import codecs
import utility
import numpy

LENGTH_BITMAP = 18
NUM_HASH_FAMILIES = 72
GROUP_SIZE = 6
HEX_LEN = LENGTH_BITMAP / 4
FILE_NAME = "sim.txt"


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


def generate_estimations(stream, hash_functions):
    max_tail = [0] * NUM_HASH_FAMILIES
    for elem in stream:
        elem = elem.replace("\n", "")
        index = 0   # represent the index of the hash function in the list
        for hash_function in hash_functions:
            h_elem = hash_function(elem)
            # print "hash = " + h_elem
            if h_elem != "0" * HEX_LEN:
                tail = get_least_sign_bit(h_elem)
                # print "tail = ", tail
                if tail > max_tail[index]:
                    max_tail[index] = tail
            index += 1
    print "Max tail = ", max_tail
    estimation = []
    for m_tail in max_tail:
        estimation.append(2 ** m_tail)
    return estimation


def compute_average(estimations, size):
    averages = []
    sum = 0
    counter = 0
    for estimation in estimations:
        sum += estimation
        counter += 1
        if counter == size:
            averages.append(float(sum) / float(counter))
            sum = 0
            counter = 0
    return averages


def estimate_f0(stream):
    hash_functions = utility.init_hash_families(NUM_HASH_FAMILIES)
    estimations = generate_estimations(stream, hash_functions)
    averages = compute_average(estimations, GROUP_SIZE)
    return numpy.median(averages)


def bf_duplicates(file_handle):
    dict = {}
    for line in file_handle:
        line = line.replace("\n","")
        if dict.has_key(line):
            dict[line] = dict[line] + 1
        else:
            dict[line] = 1
    print "number of different elements = ", len(dict.keys())


def main():
    with codecs.open(FILE_NAME, 'r') as file_handle:
        bf_duplicates(file_handle)
    with codecs.open(FILE_NAME, 'r') as file_handle:
        result = estimate_f0(file_handle)
    print "The number of estimated different elements is ", result


with codecs.open("sim.txt", 'w') as f:
    for i in range(1,200000):
        f.write(str(i % 100))
        f.write("\n")
main()
