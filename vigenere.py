from collections import Counter
from utils import ALPHABET
from language_score import english_score

# 🔹 Déchiffrement Vigenère
def vigenereDecrypt(text, key):
    """
    Déchiffre un texte avec la clé Vigenère.
    text : texte chiffré (chaîne)
    key : clé utilisée pour le chiffrement
    """
    res = ""
    k = 0  # index pour parcourir la clé
    for c in text:
        if c in ALPHABET:
            shift = ALPHABET.index(key[k % len(key)])  # valeur de décalage correspondant à la lettre de la clé
            # appliquer le décalage inversé pour déchiffrer
            res += ALPHABET[(ALPHABET.index(c) - shift) % 26]
            k += 1  # passer à la lettre suivante de la clé
        else:
            res += c  # laisser les caractères non alphabétiques inchangés
    return res


# 🔹 Trouver les séquences répétées de longueur n dans le texte
def getSequences(text, n):
    """
    Retourne toutes les séquences de longueur n qui apparaissent plus d'une fois dans le texte.
    text : texte chiffré
    n : longueur de la séquence
    """
    seqs = {}
    for i in range(len(text) - n):
        seq = text[i:i+n]  # extraire la séquence
        seqs.setdefault(seq, []).append(i)  # enregistrer les positions
    # ne garder que les séquences répétées
    return [s for s in seqs if len(seqs[s]) > 1]


# 🔹 Calculer les distances entre occurrences successives d'une séquence
def getSequenceDistance(text, seq):
    """
    Retourne les distances entre positions successives de la séquence seq dans le texte.
    text : texte chiffré
    seq : séquence répétée
    """
    positions = [i for i in range(len(text)) if text.startswith(seq, i)]
    return [positions[i+1] - positions[i] for i in range(len(positions)-1)]


# 🔹 Diviseurs d'un nombre
def getDivisions(x):
    """
    Retourne tous les diviseurs d'un entier x (>=2).
    Utile pour trouver les longueurs de clé possibles.
    """
    return [i for i in range(2, x+1) if x % i == 0]


# 🔹 Trouver les longueurs de clé candidates pour Vigenère
def getKeyLengthCandidates(ciphertext, top=5):
    """
    Utilise la méthode de Kasiski pour proposer des longueurs de clé probables.
    ciphertext : texte chiffré
    top : nombre de longueurs de clé à retourner
    """
    distances = []
    # chercher les séquences répétées de longueur 3 à 9
    for n in range(3, min(10, len(ciphertext)//2)):
        for seq in getSequences(ciphertext, n):
            distances += getSequenceDistance(ciphertext, seq)

    # compter la fréquence des diviseurs de ces distances
    divisors = Counter()
    for d in distances:
        for div in getDivisions(d):
            if div <= 16:   # limite raisonnable pour la longueur de la clé
                divisors[div] += 1

    # retourner les longueurs de clé les plus probables
    return [d for d, _ in divisors.most_common(top)]


# 🔹 Trouver la clé de Vigenère à partir de la longueur
def find_key(ciphertext, key_len):
    """
    Détermine la clé la plus probable pour une longueur de clé donnée.
    ciphertext : texte chiffré
    key_len : longueur de la clé à tester
    """
    key = ""

    # analyser chaque "colonne" du texte découpé par key_len
    for i in range(key_len):
        column = ciphertext[i::key_len]  # toutes les lettres correspondant à la position i modulo key_len

        best_shift = 0
        best_score = float("-inf")

        # tester tous les décalages possibles pour cette colonne
        for shift in range(26):
            decrypted = ""
            for c in column:
                decrypted += ALPHABET[(ALPHABET.index(c) - shift) % 26]

            # scorer le texte déchiffré pour estimer sa "probabilité" en anglais
            score = english_score(decrypted)
            if score > best_score:
                best_score = score
                best_shift = shift

        # ajouter la lettre de clé correspondant au meilleur décalage
        key += ALPHABET[best_shift]

    return key
