from collections import Counter
from utils import ALPHABET
from language_score import english_score
def vigenereDecrypt(text, key):
    res = ""
    k = 0
    for c in text:
        if c in ALPHABET:
            shift = ALPHABET.index(key[k % len(key)])
            res += ALPHABET[(ALPHABET.index(c) - shift) % 26]
            k += 1
        else:
            res += c
    return res

def getSequences(text, n):
    seqs = {}
    for i in range(len(text) - n):
        seq = text[i:i+n]
        seqs.setdefault(seq, []).append(i)
    return [s for s in seqs if len(seqs[s]) > 1]

def getSequenceDistance(text, seq):
    positions = [i for i in range(len(text)) if text.startswith(seq, i)]
    return [positions[i+1] - positions[i] for i in range(len(positions)-1)]

def getDivisions(x):
    return [i for i in range(2, x+1) if x % i == 0]

def getKeyLengthCandidates(ciphertext, top=5):
    distances = []
    for n in range(3, min(10, len(ciphertext)//2)):
        for seq in getSequences(ciphertext, n):
            distances += getSequenceDistance(ciphertext, seq)

    divisors = Counter()
    for d in distances:
        for div in getDivisions(d):
            if div <= 16:   # limite raisonnable
                divisors[div] += 1

    return [d for d, _ in divisors.most_common(top)]


def find_key(ciphertext, key_len):
    key = ""

    for i in range(key_len):
        column = ciphertext[i::key_len]

        best_shift = 0
        best_score = float("-inf")

        for shift in range(26):
            decrypted = ""
            for c in column:
                decrypted += ALPHABET[(ALPHABET.index(c) - shift) % 26]

            score = english_score(decrypted)
            if score > best_score:
                best_score = score
                best_shift = shift

        key += ALPHABET[best_shift]

    return key
