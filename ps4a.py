# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    #base case : of only one char -will be returned as a list for permutations
    #for the previous call waiting on stack
    if len(sequence) == 1:
        return [sequence]

    #recursive call return all permutation without first char
    result = get_permutations(sequence[1:])
    # saving first char  for inserting in each permutation
    first_char = sequence[0]

    # new list were im appending all possible permutation of first char in return list
    new_result = []

    for permutation in result:
        for i in range(len(permutation)+1):
            # first tought
            # new_word = list(permutation)
            # new_word.insert(i, first_char)
            # new_result.append("".join(new_word))

            #less function calls/less space alocated
            new_result.append(permutation[0:i] + first_char + permutation[i:])

    # returning the newly formed permutations list for previous recursive call 
    # waiting on stack //if not last call     
    return new_result
            

if __name__ == '__main__':
#    #EXAMPLE
   example_input = "aeiou"
   print('Input:', example_input)
   print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
   x = get_permutations(example_input)
   print('Actual Output:', x)
   n = len(x)
   print(n) 
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

