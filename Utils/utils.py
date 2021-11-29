from string import ascii_letters, digits
from random import choice, randint

def RandomString(strlen, digit=True):
    randstr = ascii_letters + (digits if digit else '')
    return ''.join([choice(randstr) for _ in range(0,strlen)])

def double_randint(len):
    return list([randint(0,9) for _ in range(0,len)])