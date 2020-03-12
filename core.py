#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64decode, b64encode
from zlib import compress, decompress


def b64converter(content):
    if isinstance(content, str):
        return b64decode(content + '=' * (len(content) % 4))
    return b64encode(content).decode().replace('=', '')


def preprocess(key, content, loop):
    if isinstance(content, str):
        content = compress(content.encode())
    try:
        loop = int(loop)
        if loop < 0 or loop > 100:
            raise ValueError
    except ValueError:
        loop1 = int(str(len(content)/len(key))[0] + str(len(content)/len(key))[-1])
        loop2 = int(str(len(content)/len(key))[-1] + str(len(content)/len(key))[0])
        if loop1 < loop2:
            loop = loop1 + 100
        else:
            loop = loop2 + 100
    return key.encode(), content, loop


def decrypt(key, content, loop='auto'):
    try:
        content = b64converter(content)
    except:
        return None
    if content == '':
        return None
    elif key == '':
        return content.decode()
    else:
        key = key[:1000]
        key, content, loop = preprocess(key, content, loop)
        for _ in range(loop):
            dc = b''
            for i in range(len(content)):
                k = key[i % len(key)]
                dc += bytes([(content[i] - k - int(str(i)[-1]) + 512) % 256])
            content = dc
        return decompress(content).decode()


def encrypt(key, content, loop='auto'):
    if content == '':
        return None
    elif key == '':
        return b64converter(content.encode())
    else:
        key = key[:1000]
        key, content, loop = preprocess(key, content, loop)
        for _ in range(loop):
            ec = b''
            for i in range(len(content)):
                k = key[i % len(key)]
                ec += bytes([(content[i] + k + int(str(i)[-1])) % 256])
            content = ec
        return b64converter(content)
