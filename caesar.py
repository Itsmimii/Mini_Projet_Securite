from utils import ALPHABET

def caesarEncryption(text, k):
    res = ""
    for c in text:
        if c in ALPHABET:
            res += ALPHABET[(ALPHABET.index(c) + k) % 26]
        else:
            res += c
    return res

def caesarDeciphering(text, k):
    return caesarEncryption(text, -k)

def caesarCryptanalysis(ciphertext):
    results = []
    for k in range(1, 26):
        results.append((k, caesarDeciphering(ciphertext, k)))
    return results
