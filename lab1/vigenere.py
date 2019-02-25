def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    plaintext = str(plaintext)
    ciphertext = ""
    for i in range(len(plaintext)):
        code = ord(keyword[i % len(keyword)])
        chr(code)
        if (code >= 65) & (code <= 90):
            code = code - 65
        elif (code >= 97) & (code <= 122):
            code = code - 97
        x = ord(plaintext[i])
        if (x >= (91 - code)) & (x <= 90):
            ciphertext = str(ciphertext) + chr(65 - (90 - (x + code-1)))
        elif (x >= (123-code)) & (x <= 122):
            ciphertext = str(ciphertext) + chr(97 - (122 - (x + code-1)))
        elif ((x >= 65) & (x <= 90 - code)) | ((x >= 97) & (x <= 122-code)):
            ciphertext = str(ciphertext) + chr(x+code)
        else:
            ciphertext = ciphertext + chr(ord(plaintext[i]))

    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    ciphertext = str(ciphertext)
    for i in range(len(ciphertext)):
        code = ord(keyword[i % len(keyword)])
        chr(code)
        if (code >= 65) & (code <= 90):
            code = code - 65
        elif (code >= 97) & (code <= 122):
            code = code - 97
        x = ord(ciphertext[i])
        if ((x >= 97) & (x <= (96 + code))) | ((x >= 65) & (x <= (64 + code))):
            plaintext = str(plaintext) + chr(x + (26 - code))
        elif ((x >= 65 + code) & (x <= 90)) | ((x >= 97 + code) & (x <= 122)):
            plaintext = str(plaintext) + chr(x - code)
        else:
            plaintext = str(plaintext) + chr(x)
    return plaintext
