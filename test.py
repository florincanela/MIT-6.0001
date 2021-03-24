
import string
secret_word = "apple"
letters_guessed = ['e', 'i', 'k', 'p', 'r', 's'] 

# def func(secret_word, letters_guessed):
#     output = ""
#     for letter in secret_word:
#       if letter not in letters_guessed:
#         output += "_"
#       else:
#         output += letter
#     return output

# print(func(secret_word, letters_guessed))

# a = 5
# b = 2
# def test(letters_guessed):
#     output = string.ascii_lowercase
#     for letter in letters_guessed:
#         output = output.replace(letter, "")
#     return output
# print(test(letters_guessed))

# guess = input("Please guess a letter: ").lower()

# print(guess)


def match_with_gaps(my_word, other_word):
    
    stripped_word = my_word.replace(" ", "")

    if len(stripped_word) != len(other_word):
      return False

    for i in range(len(stripped_word)):
        if stripped_word[i] != "_":
            if stripped_word[i] != other_word[i]:
                return False
        if stripped_word.count(stripped_word[i]) != other_word.count(other_word[i]):
            return False

    return True




# other_word = "ailed" 
# my_word = "a_ _ le"
# print(match_with_gaps(my_word, other_word))

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open("words.txt", 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

wordlist = load_words()
my_word = "a_ _ le"


def show_possible_matches(my_word):

    output = ""

    for word in wordlist:    
        if match_with_gaps(my_word, word):
            output += word + " "


    if not output:
        print("No matches found")
    
    else:
      print(output)


show_possible_matches(my_word)



