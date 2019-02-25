def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for val in plaintext:
        x = ord(val)
        if(x >= 88) & (x <= 90):
            ciphertext = str(ciphertext) + chr(65-(90-(x+2)))
        elif (x >= 120) & (x <= 122):
            ciphertext = str(ciphertext) + chr(97-(122-(x+2)))
        elif((x >= 65) & (x <= 87)) | ((x >= 97) & (x <= 119)):
            ciphertext = str(ciphertext) + chr(x+3)
        else:
            ciphertext = str(ciphertext) + chr(x)
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for val in ciphertext:
        x = ord(val)
        if ((x >= 97) & (x <= 99)) | ((x >= 65) & (x <= 67)):
            plaintext = str(plaintext) + chr(x + 23)
        elif ((x >= 68) & (x <= 90)) | ((x >= 99) & (x <= 122)):
            plaintext = str(plaintext) + chr(x - 3)
        else:
            plaintext = str(plaintext) + chr(x)
    return plaintext
