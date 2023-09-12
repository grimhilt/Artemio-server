import os
import random
import string

SECRET_KEY_FILE = './config/SECRET_KEY'

def get_secret_key():
    if os.path.isfile(SECRET_KEY_FILE):
        # read the secret key from the file
        with open(SECRET_KEY_FILE, 'r') as file:
            secret_key = file.read().strip()
        return secret_key
    else:
        # generate a new secret key
        secret_key = os.urandom(24)
        # save it to the file
        with open(SECRET_KEY_FILE, 'w') as file:
            file.write(str(secret_key))
        return secret_key
