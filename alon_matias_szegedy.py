import codecs
import random
import numpy


N = 319
# compute the f2 in the brute force way
def bf_f2(file_handle):
    hash_map = {}
    f2 = 0
    for line in file_handle:
        line = line.replace("\n", "").replace("\r", "")
        if hash_map.has_key(line):
            hash_map[line] = hash_map[line] + 1
        else:
            hash_map[line] = 1
    for elem in hash_map.keys():
        f2 += hash_map[elem] ** 2
    return f2


def main():
    with codecs.open("test_f2.txt") as file_handle:
        print "F2 is equal to ", bf_f2(file_handle)
    with codecs.open("test_f2.txt") as file_handle:
        print "The estimated F2 is equal to ", estimate_f2(file_handle)


# same probability for even and odd
def my_hash(element):
    if hash(element) % 2 == 0:
        return 1
    else:
        return -1


def estimate_f2(file_handle):
    x = {}
    pos = random.sample(range(0, N), 5)
    pos.sort()
    print pos
    counter = 0
    index = 0
    for line in file_handle:
        line = line.replace("\n", "").replace("\r", "")
        if index < 5 and counter == pos[index]:
            if x.has_key(line):
                pos[index] = pos[index] + 1
            else:
                x[line] = 1
                index += 1
        elif x.has_key(line):
            x[line] = x[line] + 1
        counter += 1
    estimates = []
    print x
    for elem in x.keys():
        estimates.append(N * (2 * x[elem] - 1))
    print estimates
    return numpy.average(estimates)



main()
