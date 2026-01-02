import re

# ✅ Fréquences des lettres anglaises
EN_FREQ_FULL = {
    'E':12.7,'T':9.1,'A':8.2,'O':7.5,'I':7.0,'N':6.7,
    'S':6.3,'H':6.1,'R':6.0,'D':4.3,'L':4.0,'C':2.8,'U':2.8,
    'M':2.4,'W':2.4,'F':2.2,'G':2.0,'Y':2.0,'P':1.9,'B':1.5,
    'V':1.0,'K':0.8,'J':0.15,'X':0.15,'Q':0.10,'Z':0.07
}

# ✅ Liste de mots anglais fréquents
COMMON_WORDS = ["THE", "AND", "OF", "TO", "IN", "IS", "THAT", "THIS", "FOR", "IT", "ON"]

# ✅ Bigrams et trigrams fréquents
COMMON_NGRAMS = ["TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND", "ING", "AND", "THE"]

def english_score(text):
    """
    Score basé sur :
    1. Fréquence des lettres
    2. Présence de mots anglais fréquents
    3. Présence de bigrammes/trigrammes fréquents
    """
    text = text.upper()
    score = 0

    # Nettoyer le texte pour n'avoir que des lettres pour certaines analyses
    letters_only = re.sub(r'[^A-Z]', '', text)

    # 1️⃣ Score basé sur la fréquence des lettres
    for c in letters_only:
        score += EN_FREQ_FULL.get(c, 0)

    # 2️⃣ Bonus pour mots anglais fréquents
    for w in COMMON_WORDS:
        score += len(re.findall(r'\b' + re.escape(w) + r'\b', text)) * 50  # pondération plus forte

    # 3️⃣ Bonus pour bigrammes/trigrammes fréquents
    for ng in COMMON_NGRAMS:
        score += text.count(ng) * 15

    return score
