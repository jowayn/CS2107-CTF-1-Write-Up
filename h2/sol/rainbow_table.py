import pandas as pd
import random

def xor(a, b):
    return bytes((i ^ j) for i, j in zip(a, b))

def encrypt(allones, sessionKey):
    random.seed(sessionKey)
    return xor(random.randbytes(20), allones)

# Initialize dataframe
df = pd.DataFrame(columns=["sessionkey", "ciphertext"])

# Iterate through all possible session keys
for i in range(2**24):
    session_key = i
    ciphertext = encrypt(b'\xFF'*4, session_key)  #Generate ciphertext
    df = df.append({"sessionkey": session_key, "ciphertext": ciphertext.hex()}, ignore_index=True)
    print(i)

# Save the DataFrame to csv
df.to_csv("rainbow_table.csv", index=False)
