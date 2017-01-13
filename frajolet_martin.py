import codecs
import utility
import numpy
import config

FILE_NAME = "live.txt"


def generate_estimations(stream, hash_functions):
    max_tail = [0] * config.NUM_HASH_FAMILIES
    for elem in stream:
        elem = elem.replace("\n", "")
        index = 0   # represent the index of the hash function in the list
        for hash_function in hash_functions:
            h_elem = hash_function(elem)
            # print "hash = " + h_elem
            if h_elem != "0" * config.HEX_LEN:
                tail = utility.get_least_sign_bit(h_elem)
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
    hash_functions = utility.init_hash_families(config.NUM_HASH_FAMILIES)
    estimations = generate_estimations(stream, hash_functions)
    averages = compute_average(estimations, config.GROUP_SIZE)
    return numpy.median(averages)


def bf_duplicates(file_handle):
    dict = {}
    for line in file_handle:
        line = line.replace("\n","")
        if dict.has_key(line):
            dict[line] = dict[line] + 1
        else:
            dict[line] = 1
    return len(dict.keys())


def main():
    output = file("output_twitter_f0.txt", 'w')
    with codecs.open(FILE_NAME, 'r') as file_handle:
        result = bf_duplicates(file_handle)
        output.write("The number of distinct elements are " + str(result) + "\n")
    with codecs.open(FILE_NAME, 'r') as file_handle:
        result = estimate_f0(file_handle)
        output.write("The number of estimated distinct elements with HASH_FAMILIES = " + str(config.NUM_HASH_FAMILIES))
        output.write(" and group size = " + str(config.GROUP_SIZE) + " is equal to " + str(result))
    output.close()

main()
