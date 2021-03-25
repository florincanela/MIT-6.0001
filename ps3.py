# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    #first component
    first_component = 0
    for letter in word.lower():
        first_component += SCRABBLE_LETTER_VALUES[letter]

    #second component:
    wordlen = len(word)
    second_component = 7*wordlen - 3*(n-wordlen)
    if second_component < 1:
        return first_component
    
    return first_component * second_component
    
#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    hand["*"] = hand.get("*", 1)
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    output = hand.copy()
    for letter in word.lower():
        if letter in output.keys():
            output[letter] -= 1
            if output[letter] == 0:
                output.pop(letter)
    return output
#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    word = word.lower()

    if "*" not in word:
        if word in word_list:
            for letter in  set(word):
                if letter not in hand.keys():
                    return False
                if word.count(letter) > hand[letter]:
                    return False
            return True

    else:
        for vowel in VOWELS:
            hand_cp = hand.copy()
            word_cp = word.replace("*", vowel)
            hand_cp[vowel] = hand_cp.get(vowel, 0) + hand_cp.pop("*")

            if word_cp in word_list:
                check = []
                for letter in set(word_cp):
                    if letter in hand_cp.keys():
                        if word_cp.count(letter) <= hand_cp[letter]:
                            check.append(1)
                            continue
                    check.append(0)

                if 0 not in check:
                    return True
                    
    return False
#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    return sum(hand.values())
    

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    total_score = 0

    # As long as there are still letters left in the hand:
    while hand:
        # Display the hand
        curr_hand = ""
        for key in hand:
            curr_hand += (key + " ") * hand[key]
        print(f'Current Hand: {curr_hand}')
        # Ask user for input
        inpt = input("Enter word, or '!!' to indicate that your are finished: ")
        # If the input is two exclamation points:
        if inpt == "!!":
            # End the game (break out of the loop)
            print(f"Total score for this hand: {total_score} points ")
            break
            
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(inpt, hand, word_list):
                points = get_word_score(inpt, calculate_handlen(hand))
                total_score += points
                # Tell the user how many points the word earned,
                print(f'"{inpt}" earned {points} points. Total: {total_score} points')
                # and the updated total score

            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("That is not a valid word. Please choose another word.")
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, inpt)
            

    # Game is over (user entered '!!' or ran out of letters),
    else:
        print(f"Ran out of letters. \nTotal score for this hand: {total_score} points ")
    # so tell user the total score


    # Return the total score as result of function
    return total_score



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    hand_cp = hand.copy()
    substitute = random.choice(string.ascii_lowercase)
    while substitute in hand_cp:
        substitute = random.choice(string.ascii_lowercase)
    hand_cp[substitute] = hand_cp.get(substitute, 0) + hand_cp.pop(letter)
    return hand_cp
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    # Asks the user to input a total number of hands
    while True:
        hands_n = input("Enter total number of hands: ")
        try:
            hands_n = int(hands_n)
            break
        except:
            continue

    #setting the total score    
    total_score = 0
    #replay option available at start
    replay_option = True
    #not replaying the hand by default
    replaying = False



    # looping for each hand
    while hands_n:
        curr_hand = deal_hand(HAND_SIZE)
         
        #printable hand
        repr_curr_hand = ""
        for key in curr_hand:
            repr_curr_hand += (key + " ") * curr_hand[key]
        

        #dealing with choices and incorrect input and runs the code if 
        #i'm not currently replaying the hand
        if not replaying:
            print(f"Current hand: {repr_curr_hand}")
            while True:           
                substitute_q = input("Would you like to substitute a letter? ").lower()
                if substitute_q == "no":
                    break
                elif substitute_q == "yes":
                    substitute_letter = input("Which letter would you like to replace: ").lower()
                    while substitute_letter not in curr_hand and not substitute_letter.isalpha():
                        print("Oops! That is not a valid letter.")
                        substitute_letter = input("Which letter would you like to replace: ")
                    curr_hand = substitute_hand(curr_hand, substitute_letter)
                    break
        #if  previous code didn't run means i am replaying this hand
        # thus im restoring replaying back to false for future hands 
        replaying = False
        temp_score = play_hand(curr_hand, word_list)

        print("-" *10)

        #runs if replay option available
        if replay_option:
            replay = input("Would you like to replay the hand? ").lower()
            while True:
                if replay == "yes":
                    #deactivating replay option
                    replay_option = False
                    # saving current score for comparison against next hand
                    last_score = temp_score
                    # not asking for letter substitution next hand
                    replaying = True
                    break
           
                if replay == "no":
                    hands_n -= 1
                    total_score += temp_score
                    break

            continue
        #if not replaying bottom code is never going to run
        #if replaying, lasts_core gets instantiated thus no exceptions is ocurred

        # if a last score was registered, checks against curr temp_score 
        # adding to total score the bigger of two 
        if last_score:
            if last_score > temp_score:
                total_score += last_score
                last_score = 0
                hands_n -= 1        
                continue

        total_score += temp_score
        hands_n -= 1
        
        

    print(f"Total score over all hands: {total_score}")



#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)