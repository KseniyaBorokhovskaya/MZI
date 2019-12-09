from os import urandom

from pygost.utils import bytes2long
from pygost.utils import hexdec
from pygost.utils import long2bytes
from pygost.utils import modinvert


MODE2SIZE = {
    2001: 32,
    2012: 64,
}


class GOST3410Curve(object):
    def __init__(self, p, q, a, b, x, y, e=None, d=None):
        self.p = p
        self.q = q
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.e = e
        self.d = d
        r1 = self.y * self.y % self.p
        r2 = ((self.x * self.x + self.a) * self.x + self.b) % self.p
        if r1 != self.pos(r2):
            raise ValueError("Invalid parameters")
        self._st = None

    def pos(self, v):
        """Make positive number
        """
        if v < 0:
            return v + self.p
        return v

    def _add(self, p1x, p1y, p2x, p2y):
        if p1x == p2x and p1y == p2y:
            # double
            t = ((3 * p1x * p1x + self.a) * modinvert(2 * p1y, self.p)) % self.p
        else:
            tx = self.pos(p2x - p1x) % self.p
            ty = self.pos(p2y - p1y) % self.p
            t = (ty * modinvert(tx, self.p)) % self.p
        tx = self.pos(t * t - p1x - p2x) % self.p
        ty = self.pos(t * (p1x - tx) - p1y) % self.p
        return tx, ty

    def exp(self, degree, x=None, y=None):
        x = x or self.x
        y = y or self.y
        tx = x
        ty = y
        if degree == 0:
            raise ValueError("Bad degree value")
        degree -= 1
        while degree != 0:
            if degree & 1 == 1:
                tx, ty = self._add(tx, ty, x, y)
            degree = degree >> 1
            x, y = self._add(x, y, x, y)
        return tx, ty

    def st_parameters(self):
        """Compute s/t parameters for twisted Edwards curve points conversion
        """
        if self.e is None or self.d is None:
            raise ValueError("non twisted Edwards curve")
        if self._st is not None:
            return self._st
        self._st = (
            self.pos(self.e - self.d) * modinvert(4, self.p) % self.p,
            (self.e + self.d) * modinvert(6, self.p) % self.p,
        )
        return self._st


CURVES = {
    "GostR3410_2001_ParamSet_cc": GOST3410Curve(
        p=bytes2long(
            hexdec(
                "C0000000000000000000000000000000000000000000000000000000000003C7"
            )
        ),
        q=bytes2long(
            hexdec(
                "5fffffffffffffffffffffffffffffff606117a2f4bde428b7458a54b6e87b85"
            )
        ),
        a=bytes2long(
            hexdec(
                "C0000000000000000000000000000000000000000000000000000000000003c4"
            )
        ),
        b=bytes2long(
            hexdec(
                "2d06B4265ebc749ff7d0f1f1f88232e81632e9088fd44b7787d5e407e955080c"
            )
        ),
        x=bytes2long(
            hexdec(
                "0000000000000000000000000000000000000000000000000000000000000002"
            )
        ),
        y=bytes2long(
            hexdec(
                "a20e034bf8813ef5c18d01105e726a17eb248b264ae9706f440bedc8ccb6b22c"
            )
        ),
    ),
    "id-GostR3410-2001-TestParamSet": GOST3410Curve(
        p=bytes2long(
            hexdec(
                "8000000000000000000000000000000000000000000000000000000000000431"
            )
        ),
        q=bytes2long(
            hexdec(
                "8000000000000000000000000000000150FE8A1892976154C59CFC193ACCF5B3"
            )
        ),
        a=bytes2long(
            hexdec(
                "0000000000000000000000000000000000000000000000000000000000000007"
            )
        ),
        b=bytes2long(
            hexdec(
                "5FBFF498AA938CE739B8E022FBAFEF40563F6E6A3472FC2A514C0CE9DAE23B7E"
            )
        ),
        x=bytes2long(
            hexdec(
                "0000000000000000000000000000000000000000000000000000000000000002"
            )
        ),
        y=bytes2long(
            hexdec(
                "08E2A8A0E65147D4BD6316030E16D19C85C97F0A9CA267122B96ABBCEA7E8FC8"
            )
        ),
    ),
    "id-GostR3410-2001-CryptoPro-A-ParamSet": GOST3410Curve(
        p=bytes2long(
            hexdec(
                "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD97"
            )
        ),
        q=bytes2long(
            hexdec(
                "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6C611070995AD10045841B09B761B893"
            )
        ),
        a=bytes2long(
            hexdec(
                "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD94"
            )
        ),
        b=bytes2long(
            hexdec(
                "00000000000000000000000000000000000000000000000000000000000000a6"
            )
        ),
        x=bytes2long(
            hexdec(
                "0000000000000000000000000000000000000000000000000000000000000001"
            )
        ),
        y=bytes2long(
            hexdec(
                "8D91E471E0989CDA27DF505A453F2B7635294F2DDF23E3B122ACC99C9E9F1E14"
            )
        ),
    ),
    "id-tc26-gost-3410-2012-256-paramSetA": GOST3410Curve(
        p=bytes2long(
            hexdec(
                "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD97"
            )
        ),
        q=bytes2long(
            hexdec(
                "400000000000000000000000000000000FD8CDDFC87B6635C115AF556C360C67"
            )
        ),
        a=bytes2long(
            hexdec(
                "C2173F1513981673AF4892C23035A27CE25E2013BF95AA33B22C656F277E7335"
            )
        ),
        b=bytes2long(
            hexdec(
                "295F9BAE7428ED9CCC20E7C359A9D41A22FCCD9108E17BF7BA9337A6F8AE9513"
            )
        ),
        x=bytes2long(
            hexdec(
                "91E38443A5E82C0D880923425712B2BB658B9196932E02C78B2582FE742DAA28"
            )
        ),
        y=bytes2long(
            hexdec(
                "32879423AB1A0375895786C4BB46E9565FDE0B5344766740AF268ADB32322E5C"
            )
        ),
        e=0x01,
        d=bytes2long(
            hexdec(
                "0605F6B7C183FA81578BC39CFAD518132B9DF62897009AF7E522C32D6DC7BFFB"
            )
        ),
    ),
}
DEFAULT_CURVE = CURVES["id-GostR3410-2001-CryptoPro-A-ParamSet"]


