#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64decode, b64encode


def decrypt(key, content):
    try:
        content = b64decode(content).decode()
    except:
        return None
    if content == '':
        return None
    elif key == '':
        return content
    else:
        loop = int(str(len(content)/len(key))[-1])
        if not loop:
            loop = int(str(len(content))[0])
        for i in range(loop):
            dc = ''
            for i in range(len(content)):
                k = key[i % len(key)]
                dc += chr((ord(content[i]) - ord(k) -
                           ord(str(i)[-1]) + 1114111*2) % 1114111)
            content = dc
        return dc


def encrypt(key, content):
    if content == '':
        return None
    elif key == '':
        return b64encode(content.encode()).decode()
    else:
        loop = int(str(len(content)/len(key))[-1])
        if not loop:
            loop = int(str(len(content))[0])
        for l in range(loop):
            ec = ''
            for i in range(len(content)):
                k = key[i % len(key)]
                ec += chr((ord(content[i]) + ord(k) +
                           ord(str(i)[-1])) % 1114111)
            content = ec
        return b64encode(ec.encode()).decode()
