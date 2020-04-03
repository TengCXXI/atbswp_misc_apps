#! python3
# password_detection.py - Allows user to enter a password and check whether it is strong based on the criteria below.
# Created by Teng Mao @https://github.com/TengCXXI

import re

# Create a while loop that asks user to enter a password until a strong one is entered
while True:
    print("""Please enter a password that is:
        *at least 8 characters long
        *contains both uppercase and lowercase characters
        *has at least one digit""")

    password = input()

    pass_length = re.compile(r'\w{8,}').search(password) != None    # Checks password is at least 8 characters long
    pass_upper = re.compile(r'[A-Z]').search(password) != None      # Checks password has upper case
    pass_lower = re.compile(r'[a-z]').search(password) != None      # Checks password has lower case
    pass_digit = re.compile(r'[0-9]').search(password) != None      # Checks password has at least one digit

    pass_strong = pass_length and pass_upper and pass_lower and pass_digit # Combines boolean for all checks

    if pass_strong == True:
        print("Your password is strong!")
        break
    else:
        continue
