import base64
import hashlib
import hmac
import random
import textwrap
from Crypto.Cipher import AES
from Crypto.Util import Counter
import pycoin.ecdsa
from pycoin.ecdsa import generator_secp256k1 as SECP256k1, generator_secp256k1

__author__ = 'ktn'


def point(x, y):
    return pycoin.ecdsa.Point(pycoin.ecdsa.generator_secp256k1.curve(), x, y)


def pad(message, block_size):
    num = block_size - len(message) % block_size
    return message + bytes([num] * num)


def unpad(message, block_size):
    if (len(message) == 0 or
                len(message) < message[-1] or
                message[-1] > block_size):
        raise 1  # Needs to be the same as the MAC verification failing

    if any(x != message[-1] for x in message[-message[-1]:]):
        raise 1  # Needs to be the same as the MAC verification failing

    return message[:-message[-1]]


def encode_point(p, compressed=False):
    x_str = p.x().to_bytes(32, 'big')
    if compressed:
        return bytes([2 if (p.y() & 1) == 0 else 3]) + x_str
    else:
        y_str = p.y().to_bytes(32, 'big')
        return bytes([4]) + x_str + y_str


def decode_point(p):
    # See http://www.secg.org/download/aid-780/sec1-v2.pdf section 2.3.4
    curve = SECP256k1.curve()
    order = SECP256k1.order()
    baselen = 32

    if p[0] == 4:
        # 3
        x_str = p[1:baselen + 1]
        y_str = p[baselen + 1:]
        return point(int.from_bytes(x_str, 'big'), int.from_bytes(y_str, 'big'))
    else:
        # 2.3
        if p[0] == 2:
            yp = 0
        elif p[0] == 3:
            yp = 1
        else:
            return None
        # 2.2
        x_str = p[1:baselen + 1]
        x = int.from_bytes(x_str, 'big')
        # 2.4.1
        alpha = ((x * x * x) + (curve.a() * x) + curve.b()) % curve.p()
        beta = pycoin.ecdsa.numbertheory.modular_sqrt(alpha, curve.p())
        if (beta - yp) % 2 == 0:
            y = beta
        else:
            y = curve.p() - beta
        return point(x, y)


def encrypt(point, message):
    message = message.encode('utf-8')
    padded = pad(message, AES.block_size)
    r = random.SystemRandom().randint(0, SECP256k1.order())
    R = SECP256k1 * r
    S = (point * r).x()
    S_bytes = S.to_bytes((S.bit_length() + 7) // 8, 'big')
    k_E = hashlib.sha256(S_bytes + b'\0\0\0\1').digest()
    k_M = hashlib.sha256(S_bytes + b'\0\0\0\2').digest()
    prefix_bytes = random.SystemRandom().getrandbits(64).to_bytes(8, 'little')
    ctr = Counter.new(64, prefix=prefix_bytes)
    cipher = AES.new(key=k_E, mode=AES.MODE_CTR, counter=ctr)
    c = cipher.encrypt(padded)
    d = hmac.new(k_M, prefix_bytes + c, hashlib.sha256).digest()
    result = base64.b64encode(encode_point(R, True) + d + prefix_bytes + c).decode('utf-8')
    return textwrap.fill(result, 40)


def decrypt(secret, message):
    message = message.encode('utf-8')
    curve = SECP256k1.curve()
    order = SECP256k1.order()
    R_size = 1 + 32
    mac_size = hashlib.sha256().digest_size

    message_binary = base64.b64decode(message)
    if len(message_binary) < (R_size + mac_size):
        return None

    R = decode_point(message_binary)
    d = message_binary[R_size:R_size + mac_size]
    prefix_bytes = message_binary[R_size + mac_size:R_size + mac_size + 8]
    c = message_binary[R_size + mac_size + 8:]
    S = (secret * R).x()
    S_bytes = S.to_bytes(32, 'big')
    k_E = hashlib.sha256(S_bytes + b'\0\0\0\1').digest()
    k_M = hashlib.sha256(S_bytes + b'\0\0\0\2').digest()
    d_verify = hmac.new(k_M, prefix_bytes + c, hashlib.sha256).digest()
    if d_verify != d:
        return None
    ctr = Counter.new(64, prefix=prefix_bytes)
    cipher = AES.new(key=k_E, mode=AES.MODE_CTR, counter=ctr)
    padded = cipher.decrypt(c)
    try:
        return unpad(padded, AES.block_size).decode('utf-8')
    except:
        return None

