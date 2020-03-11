#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64decode, b64encode


def preprocess(key, content, loop):
    if isinstance(content, str):
        content = content.encode()
    try:
        loop = int(loop)
        if loop < 0 or loop > 100:
            raise ValueError
    except ValueError:
        loop = int(str(len(content)/len(key))[-1])
        if not loop:
            loop = int(str(len(content))[0])
    return key.encode(), content, loop


def decrypt(key, content, loop='auto'):
    try:
        content = b64decode(content)
    except:
        return None
    if content == '':
        return None
    elif key == '':
        return content
    else:
        key = key[:1000]
        key, content, loop = preprocess(key, content, loop)
        for _ in range(loop):
            dc = b''
            for i in range(len(content)):
                k = key[i % len(key)]
                dc += bytes([(content[i] - k - int(str(i)[-1]) + 512) % 256])
            content = dc
        return content.decode()


def encrypt(key, content, loop='auto'):
    if content == '':
        return None
    elif key == '':
        return b64encode(content.encode()).decode()
    else:
        key = key[:1000]
        key, content, loop = preprocess(key, content, loop)
        for _ in range(loop):
            ec = b''
            for i in range(len(content)):
                k = key[i % len(key)]
                ec += bytes([(content[i] + k + int(str(i)[-1])) % 256])
            content = ec
        return b64encode(content).decode()
