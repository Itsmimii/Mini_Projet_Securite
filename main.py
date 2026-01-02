from utils import clean_text
from caesar import caesarCryptanalysis
from vigenere import getKeyLengthCandidates, find_key, vigenereDecrypt
from language_score import english_score
from utils import restore_spaces, saveSpacesIndex

def break_cipher(ciphertext):
    text = clean_text(ciphertext)
    spaces = saveSpacesIndex(ciphertext)

    # 🔹 Caesar attempt
    caesar_results = caesarCryptanalysis(text)
    best_caesar = max(caesar_results, key=lambda x: english_score(x[1]))

    # 🔹 Vigenere attempt
    best_vigenere = ("", "", 0)
    text = text.replace(" ", "")  # Vigenère sans espaces

    for klen in getKeyLengthCandidates(text):
        key = find_key(text, klen)
        plain = vigenereDecrypt(text, key)
        score = english_score(plain)

        if score > best_vigenere[2]:
            best_vigenere = (key, plain, score)

    vigenere_key, vigenere_plain, vigenere_score = best_vigenere


    # 🔹 Decision logic
    if english_score(best_caesar[1]) > vigenere_score:
        return {
            "cipher": "CAESAR",
            "key": best_caesar[0],
            "plaintext": best_caesar[1]
        }
    else:
        return {
            "cipher": "VIGENERE",
            "key": vigenere_key,
            "plaintext": restore_spaces(vigenere_plain, spaces)
        }

# ===== RUN =====
if __name__ == "__main__":
    cipher = input("Enter ciphertext:\n")
    result = break_cipher(cipher)

    print("\n🔐 Cipher detected:", result["cipher"])
    print("🔑 Key:", result["key"])
    print("📜 Plaintext:\n", result["plaintext"])
