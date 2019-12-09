from hashlib import md5, sha1, sha256
from zlib import crc32, adler32


class HMAC:
    def __init__(self, key, message, hash_h=md5):

        self.i_key_pad = bytearray()
        self.o_key_pad = bytearray()
        self.key = key
        self.message = message
        self.blocksize = 64
        self.hash_h = hash_h
        self.init_flag = False

    def init_pads(self):

        for i in range(self.blocksize):
            self.i_key_pad.append(0x36 ^ self.key[i])
            self.o_key_pad.append(0x5C ^ self.key[i])

    def init_key(self):

        if len(self.key) > self.blocksize:
            self.key = bytearray(md5(key).digest())
        elif len(self.key) < self.blocksize:
            i = len(self.key)
            while i < self.blocksize:
                self.key += b"\x00"
                i += 1

    def digest(self):

        if self.hash_h == adler32 or self.hash_h == crc32:
            return self.hash_h(
                bytes(self.o_key_pad)
                + str(
                    self.hash_h(bytes(self.i_key_pad) + self.message)
                ).encode()
            )
        # returns a digest, byte object.
        # check if init_flag is set

        if not self.init_flag:
            self.init_key()
            self.init_pads()
            self.init_flag = True

        return self.hash_h(
            bytes(self.o_key_pad)
            + self.hash_h(bytes(self.i_key_pad) + self.message).digest()
        ).digest()

    def hexdigest(self):

        if self.hash_h == adler32 or self.hash_h == crc32:
            return hex(
                self.hash_h(
                    bytes(self.o_key_pad)
                    + str(
                        self.hash_h(bytes(self.i_key_pad) + self.message)
                    ).encode()
                )
            )[2:]
        # returns a digest in hexadecimal.
        # check if init_flag is set

        if not self.init_flag:

            self.init_key()
            self.init_pads()
            self.init_flag = True

        return self.hash_h(
            bytes(self.o_key_pad)
            + self.hash_h(bytes(self.i_key_pad) + self.message).digest()
        ).hexdigest()
