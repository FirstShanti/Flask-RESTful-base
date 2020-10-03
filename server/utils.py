import hashlib


def encrypt_string(string):
    return hashlib.sha3_256(string.encode()).hexdigest()