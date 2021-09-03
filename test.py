import re

def check(str):
    # _matching the strings
    if re.search(re.compile('^[123]+$'), str):
        print("Valid String")
    else:
        print("Invalid String")


# _driver code
check('453642')
check('349')
