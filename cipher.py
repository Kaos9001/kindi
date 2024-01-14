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

def vigenere(text, key, arg):
    number_key = to_number_key(text, key)
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




a = autokey("attackatdawn", "QUEENLY", "encode")
print(a)
b = autokey(a, "QUEENLY", "decode")
print(b)