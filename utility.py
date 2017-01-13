import hashlib
import codecs
import config


def hash_family(i):
    result_size = config.LENGTH_BITMAP / 4  # how many bytes we want back
    max_len = config.NUM_HASH_FAMILIES  # how long can our i be (in decimal)
    salt = str(i).zfill(max_len)[-max_len:]

    def hash_member(x):
        return hashlib.sha1(x.encode('utf-8') + salt).hexdigest()[-result_size:]
    return hash_member


def init_hash_families(nhf):
    hash_families = []
    for i in range(nhf):
        hash_families.append(hash_family(i))
    return hash_families


def ip_file():
    counter = 0
    with codecs.open("access_log_Jul95", 'r') as file_handle:
        with codecs.open("ip.txt", 'w') as f_handle:
            for line in file_handle:
                counter += 1
                if counter > 100000:
                    break
                split = line.split(" - - ")
                f_handle.write(split[0])
                f_handle.write("\n")


def get_binary_representation(number):
    binary = "{0:b}".format(int(number, 16))  # give me the binary form of the hex representation of number
    while len(binary) < config.LENGTH_BITMAP:
        binary = "0" + binary
    return binary


# least significant one position, it is equal to the length of the tail
def get_least_sign_bit(number):
    if number == 0:
        return config.LENGTH_BITMAP
    b_number = get_binary_representation(number)
    # print "binary = " + b_number
    return config.LENGTH_BITMAP - 1 - b_number.rfind("1")

class proceed:
    def __init__(self):
        self.c = "y"

    def change(self):
        self.c = "n"

    def get_c(self):
        return self.c
