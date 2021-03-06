# jamb 2017

import math

N = 16
b = 4  # log n
W = 40 # TODO should be (b+1)*b*logb*2


# input: list of elems to sort
# output: sorted list of them
def packed_sort(elems):
    if len(elems) == 0:
        return []
    # pack into large words via word-level mergesort
    words = base_case_merge(elems)
    print("words:", [format_nicely(x) for x in words])
    
    # recursively merge sorted lists of words into twice-as-large lists
    list_of_word_lists = [[x] for x in words]
    next_list = []
    
    while len(list_of_word_lists) > 1:
        l = len(list_of_word_lists)//2
        print("lists:", [[format_nicely(x) for x in w] for w in list_of_word_lists])
        for i in range(l):
            list1 = list_of_word_lists[2*i]
            list2 = list_of_word_lists[2*i+1]
            next_list.append(merge_lists(list1, list2))
        if len(list_of_word_lists) % 2 == 1:
            next_list.append(list_of_word_lists[-1])
        list_of_word_lists = next_list
        next_list = []

    print("lists:", [[format_nicely(x) for x in w] for w in list_of_word_lists])

    # extract from the words back into a list
    wordlist = list_of_word_lists[0]
    sorted_elems = []
    mask = (1 << (b+1)) - 1
    for word in wordlist:
        els = []
        for i in range(W//(b+1)//2):
            els.append(word & mask)
            word = word >> (b+1)
        sorted_elems.extend(els[::-1])
    return sorted_elems

# input: list of elems to sort
# output: list of words with sorted elems packed into them
def base_case_merge(elems):
    # TODO replace this with something actually efficient;
    # for now I'm working with small words so roughly constant to just manually sort
    index = 0
    elems_per_word = W//2//(b+1)
    words = []
    next_word = []
    for elem in elems:
        next_word.append(elem)
        index += 1
        if (index % elems_per_word == 0):
            word = sorted(next_word)
            word_val = 0
            for x in word:
                word_val = word_val << (b+1)
                word_val += x
            words.append(word_val)
            next_word = []
    if (index % elems_per_word != 0):
            word = sorted(next_word)
            word_val = 0
            for x in word:
                word_val = word_val << (b+1)
                word_val += x
            words.append(word_val)

    return words

def get_last_element(word):
    mask = (1 << b) - 1
    elt = word & mask
    return elt

# input: two lists of words with sorted elems in sorted order, each word only half full
# output: list of words with sorted elems such that the whole thing is sorted, each word only half full
def merge_lists(wordlist1, wordlist2):
    it1 = 0
    it2 = 0
    wordlist = []
    while True:
        if it1 >= len(wordlist1):
            if it2 >= len(wordlist2):
                break
            wordlist.append(wordlist2[it2])
            it2 += 1
        elif it2 >= len(wordlist2):
            wordlist.append(wordlist1[it1])
            it1 += 1
        else:
            word1 = wordlist1[it1]
            word2 = wordlist2[it2]
            word = bitonic_pair_merge(word1, word2)
            (w1, w2) = split_word(word)
            wordlist.append(w1)
            biggest = get_last_element(w2)
            if biggest == get_last_element(word1):
                # we put the larger of the word pair back onto list 1
                wordlist1[it1] = w2
                it2 += 1
            elif biggest == get_last_element(word2):
                # we put the larger of the word pair back onto list 2
                wordlist2[it2] = w2
                it1 += 1
            else:
                # it should've been in one of the lists...
                raise ValueError("Where did this value come from?!")
            
    return wordlist
        

# input: word with sorted elems
# output: two first-half-empty words, containing the first and second halves of elements
def split_word(word):
    first = word >> (W//2)
    sec_and = (1 << (W//2)) - 1
    second = word & sec_and
    return first, second

# merge a pair of half-full words with sorted elems into a full word
def bitonic_pair_merge(word1, word2):
    word = reverse_word(word2) + word1  # / / -> \/
    for step in range(int(math.log2(W//(b+1))+0.0001)): #added epsilon for floating error
        word = bitonic_step(word, step)
    return word
    
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
# output: word that has elements swapped so that in each 1/2^{step} of the word, the
#   first half has the smaller half of the elements, and they're still bitonic
def bitonic_step(word, step):
    m = W//(2*2**step)  # chunk size
    repeater = 0
    for i in range(W//(m*2)):
        repeater = repeater << (m*2)
        repeater += 1
    diffmask = 0
    for i in range(W//(b+1)):
        diffmask = diffmask << (b+1)
        diffmask += 1
    diffmask = diffmask << b
    
    firstmask = (((1<<m) - 1)<<m)*repeater
    secondmask = ((1<<m) - 1)*repeater
    topline = (word & firstmask) >> m
    topline = diffmask | topline
    bottomline = (word & secondmask)
    diff = topline - bottomline
    topline = topline & ~diffmask
    
    A_bits = ((diff & diffmask) >> b)*((1 << (b+1))-1)  # & this with A
    B_bits = ~A_bits
    smaller = (topline & B_bits) + (bottomline & A_bits)
    larger = (topline & A_bits) + (bottomline & B_bits)
    return (smaller << m) + larger
    



def basic_tests():
    # elems = [3, 7, 2, 15, 0, 8, 6, 12]  # all fit in one word
    # TESTING BITONIC_PAIR_MERGE
    word1 = 0
    for elem in [1, 3, 4, 5]:
        word1 = word1 << b+1
        word1 += elem
    word2 = 0
    for elem in [0, 1, 4, 6]:
        word2 = word2 << b+1
        word2 += elem
    print("word1:")
    print_nicely(word1)
    print("word2:")
    print_nicely(word2)
    print("sorted:")
    word = bitonic_pair_merge(word1, word2)
    print_nicely(word)
    w1, w2 = split_word(word)
    print_nicely(w1)
    print_nicely(w2)

    word3 = 0
    for elem in [6, 6, 8, 9]:
        word3 = word3 << b+1
        word3 += elem
    word4 = 0
    for elem in [11, 12, 14, 15]:
        word4 = word4 << b+1
        word4 += elem
    # TESTING MERGE_LISTS
    list1 = [word1, word3, word4]
    list2 = [word2, word4]
    print("LIST1")
    print([format_nicely(x) for x in list1])
    print("LIST2")
    print([format_nicely(x) for x in list2])
    list_merge = merge_lists(list1, list2)
    print("MERGE")
    print([format_nicely(x) for x in list_merge])

    # TESTING BASE CASE MERGE
    print("\nTESTING BASE CASE MERGE")
    vals = [0, 5, 1, 3, 6, 2, 7, 4, 3, 6, 7, 11, 13, 9]
    res = base_case_merge(vals)
    for x in res:
        print_nicely(x)

    # TESTING PACKED SORT
    print("\nTESTING PACKED SORT")
    print(packed_sort(vals))


def print_nicely(word):
    print(format_nicely(word))
    
def format_nicely(word):
    # words are formatted as element values separated by underscored
    out = ""
    for i in range(W//(b+1)):
        nextb = word % 2**b
        word = word >> b+1           
        next_out = "_" + str(nextb)
        out = next_out + out
    return out

def print_binary(word):
    print(format_binary(word))

def format_binary(word):
    out = ""
    for i in range(W):
        if (i%(b+1) == 0):
            out = " " + out
        out = str(word % 2) + out
        word = word >> 1
    return out


basic_tests()
