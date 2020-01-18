#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64decode, b64encode


def decrypt(key, content):
    dc = ''
    try:
        c = b64decode(content).decode()
    except:
        return None
    for i in range(len(c)):
        k = key[i % len(key)]
        dc += chr((1114111*2 + ord(c[i]) -
                   ord(k) - ord(str(i)[-1])) % 1114111)
    return dc


def encrypt(key, content):
    ec = ''
    for i in range(len(content)):
        k = key[i % len(key)]
        ec += chr((ord(content[i]) + ord(k) + ord(str(i)[-1])) % 1114111)
    return b64encode(ec.encode()).decode()
