#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64decode, b64encode


def get_loop(key, content, loop):
    try:
        loop = int(loop)
        if loop < 0 or loop > 99999:
            raise ValueError
    except ValueError:
        loop = int(str(len(content)/len(key))[-1])
        if not loop:
            loop = int(str(len(content))[0])
    return loop


def decrypt(key, content, loop='auto'):
    try:
        content = b64decode(content).decode()
    except:
        return None
    if content == '':
        return None
    elif key == '':
        return content
    else:
        key = key[:1000]
        loop = get_loop(key, content, loop)
        for _ in range(loop):
            dc = ''
            for i in range(len(content)):
                k = key[i % len(key)]
                dc += chr((ord(content[i]) - ord(k) -
                           ord(str(i)[-1]) + 1114111*2) % 1114111)
            content = dc
        return content


def encrypt(key, content, loop='auto'):
    if content == '':
        return None
    elif key == '':
        return b64encode(content.encode()).decode()
    else:
        key = key[:1000]
        loop = get_loop(key, content, loop)
        for _ in range(loop):
            ec = ''
            for i in range(len(content)):
                k = key[i % len(key)]
                ec += chr((ord(content[i]) + ord(k) +
                           ord(str(i)[-1])) % 1114111)
            content = ec
        return b64encode(content.encode()).decode()
