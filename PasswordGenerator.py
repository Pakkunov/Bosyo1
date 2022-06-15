
import string
import secrets
import os
while True:
    
    
    
    alphabet = string.hexdigits + string.punctuation + string.ascii_letters
    password = ''.join(secrets.choice(alphabet) for i in range(50))
    print(password)
    print("Are you satisfied with your password?")
    choice = input("y/n: ")
    if choice == 'y':
        break
