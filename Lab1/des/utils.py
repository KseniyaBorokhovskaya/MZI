import Lab1.des.constants as constants


def string_to_bits_list(string):
    """
        Turns string into the bits (0 or 1) array

    :param string
    :return: bits array
    """
    string_data = string.encode("ascii")
    return bytes_to_bits_list(string_data)


def bytes_to_bits_list(data):
    """
        Turns bytes into the bits (0 or 1) array

    :param data
    :return: bits array
    """
    array_length = len(data) * 8
    result = [0] * array_length

    array_position = 0
    for character in data:
        i = 7
        while i >= 0:
            if character & (1 << i) != 0:
                result[array_position] = 1
            else:
                result[array_position] = 0

            array_position += 1
            i -= 1

    return result


def bits_list_to_bytes(data):
    """
        Turns the bits (0 or 1) array into bytes

    :param data
    :return: bytes array
    """
    result = []
    position = 0
    c = 0
    while position < len(data):
        c += data[position] << (7 - (position % 8))
        if (position % 8) == 7:
            result.append(c)
            c = 0

        position += 1

    return bytes(result)


def generate_sub_keys(key_string):
    """
        Generates sub keys for Feistel function in DES

    :param key_string: encryption key passed as string
    :return: sub_keys for Feistel function in DES
    """

    bites_key = string_to_bits_list(key_string)

    c_block = [bites_key[constants.permuted_choice_1[i]] for i in range(28)]
    d_block = [
        bites_key[constants.permuted_choice_1[i + 28]] for i in range(28)
    ]

    sub_keys = []

    i = 0
    while i < 16:

        j = 0
        while j < constants.bits_rotation_table[i]:
            c_block.append(c_block.pop(0))

            d_block.append(d_block.pop(0))

            j += 1

        c_d_vector = c_block + d_block
        sub_keys.append(
            [c_d_vector[index] for index in constants.permuted_choice_2]
        )

        i += 1

    return sub_keys


def add_padding_to_data(data, block_size, padding_byte=" "):
    """
        Adds the padding to data to be a multiple of block size

    :param data: data to add padding to
    :param block_size: size of the DES block
    :param padding_byte: byte to add to data
    :return: data with padding
    """

    if isinstance(data, str):
        data = data.encode("ascii")

    if padding_byte is not None:
        padding_byte = padding_byte.encode("ascii")

    if len(data) % block_size == 0:
        return data

    data += (block_size - (len(data) % block_size)) * padding_byte

    return data
