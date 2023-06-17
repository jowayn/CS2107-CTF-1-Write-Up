from Crypto.Util.number import long_to_bytes
import random
import os
import csv

with open('ciphertexts.txt', 'r') as file:
    lines = file.readlines()

cipher0 = lines[0].split(": ")[1]
cipher1 = lines[1].split(": ")[1]
cipher2 = lines[2].split(": ")[1]

# Define the xor function
def xor(a, b):
    return bytes(i ^ j for i, j in zip(a, b))

# Define the decrypt function
def decrypt(ct, sessionKey):
    random.seed(sessionKey)
    return xor(random.randbytes(20), ct)[4:]

def lookup(cipher0, cipher1, cipher2):
    n = 3
    c0 = bytes.fromhex(cipher0)
    c1 = bytes.fromhex(cipher1)
    c2 = bytes.fromhex(cipher2)
    ciphertexts = [c0, c1, c2]
    prefix = cipher0[:8]
    print(f"First 4 bytes: {prefix}")
    with open("rainbow_table.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["ciphertext"].startswith(prefix):
                print("Match Found")
                sessionKey = int(row["sessionkey"])
                print(f"sessionkey used: {sessionKey}")

                # Decrypt each ciphertext using the session key
                plaintexts = [decrypt(ct, sessionKey) for ct in ciphertexts]

                # Print the plaintexts
                for i in range(n):
                    my_bytes = plaintexts[i]
                    hex_str = ''.join(['{:02x}'.format(b) for b in my_bytes])
                    print(hex_str)
                break
        else:
            print("No match found")

# call the lookup function with the extracted ciphertexts
lookup(cipher0 ,cipher1, cipher2)
