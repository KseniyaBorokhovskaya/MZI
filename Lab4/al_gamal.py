import random


class PrivateKey(object):
    def __init__(self, p=None, g=None, x=None, num_bits=0):
        self.p = p
        self.g = g
        self.x = x
        self.num_bits = num_bits


class PublicKey(object):
    def __init__(self, p=None, g=None, y=None, num_bits=0):
        self.p = p
        self.g = g
        self.y = y
        self.num_bits = num_bits


def greatest_common_denominator(a, b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a


def modexp(base, exp, modulus):
    return pow(base, exp, modulus)


def solovay_strassen_primality_test(num, confidence):
    for i in range(confidence):
        a = random.randint(1, num - 1)

        if greatest_common_denominator(a, num) > 1:
            return False

        if not compute_jacobi(a, num) % num == modexp(a, (num - 1) // 2, num):
            return False

    return True


def compute_jacobi(a, n):
    if a == 0:
        if n == 1:
            return 1
        else:
            return 0
    elif a == -1:
        if n % 2 == 0:
            return 1
        else:
            return -1
    elif a == 1:
        return 1
    elif a == 2:
        if n % 8 == 1 or n % 8 == 7:
            return 1
        elif n % 8 == 3 or n % 8 == 5:
            return -1
    elif a >= n:
        return compute_jacobi(a % n, n)
    elif a % 2 == 0:
        return compute_jacobi(2, n) * compute_jacobi(a // 2, n)
    else:
        if a % 4 == 3 and n % 4 == 3:
            return -1 * compute_jacobi(n, a)
        else:
            return compute_jacobi(n, a)


def find_primitive_root(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p - 1) // p1

    while 1:
        g = random.randint(2, p - 1)
        if not (modexp(g, (p - 1) // p1, p) == 1):
            if not modexp(g, (p - 1) // p2, p) == 1:
                return g


def find_prime(num_bits, confidence):
    while 1:
        p = random.randint(2 ** (num_bits - 2), 2 ** (num_bits - 1))

        while not solovay_strassen_primality_test(p, confidence):
            p = random.randint(2 ** (num_bits - 2), 2 ** (num_bits - 1))
            while p % 2 == 0:
                p = random.randint(2 ** (num_bits - 2), 2 ** (num_bits - 1))

        p = p * 2 + 1
        if solovay_strassen_primality_test(p, confidence):
            return p


def generate_keys(num_bits=256, confidence=32):
    p = find_prime(num_bits, confidence)
    g = find_primitive_root(p)
    g = modexp(g, 2, p)
    x = random.randint(2, p - 1)
    y = modexp(g, x, p)

    public_key = PublicKey(p, g, y, num_bits)
    private_key = PrivateKey(p, g, x, num_bits)

    return {"private_key": private_key, "public_key": public_key}


def encrypt(key, plain_text):
    z = bytearray(plain_text, "utf-8")

    cipher_pairs = []
    for i in z:
        k = random.randint(2, key.p - 1)
        a = modexp(key.g, k, key.p)
        b = (i * modexp(key.y, k, key.p)) % key.p
        cipher_pairs.append([a, b])

    encrypted_str = ""
    for pair in cipher_pairs:
        encrypted_str += str(pair[0]) + " " + str(pair[1]) + " "

    return encrypted_str


def decrypt(key, cipher):
    plain_text = []

    cipher_array = cipher.split()
    if not len(cipher_array) % 2 == 0:
        return "Malformed Cipher Text"
    for i in range(0, len(cipher_array), 2):
        a = int(cipher_array[i])
        b = int(cipher_array[i + 1])

        s = modexp(a, key.x, key.p)
        plain = (b * modexp(s, key.p - 2, key.p)) % key.p
        plain_text.append(plain)

    decrypted_text = bytearray(plain_text).decode("utf-8")

    return decrypted_text


def main():
    keys = generate_keys()
    private = keys["private_key"]
    public = keys["public_key"]
    message = "Hello, it's AlGamal"
    cipher = encrypt(public, message)
    print("Encrypted:", cipher)
    plain = decrypt(private, cipher)
    print("Decrypted:", plain)

    print("Correct" if plain == message else "Incorrect")


if __name__ == "__main__":
    main()
