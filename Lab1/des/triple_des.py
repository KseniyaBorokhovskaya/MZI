import Lab1.des.des as des


def encrypt(data, first_key, second_key, third_key=None):
    """
        Encrypts passed data with passed keys

    :param data: data to encrypt
    :param first_key: first key to encrypt with
    :param second_key: second key to encrypt with
    :param third_key: second key to encrypt with
    :return: encrypted data as bytes
    """

    if third_key is None:
        third_key = first_key

    first_encryption = des.encrypt(data, first_key)
    second_encryption = des.encrypt(first_encryption, second_key)
    third_encryption = des.encrypt(second_encryption, third_key)

    return third_encryption


def decrypt(encrypted_data, first_key, second_key, third_key=None):
    """
        Decrypts passed data with passed keys

    :param encrypted_data: data to decrypt
    :param first_key: first key to decrypt with
    :param second_key: second key to decrypt with
    :param third_key: second key to decrypt with
    :return: decrypted data as bytes
    """

    if third_key is None:
        third_key = first_key

    first_decryption = des.decrypt(encrypted_data, third_key)
    second_decryption = des.decrypt(first_decryption, second_key)
    third_decryption = des.decrypt(second_decryption, first_key)

    return third_decryption
