#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64decode, b64encode
from zlib import compress, decompress

from Cryptodome.Cipher import AES
from Cryptodome.Hash import HMAC, SHA256
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Random import get_random_bytes


def zlib(data):
    if isinstance(data, str):
        compressed = compress(data.encode())
        if len(compressed) > len(data.encode()):
            return data.encode(), b'0'
        return compressed, b'1'
    return decompress(data)


def truncate_iv(iv, ol, tlen):  # ol and tlen in bits
    ivl = len(iv)  # iv length in bytes
    ol = (ol - tlen) // 8
    # "compute the length of the length" (see ccm.js)
    L = 2
    while (L < 4) and ((ol >> (8*L))) > 0:
        L += 1
    if L < 15 - ivl:
        L = 15 - ivl
    return iv[:(15-L)]


def prf(key, salt):
    return HMAC.new(key, salt, SHA256).digest()


def decrypt(key, data):
    data = b64decode(data + '=' * (len(data) % 4))
    if key == '':
        return data.decode()
    salt = data[:8]
    iv = data[8:24]
    key = PBKDF2(key.encode(), salt, count=10000, dkLen=16, prf=prf)
    ciphertext = data[24:-1]
    nonce = truncate_iv(iv, len(ciphertext)*8, 64)
    cipher = AES.new(key, AES.MODE_CCM, nonce=nonce, mac_len=8)
    if data[-1] == b'0'[0]:
        return cipher.decrypt_and_verify(ciphertext[:-8], ciphertext[-8:]).decode()
    return zlib(cipher.decrypt_and_verify(ciphertext[:-8], ciphertext[-8:])).decode()


def encrypt(key, plaintext):
    if key == '':
        return b64encode(plaintext.encode()).decode().replace('=', '')
    salt = get_random_bytes(8)
    iv = get_random_bytes(16)
    key = PBKDF2(key.encode(), salt, count=10000, dkLen=16, prf=prf)
    data, compression = zlib(plaintext)
    nonce = truncate_iv(iv, len(data) * 8, 64)
    cipher = AES.new(key, AES.MODE_CCM, nonce=nonce, mac_len=8)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return b64encode(salt+iv+ciphertext+tag+compression).decode().replace('=', '')
    # return {
    #    'salt': b64encode(salt),
    #    'iter': 10000,
    #    'ks': 128,
    #    'ct': b64encode(ciphertext + tag),
    #    'iv': b64encode(iv),
    #    'cipher': 'aes',
    #    'mode': 'ccm',
    #    'adata': '',
    #    'v': 1,
    #    'ts': 64
    # }


def encrypt_old(key, data):
    if data == '':
        return None
    elif key == '':
        return b64encode(data.encode()).decode()
    else:
        data = data.encode()
        ec = b''
        for i in range(len(data)):
            k = key[i % len(key)]
            ec += bytes([(data[i] + k) % 256])
        return b64encode(ec).decode()
