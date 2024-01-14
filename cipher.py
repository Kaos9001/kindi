# Cifras encontradas em : 
# - https://www.geeksforgeeks.org/substitution-cipher/
# - https://www.geeksforgeeks.org/vigenere-cipher/
import string

def substitution(text, key, arg):
    
    # A list containing all characters
    # all_letters= string.ascii_letters
    lower_letters = string.ascii_lowercase
    upper_letters = string.ascii_uppercase


    dict_lower = {}
    dict_upper = {}

    if isinstance(key, int):
        for i in range(26):
            if arg == "encode":
                new_pos = (i+key)%26
            elif arg == "decode":
                new_pos = (i-key)%26
            dict_lower[lower_letters[i]] = lower_letters[new_pos]
            dict_upper[upper_letters[i]] = upper_letters[new_pos]
    
    else: # caso em que a key é do tipo subst
        for i in range(len(lower_letters)):
            if arg == "encode":
                dict_lower[lower_letters[i]] = key[i]
                dict_upper[upper_letters[i]] = key[i].upper()
            elif arg == "decode":
                dict_lower[key[i]] = lower_letters[i]
                dict_upper[key[i].upper()] = upper_letters[i]



    # este loop gera o nosso texto encriptado afetando apenas os caracteres 
    # de letras romanas
    cipher_txt=[]
    for char in text:
        if char in lower_letters:
            temp = dict_lower[char]
            cipher_txt.append(temp)
        elif char in upper_letters:
            temp = dict_upper[char]
            cipher_txt.append(temp)
        else:
            temp =char
            cipher_txt.append(temp)
            
    new_text= "".join(cipher_txt)
    print(new_text)
    return(new_text)

    alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
    alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"




# Python code to implement
# Vigenere Cipher
 
     
# This function returns the 
# encrypted text generated 
# with the help of the key
def cipherText(text, key_o,arg):

    # A list containing all characters
    # all_letters= string.ascii_letters
    lower_letters = string.ascii_lowercase
    upper_letters = string.ascii_uppercase


    # cria a chave para ter mesmo comprimento do texto
    key = key_o.lower()
    key = list(key)
    if len(text) == len(key):
        return(key)
    elif len(text) > len(key):
        for i in range(len(text) -
                       len(key)):
            key.append(key[i % len(key)])
    else:
        print("?????")
    # key =  "" .join(key)

    cipher_text = []
    for i in range(len(text)):
        x = text[i]
        # print(x)
        if x in upper_letters:
            x = x.lower()
            if arg == "encode":
                x = ord(x) + ord(key[i]) - 97 - 97
            elif arg == "decode":
                print("aaa")
                x = ord(x) - ord(key[i])
            x = x % 26 + ord("A")
            # print("->{}".format(chr(x)))
            cipher_text.append(chr(x).upper())

        elif x in lower_letters:
            if arg == "encode":
                x = ord(x) + ord(key[i])
            elif arg == "decode":
                x = ord(x) - ord(key[i]) + 26
            x = x % 26 + ord("a")
            cipher_text.append(chr(x))
        else: 
            cipher_text.append(x)

    return("" . join(cipher_text))
     
# This function decrypts the 
# encrypted text and returns 
# the original text
def originalText(cipher_text, key):
    orig_text = []
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) -
             ord(key[i])) % 26
        x += ord('A')
        orig_text.append(chr(x))
    return("" . join(orig_text))
     

    
# perm = "jvlxatqdmykhwnzbrgfieocspu"

# encodada = substitution("isto e um teste \n ISTO E UM TESTE", perm, "encode")
# decodada = substitution(encodada, perm, "decode")

a = cipherText("GEEKSFORGEEKS", "AYUSH", "encode")
print(a)
b = cipherText(a, "abc", "decode")
print(b)