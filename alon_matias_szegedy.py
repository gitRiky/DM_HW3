import codecs
import random
import utility
import numpy
import config


N = 1377
FILE_NAME = "live.txt"


# compute the f2 in the brute force way
def bf_f2(file_handle):
    hash_map = {}
    f2 = 0
    lines = 0
    for line in file_handle:
        lines += 1
        line = line.replace("\n", "").replace("\r", "")
        if hash_map.has_key(line):
            hash_map[line] = hash_map[line] + 1
        else:
            hash_map[line] = 1
    for elem in hash_map.keys():
        f2 += hash_map[elem] ** 2
    print "length ", lines
    return f2


def main():
    output = file("output_twitter_f2.txt", 'w')
    with codecs.open(FILE_NAME, 'r', encoding="utf-8") as file_handle:
        result = bf_f2(file_handle)
        output.write("Exact value for f2 = " + str(result) + "\n")
    with codecs.open(FILE_NAME, 'r', encoding="utf-8") as file_handle:
        result = f2_with_sketch(file_handle)
        output.write("Estimation for f2 using sketch with var = " + str(config.NUM_HASH_FAMILIES) + " is " + str(result))
    output.close()

"""
def estimate_f2(file_handle):
    x = {}
    pos = random.sample(range(0, N), config.NUM_HASH_FAMILIES)
    pos.sort()
    counter = 0
    index = 0
    for line in file_handle:
        line = line.replace("\n", "").replace("\r", "")
        if index < config.NUM_HASH_FAMILIES and counter == pos[index]:
            if x.has_key(line):
                index += 1
            else:
                x[line] = 1
                index += 1
        elif x.has_key(line):
            x[line] = x[line] + 1
        counter += 1
    estimates = []
    for elem in x.keys():
        estimates.append(N * (2 * x[elem] - 1))
    summ = 0
    for elem in estimates:
        summ += elem
    return summ/len(estimates)
"""


def f2_with_sketch(file_handle):
    z = [0] * config.NUM_HASH_FAMILIES
    hash_functions = utility.init_hash_families(config.NUM_HASH_FAMILIES)
    for line in file_handle:
        line = line = line.replace("\n", "").replace("\r", "")
        for i in range(0, config.NUM_HASH_FAMILIES):
            z[i] += utility.my_hash(hash_functions[i](line))
    estimates = []
    for elem in z:
        estimates.append(elem ** 2)
    return int(numpy.average(estimates))


main()
