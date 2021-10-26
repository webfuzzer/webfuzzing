from string import ascii_letters, digits
from random import choice

def RandomString(strlen, digit=True):
    return ''.join([choice(ascii_letters + (digits if digit else '')) for _ in range(0,strlen)])