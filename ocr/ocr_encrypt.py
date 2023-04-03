import os


def encrypt_file(key, tgt_txt):
    pass


def decrypt_file(key, tgt_txt):
    pass


encrypt_key = input('input encryption key string:')
files = os.listdir('texts')
for file in files:
    if file.endswith('.txt'):
        encrypt_file(encrypt_key, os.path.join('texts', file))
    elif file.endswith('.xmas'):
        decrypt_file(encrypt_key, os.path.join('texts', file))
