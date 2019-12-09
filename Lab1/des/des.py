import Lab1.des.constants as constants
import Lab1.des.utils as utils


ENCRYPT = 0
DECRYPT = 1


def encrypt(data, key):
    """
        Encrypts passed data with passed key

    :param data: data to encrypt
    :param key: key to encrypt with
    :return: encrypted data as bytes
    """
    return crypt(data, ENCRYPT, key)


def decrypt(encrypted_data, key):
    """
        Decrypts passed data with passed key

    :param encrypted_data: data to decrypt
    :param key: key to decrypt with
    :return: decrypted data as bytes
    """
    return crypt(encrypted_data, DECRYPT, key)


def crypt(data, crypt_type, key, block_size=8, padding_byte=" "):
    """
        Main DES flow. Separates data in blocks and passes them to DES algorithm.

    :param padding_byte: optional argument for encryption padding. Must only be one byte
    :param key: key to crypt data
    :param data: bits array to encrypt
    :param crypt_type: ENCRYPT or DECRYPT
    :param block_size: the size of data blocks
    :return: crypted data
    """
    data = utils.add_padding_to_data(data, block_size, padding_byte)

    if len(data) % block_size != 0:
        raise ValueError(
            "Invalid data length, data must be a multiple of "
            + str(block_size)
            + " bytes\n"
        )

    sub_keys = utils.generate_sub_keys(key)
    if crypt_type == DECRYPT:
        sub_keys.reverse()

    i = 0
    crypted_data = []
    while i < len(data):
        block = utils.bytes_to_bits_list(data[i : i + block_size])

        crypted_block = des_algorithm(block, sub_keys)

        crypted_data.append(utils.bits_list_to_bytes(crypted_block))

        i += block_size

    return bytes.fromhex("").join(crypted_data)


def des_algorithm(block, sub_keys):
    """
        Crypts block with DES algorithm

    :param sub_keys: keys for des iterations
    :param block: block passed for crypting
    :return: crypted block
    """

    block = [block[index] for index in constants.initial_permutation]

    left_block = block[:32]
    right_block = block[32:]

    i = 0
    while i < 16:
        left_block, right_block = des_algorithm_iteration(
            left_block, right_block, sub_keys[i]
        )

        i += 1

    block = right_block + left_block
    block = [block[index] for index in constants.final_permutation]

    return block


def des_algorithm_iteration(left_block, right_block, iteration_key):
    """
        DES algorithm iteration

    :param left_block: previous left block
    :param right_block: previous right block
    :param iteration_key: key for current iteration
    :return: new left and right blocks
    """
    temp_right_block = right_block[:]

    right_block = [right_block[index] for index in constants.expansion_function]

    right_block = list(map(lambda x, y: x ^ y, right_block, iteration_key))

    six_bits_blocks = [
        right_block[:6],
        right_block[6:12],
        right_block[12:18],
        right_block[18:24],
        right_block[24:30],
        right_block[30:36],
        right_block[36:42],
        right_block[42:],
    ]

    j = 0
    position = 0
    while j < 8:

        m = (six_bits_blocks[j][0] << 1) + six_bits_blocks[j][5]
        n = (
            (six_bits_blocks[j][1] << 3)
            + (six_bits_blocks[j][2] << 2)
            + (six_bits_blocks[j][3] << 1)
            + six_bits_blocks[j][4]
        )
        v = constants.s_boxes[j][(m << 4) + n]

        right_block[position] = (v & 8) >> 3
        right_block[position + 1] = (v & 4) >> 2
        right_block[position + 2] = (v & 2) >> 1
        right_block[position + 3] = v & 1

        position += 4
        j += 1

    right_block = [right_block[index] for index in constants.permutation]

    right_block = list(map(lambda x, y: x ^ y, right_block, left_block))

    left_block = temp_right_block

    return left_block, right_block


if __name__ == "__main__":
    key = "ASDFGHJK"

    with open("text.txt", "r") as file:
        data = file.read()
        encrypted = encrypt(data, key)

        d = decrypt(encrypted, key)
        print(d)
