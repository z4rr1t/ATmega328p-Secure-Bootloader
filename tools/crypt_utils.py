from ecdsa import NIST192p
from ecdsa.util import number_to_string
import xxhash
from pwn import enhex

NUM_ECC_DIGITS = 24  # 24 bytes for NIST P-192 curve

def xxhash128(data):
    h = xxhash.xxh128()
    h.update(data)
    return h.digest()


def xxhash128(data):
    h = xxhash.xxh128()
    h.update(data)
    return h.digest()

def ecdsa_sign(p_privateKey, p_random, p_hash):
    private_key = int.from_bytes(p_privateKey, byteorder='little')
    random_k = int.from_bytes(p_random, byteorder='big')
    e = int.from_bytes(p_hash, byteorder='big')
    
    curve = NIST192p
    curve_n = curve.order

    if random_k == 0:
        return 0

    k = random_k % curve_n

    kG = k * curve.generator
    
    r = kG.x() % curve_n
    if r == 0:
        return 0
    
    s = (e + r * private_key) % curve_n
    s = s * pow(k, -1, curve_n) % curve_n
    s = s % curve_n
    
    r_bytes = number_to_string(r, curve.order)
    s_bytes = number_to_string(s, curve.order)

    return r_bytes, s_bytes


def pack_data(data, private_key):
    if isinstance(data, str):
        data = data.encode()

    random = bytearray([1] + [0]*23) # default for now
    xx_hash = b"\x00"*8 + xxhash128(data)
    signature = ecdsa_sign(private_key, random, xx_hash)

    r = signature[0][::-1]
    s = signature[1][::-1]

    return (r + s + data)


if __name__ == "__main__":
    private_key_raw = b"\x64\xF2\x04\xD7\x01\x8B\xCC\xAA\x61\x17\x3E\xB6\xE1\xE8\x15\x3E\x77\xB5\xC8\xA6\x0E\x0B\x9C\xE8" #[::-1]
    data = b"THIS IS NOT RANDOM DATA"
    hash_ = b"\x00"*8 + xxhash128(data)
    print(enhex(hash_[::-1]))
    signature = ecdsa_sign(private_key_raw, bytearray([1] + [0]*23), hash_)

    r = enhex(signature[0][::-1])
    s = enhex(signature[1][::-1])
    print(r)
    print(s)

    print(enhex(pack_data(data, private_key_raw)))


