#!/usr/bin/env python3

import unittest

from ste import decrypt, encrypt


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_encrypt_decrypt_with_key(self):
        key = 'key'
        message = 'secret message to encrypt'
        cyphertext = encrypt(key, message)
        self.assertEqual(decrypt(key, cyphertext), message)

    def test_encrypt_without_key(self):
        self.assertEqual(encrypt('', 'test'), 'dGVzdA')

    def test_decrypt_without_key(self):
        self.assertEqual(decrypt('', 'dGVzdA'), 'test')


if __name__ == '__main__':
    unittest.main()
