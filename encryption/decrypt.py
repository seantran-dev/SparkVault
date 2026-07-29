from . import modes

# from credential
def decrypt_secret(key, credential):
    ciphertext = credential[4]
    nonce = credential[5]
    
    nonce, password = modes.encrypt_CTR(ciphertext, key, nonce)

    return password.decode("utf-8")

# from direct ciphertext + nonce
def decrypt_password(key, ciphertext, nonce):
    nonce, password = modes.encrypt_CTR(ciphertext, key, nonce)

    return password.decode("utf-8")