def public_key(curve, prv):
    """ Generate public key from the private one

    :param GOST3410Curve curve: curve to use
    :param long prv: private key
    :returns: public key's parts, X and Y
    :rtype: (long, long)
    """
    return curve.exp(prv)


def sign(curve, prv, digest, mode=2001):
    """ Calculate signature for provided digest

    :param GOST3410Curve curve: curve to use
    :param long prv: private key
    :param digest: digest for signing
    :type digest: bytes, 32 or 64 bytes
    :returns: signature
    :rtype: bytes, 64 or 128 bytes
    """
    size = MODE2SIZE[mode]
    q = curve.q
    e = bytes2long(digest) % q
    if e == 0:
        e = 1
    while True:
        k = bytes2long(urandom(size)) % q
        if k == 0:
            continue
        r, _ = curve.exp(k)
        r %= q
        if r == 0:
            continue
        d = prv * r
        k *= e
        s = (d + k) % q
        if s == 0:
            continue
        break
    return long2bytes(s, size) + long2bytes(r, size)


def verify(curve, pub, digest, signature, mode=2001):
    """ Verify provided digest with the signature

    :param GOST3410Curve curve: curve to use
    :type pub: (long, long)
    :param digest: digest needed to check
    :type digest: bytes, 32 or 64 bytes
    :param signature: signature to verify with
    :type signature: bytes, 64 or 128 bytes
    :rtype: bool
    """
    size = MODE2SIZE[mode]
    if len(signature) != size * 2:
        raise ValueError("Invalid signature length")
    q = curve.q
    p = curve.p
    s = bytes2long(signature[:size])
    r = bytes2long(signature[size:])
    if r <= 0 or r >= q or s <= 0 or s >= q:
        return False
    e = bytes2long(digest) % curve.q
    if e == 0:
        e = 1
    v = modinvert(e, q)
    z1 = s * v % q
    z2 = q - r * v % q
    p1x, p1y = curve.exp(z1)
    q1x, q1y = curve.exp(z2, pub[0], pub[1])
    lm = q1x - p1x
    if lm < 0:
        lm += p
    lm = modinvert(lm, p)
    z1 = q1y - p1y
    lm = lm * z1 % p
    lm = lm * lm % p
    lm = lm - p1x - q1x
    lm = lm % p
    if lm < 0:
        lm += p
    lm %= q
    # This is not constant time comparison!
    return lm == r


def prv_unmarshal(prv):
    """Unmarshal private key

    :param bytes prv: serialized private key
    :rtype: long
    """
    return bytes2long(prv[::-1])


def pub_marshal(pub, mode=2001):
    """Marshal public key

    :type pub: (long, long)
    :rtype: bytes
    """
    size = MODE2SIZE[mode]
    return (long2bytes(pub[1], size) + long2bytes(pub[0], size))[::-1]


def pub_unmarshal(pub, mode=2001):
    """Unmarshal public key

    :type pub: bytes
    :rtype: (long, long)
    """
    size = MODE2SIZE[mode]
    pub = pub[::-1]
    return (bytes2long(pub[size:]), bytes2long(pub[:size]))


def uv2xy(curve, u, v):
    """Convert twisted Edwards curve U,V coordinates to Weierstrass X,Y
    """
    s, t = curve.st_parameters()
    k1 = (s * (1 + v)) % curve.p
    k2 = curve.pos(1 - v)
    x = t + k1 * modinvert(k2, curve.p)
    y = k1 * modinvert(u * k2, curve.p)
    return x % curve.p, y % curve.p


def xy2uv(curve, x, y):
    """Convert Weierstrass X,Y coordinates to twisted Edwards curve U,V
    """
    s, t = curve.st_parameters()
    xmt = curve.pos(x - t)
    u = xmt * modinvert(y, curve.p)
    v = curve.pos(xmt - s) * modinvert(xmt + s, curve.p)
    return u % curve.p, v % curve.p
