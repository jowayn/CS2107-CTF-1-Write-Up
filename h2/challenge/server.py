#!/usr/local/bin/python

import os
import random
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long

# xor 2 bytes
def xor(a, b):
    return bytes((i ^ j) for i, j in zip(a, b))

def encrypt(pt, sessionKey):
    pt = b'\xFF' * 4 + pt
    random.seed(sessionKey)
    return xor(random.randbytes(20), pt)
    
flag = "REDACTED"
n = 3

masterKey = os.urandom(16)
plaintexts  = [os.urandom(16) for _ in range(n)]

# AES encryption with Master Key and v to get t
aes = AES.new(masterKey, AES.MODE_ECB)
t_bytes = aes.encrypt(b'\x00' * 16)
                   
# Extract 3-byte sessionKey from t
sessionKey = bytes_to_long(t_bytes) & 0xFFFFFF
print(sessionKey)

# FASTencryption Version Alpha
ciphertexts = [encrypt(pt, sessionKey) for pt in plaintexts]

for i in range(n):
    print("Ciphertext%d in hex: %s" %(i, ciphertexts[i].hex()))

for i in range(n):
    userIn = input(f"\nPlease enter Plaintext{i} in hex without 0x at the start: ")
    if (bytes.fromhex(userIn) != plaintexts[i]):
        print("Wrong plaintext, try again!")
        exit(0)

print(f"Congrats! Here is your flag! \n{flag}")

