import Lab1.des.des as des


def encrypt(data, first_key, second_key):
    """
        Encrypts passed data with passed keys

    :param data: data to encrypt
    :param first_key: first key to encrypt with
    :param second_key: second key to encrypt with
    :return: encrypted data as bytes
    """

    first_encryption = des.encrypt(data, first_key)
    second_encryption = des.encrypt(first_encryption, second_key)

    return second_encryption


def decrypt(encrypted_data, first_key, second_key):
    """
        Decrypts passed data with passed keys

    :param encrypted_data: data to decrypt
    :param first_key: first key to decrypt with
    :param second_key: second key to decrypt with
    :return: decrypted data as bytes
    """

    first_decryption = des.decrypt(encrypted_data, second_key)
    second_decryption = des.decrypt(first_decryption, first_key)

    return second_decryption
