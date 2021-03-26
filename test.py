import string


x = "abc-"


first_char  = "A"
permutation = "bc"
x = []
for i in range(len(permutation)+1):
    x += [permutation[0:i] + first_char + permutation[i:]]

# print((hex(id(x))))

# def cp(item):
#     return item.copy()

# print(hex(id(cp(x))))

shift = 13
shifted = {}
# for letter in string.ascii_uppercase:
#     shifted[letter] = chr(((ord(letter) - 65 + shift) % 26) + 65)

for letter in string.ascii_lowercase:
    shifted[letter] = chr(((ord(letter) - 97 + shift) % 26) + 97)
    uppercase = chr(ord(letter) - 32)
    shifted[uppercase] = chr(((ord(letter) - 97 + shift) % 26) + 65)

plaintext = "hello"


message = ""

for char in plaintext:
    if char in shifted:
        message += shifted[char]
    else:
        message += char
print(message) 

