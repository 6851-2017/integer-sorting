# jamb 2017



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
    pass

# input: word to operate on, which step to do (i.e. first step works with the two halves,
#   nth step works with the two halves of each 1/2^n of the word); requires it to have all
#   previous steps done and be bitonic at that level
# output: word that has elements swapped so that in each 1/2^{step_size} of the word, the
#   first half has the smaller half of the elements, and they're still bitonic
def bitonic_step(word, step_size):
    pass
