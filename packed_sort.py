# jamb 2017

N = 16
b = 4  # log n
W = 40 # TODO should be (b+1)*b*logb*2


# input: list of elems to sort
# output: sorted list of them
def packed_sort(elems):
    # pack into large words via word-level mergesort
    base_case_merge()
    # recursively merge sorted lists of words into twice-as-large lists
    merge_lists()
    # extract from the words back into a list
    pass

# input: list of elems to sort
# output: list of words with sorted elems packed into them
def base_case_merge(elems):
    pass

# input: list of words with sorted elems
# output: list of words with sorted elems such that the whole thing is sorted
def merge_lists(words):
    pass

# input: word with sorted elems
# output: two first-half-empty words, containing the first and second halves of elements
def split_word(word):
    pass

# merge a pair of half-full words with sorted elems into a full word
def bitonic_pair_merge(word1, word2):
    pass
    
# flip order of input word's elements and return it
def reverse_word(word):
    m = W//2
    while (m >= b+1):
        word = reverse_helper(word, m)
        m = m//2
    return word

# word = word to reverse at this level; level determined by chunk size m, where m | W
# returns word with every m bits swapped with the adjacent m
def reverse_helper(word, m):
    repeater = 0
    for i in range(W//(m*2)):
        repeater = repeater << (m*2)
        repeater += 1
    
    firstmask = (((1<<m) - 1)<<m)*repeater
    secondmask = ((1<<m) - 1)*repeater
    result = ((word & secondmask) << m) + ((word & firstmask) >> m)
    #print("result=")
    #print_binary(result)
    return result


    

# input: word to operate on, which step to do (i.e. first step works with the two halves,
#   nth step works with the two halves of each 1/2^n of the word); requires it to have all
#   previous steps done and be bitonic at that level
# output: word that has elements swapped so that in each 1/2^{step_size} of the word, the
#   first half has the smaller half of the elements, and they're still bitonic
def bitonic_step(word, step_size):
    pass






def basic_tests():
    elems = [3, 7, 2, 15, 0, 8, 6, 12]  # all fit in one word
    word = 0
    for elem in elems:
        word = word << b+1
        word += elem
    print("original word: ")
    print_nicely(word)
    print ("reversed: ")
    print_nicely(reverse_word(word))


def print_nicely(word):
    # words are formatted as element values separated by underscored
    out = ""
    for i in range(W//(b+1)):
        nextb = word % 2**b
        word = word >> b+1           
        next_out = "_" + str(nextb)
        out = next_out + out
    print(out)

def print_binary(word):
    out = ""
    for i in range(W):
        out = str(word % 2) + out
        word = word >> 1
    print(out)


basic_tests()
