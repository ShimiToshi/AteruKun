
# -*- coding: utf-8 -*-
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Padding

class AESCipher(object):
    def __init__(self, key):
        if type(key) == bytes:
            self.key = key
        elif type(key) == str:
            self.key = bytes.fromhex(key)
        else:
            raise ValueError("Weird Key... %s" % type(key))

    def encrypt(self, raw):
        iv = Random.get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        data = Padding.pad(raw.encode('utf-8'), AES.block_size, 'pkcs7')
        return base64.b64encode(iv + cipher.encrypt(data))

    def decrypt(self, enc):
        print("!!!!!", enc, len(enc), type(enc))
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        data = Padding.unpad(cipher.decrypt(enc[AES.block_size:]), AES.block_size, 'pkcs7')
        return data.decode('utf-8')


import random
import string
from crypt import AESCipher


def random_byte():
    h = hex(random.randint(0, 255))
    if len(h) == 3:
        num = h[-1]
        h = '0x0' + num

    return h

text = 'plain text'
# key = [random_byte() for i in range(32)]
# key = ''.join([i[2:] for i in key])
key = b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
cipher = AESCipher(key)
encrypted = cipher.encrypt(text)
print(encrypted, len(encrypted))  # -> b'MLXpzLheE1383lHyVkGzoppMmO78otn3d0BOgh7WGdw='

decrypted = cipher.decrypt(encrypted)
print(decrypted)  # -> 'plain text'

# obj.encrypt(pad(message, BLOCK_SIZE))
# obj2.decrypt(unpad(ciphertext, BLOCK_SIZE))
#
#
# print("-------------------------")
# msg = "This is the message which will appear when decrypted with the correct key."
# print("key:", key)
# print("message:", msg)
# cipher_msg = cipher.encrypt(msg)
# print(cipher_msg)
# decrypted_msg = cipher.decrypt(cipher_msg)
# print(decrypted_msg)
