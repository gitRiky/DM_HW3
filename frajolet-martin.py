import codecs

LENGTH_BITMAP = 32


def get_binary_representation(number):
    binary = "{0:b}".format(number)
    while len(binary) < LENGTH_BITMAP:
        binary = "0" + binary
    return binary


# least significant one position, it is equal to the length of the tail
def get_least_sign_bit(number):
    if number == 0:
        return LENGTH_BITMAP
    if type(number) is str:
        b_number = number
    else:
        b_number = get_binary_representation(number)
    # print "Binary representation of hash %d is equal to %s" % (number, b_number)
    return LENGTH_BITMAP - 1 - b_number.rfind("1")


def my_hash(element):
    return (19*hash(element) +1) % 2**32


def estimate_f0(stream):
    bitmap = []
    max_tail = 0
    for i in range(0, LENGTH_BITMAP):
        bitmap.append('0')
    for elem in stream:
        elem = elem.replace("\n", "")
        # print "I'm considering element " + elem
        h_elem = my_hash(elem)
        if h_elem != 0:
            lsb = get_least_sign_bit(h_elem)
            # print "Least significant 1 bit = ", lsb
            # tail = len - 1 - lsb;
            tail = lsb
            if tail > max_tail:
                max_tail = tail
    print "Max tail = ", max_tail
    estimation = 2 ** max_tail
    print "We know that the estimation has to be equal to 2 ^ max_tail"
    return estimation


def main():
    with codecs.open("ip.txt", 'r') as file_handle:
        bf_duplicates(file_handle)
        result = estimate_f0(file_handle)
    print "The number of estimated different elements is ", result


def ip_file():
    counter = 0
    with codecs.open("access_log_Jul95", 'r') as file_handle:
        with codecs.open("ip.txt", 'w') as f_handle:
            for line in file_handle:
                counter += 1
                if counter > 8000:
                    break
                split = line.split(" - - ")
                f_handle.write(split[0])
                f_handle.write("\n")


def bf_duplicates(file_handle):
    dict = {}
    for line in file_handle:
        line = line.replace("\n","")
        if dict.has_key(line):
            dict[line] = dict[line] + 1
        else:
            dict[line] = 1
    for elem in dict.keys():
        print "elem " + elem + ", duplicates = ", dict[elem]
    print "number of different elements = ", len(dict.keys())


main()
