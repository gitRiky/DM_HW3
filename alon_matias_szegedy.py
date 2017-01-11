import codecs
import random
import utility
import numpy


N = 320000
FILE_NAME = "ip.txt"
VARIABLES_NUM = 100


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
    output = file("output_f2_ip_3.txt", 'w')
    with codecs.open(FILE_NAME) as file_handle:
        result = bf_f2(file_handle)
        output.write("Exact value for f2 = " + str(result) + "\n")
    with codecs.open(FILE_NAME) as file_handle:
        estim = estimate_f2(file_handle)
        output.write("Estimation for f2 using X_i with var = " + str(VARIABLES_NUM) + " is " + str(estim) + "\n")
    with codecs.open(FILE_NAME) as file_handle:
        result = f2_with_sketch(file_handle)
        output.write("Estimation for f2 using sketch with var = " + str(VARIABLES_NUM) + " is " + str(result))
    output.close()


# same probability for even and odd
def my_hash(element):
    if hash(element) % 2 == 0:
        return 1
    else:
        return -1


def estimate_f2(file_handle):
    x = {}
    pos = random.sample(range(0, N), VARIABLES_NUM)
    pos.sort()
    counter = 0
    index = 0
    for line in file_handle:
        line = line.replace("\n", "").replace("\r", "")
        if index < VARIABLES_NUM and counter == pos[index]:
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


def f2_with_sketch(file_handle):
    z = [0] * VARIABLES_NUM
    hash_functions = utility.init_hash_families(VARIABLES_NUM)
    for line in file_handle:
        line = line = line.replace("\n", "").replace("\r", "")
        for i in range(0, VARIABLES_NUM):
            z[i] += my_hash(hash_functions[i](line))
    estimates = []
    for elem in z:
        estimates.append(elem ** 2)
    return numpy.average(estimates)

main()
