import hashlib
import codecs


LENGTH_BITMAP = 64
NUM_HASH_FAMILIES = 20


def hash_family(i):
    result_size = LENGTH_BITMAP / 4  # how many bytes we want back
    max_len = NUM_HASH_FAMILIES  # how long can our i be (in decimal)
    salt = str(i).zfill(max_len)[-max_len:]

    def hash_member(x):
        return hashlib.sha1(x + salt).hexdigest()[-result_size:]
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
