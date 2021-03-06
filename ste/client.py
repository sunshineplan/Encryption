#!/usr/bin/python3
# coding:utf-8

from getpass import getpass
from os import name, system

from ste import decrypt, encrypt


def menu():
    print('   * * * * * * * * * * * * * * * * * * * *')
    print('   *                                     *')
    print('   *  Welcome to use Encryption!         *')
    print('   *                                     *')
    print('   *  1. Encrypt                         *')
    print('   *  2. Decrypt                         *')
    print('   *  Q. Quit                            *')
    print('   *                                     *')
    print('   * * * * * * * * * * * * * * * * * * * *')
    print()
    choice = input('Please choose one function:')
    print()
    return choice


def clear():
    system('cls' if name == 'nt' else 'clear')


def pause(mode='normal'):
    print()
    if mode == 'normal':
        prompt = 'Press any key to continue...'
    else:
        prompt = 'Wrong choice! Press any key to choose again!'
    system('echo '+prompt+'&pause>nul' if name ==
           'nt' else '/bin/bash -c "read -n1 -sp \''+prompt+'\'"')


def multiline_input():
    print('Multiline Content(end with EOC):')
    buffer = []
    while True:
        line = input()
        if line == 'EOC':
            break
        buffer.append(line)
    return '\n'.join(buffer)


def client():
    try:
        while True:
            clear()
            choice = menu()
            if choice == '1':
                content = multiline_input()
                key = getpass('Key:')
                ec = encrypt(key, content)
                if ec:
                    print('Encrypted Content:')
                    print(ec)
                else:
                    print('Empty content!')
                pause()
            elif choice == '2':
                content = input('Content:')
                key = getpass('Key:')
                dc = decrypt(key, content)
                if dc:
                    print('Decrypted Content:')
                    print(dc)
                else:
                    print('Empty or Malformed content!')
                pause()
            elif choice.lower() == 'q':
                clear()
                break
            else:
                pause(mode='error')
    except KeyboardInterrupt:
        clear()
