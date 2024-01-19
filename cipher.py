from kindierrors import *

alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def rot(ch, n):
    if ch in alphabet_lower:
        init_pos = 97
    elif ch in alphabet_upper:
        init_pos = 65
    else:
        return ch
    pos = ord(ch) - init_pos + n
    pos = pos % 26
    nch = chr(pos+init_pos)

    return nch

def substitution(text, key, arg):
    if isinstance(key, int):
        answer = ""
        if arg == "encode":
            encry = key
        elif arg == "decode":
            encry = - key
        for i in range(len(text)):
            answer += rot(text[i], encry)

        return answer
    

def to_number_key(text, key):
    lower_key = key.lower()
    number_key = []
    for i in range(len(text)):
        key_pos = i % len(lower_key)
        num = ord(lower_key[key_pos]) - ord("a")
        number_key.append(num)
    return number_key


def substsubst(text, key, arg):
    key = key.lower()
    alpha_dict = {}
    for i in range(len(alphabet_lower)):
        if arg == "encode":
            alpha_dict[alphabet_lower[i]] = key[i]
        elif arg == "decode":
            alpha_dict[key[i]] = alphabet_lower[i]
    answer = ""
    for letter in text:
        if letter in alphabet_lower:
            answer += alpha_dict[letter]
        elif letter in alphabet_upper:
            answer += chr(ord(alpha_dict[letter]) - ord("a") + ord("A"))
        else:
            answer += letter
    return answer

def vigenere(text, key, arg):
    number_key = []
    if isinstance(key, int):
        number_key = to_number_key(text, key)
    if isinstance(key, str):
        key = key.lower()
        for i in range(len(text)):
            pos = i % len(key)
            c = key[pos]
            number_key.append(ord(c) - ord("a"))
    answer = ""
    for i in range(len(text)):
        if arg == "encode":
            encry = number_key[i]
        elif arg == "decode":
            encry = - number_key[i]
        answer += rot(text[i], encry)

    return answer

def autokey(text, key, arg):
    if arg == "encode":
        new_key = key + text
        return vigenere(text, new_key, arg)
    elif arg == "decode": 
        number_key = to_number_key(key, key)
        answer = ""
        for i in range(len(text)):
            current = rot(text[i], -number_key[0])
            answer += current
            number_key.append(to_number_key(current, current)[0])
            number_key.pop(0)
        return answer

def one_time_pad(text, key, arg):
    if len(key) >= len(text):
        return vigenere(text, key, arg)
    else:
        error_msg = "Key lenght of incompatible lenght ({}), expected: {}".format(len(key), len(text))
        raise EncryptionKeyLenError(error_msg)
    
# def beaufort(text, key, arg):


# def table(letter):
#     pos = ord("z") - ord(letter)
#     tt = []
#     for i in range(26):
#         new_pos = (pos-i) % 26
#         nletter = chr(new_pos+ ord("a"))
#         tt.append(nletter)
#     print(tt)


def XOR(text, key) -> bytes:
    # exemplo tomado de https://en.wikipedia.org/wiki/XOR_cipher
    """Concate xor two strings together."""
    if len(text) == len(key):
        return bytes([a ^ b for a, b in zip(text, key)])
    else:
        error_msg = "Key lenght of incompatible lenght ({}), expected: {}".format(len(key), len(text))
        raise EncryptionKeyLenError(error_msg)

def call_encrypt_function(crypt, text, key, arg):
    if crypt == "substitution":
        return substitution(text, key, arg)
    elif crypt == "vigenere":
        return vigenere(text, key, arg)
    elif crypt == "autokey":
        return autokey(text, key, arg)
    elif crypt == "one_time_pad":
        return one_time_pad(text, key, arg)
    elif crypt == "XOR":
        return XOR(text, key)
    elif crypt == "substsubst":
        return substsubst(text, key, arg)