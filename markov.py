"""Generate Markov text from text files."""

from random import choice
from sys import argv

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path) as data_file:
        return data_file.read()

def make_bigram_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """
    #the argument-less version of .split(), so it breaks on any kind of whitespace, including linebreaks, spaces, and tabs.
    #this becomes a list of strings
    split_string = text_string.split()

    #make empty dictionary
    chains = {}

    #loop through each item in list
        #create bigrams (word pairs) as tuples
        #add to dictionary as KEYS
        #if it's the first time key added, we create its value as a list of word_after
        #if key already in dict, we add word_after to the existing list

    for i in range(0, (len(split_string)-2)):
        bigram_tuple = (split_string[i], split_string[i+1])
        word_after = split_string[i+2]

        if bigram_tuple not in chains:
            chains[bigram_tuple] = [word_after]

        else:
            chains[bigram_tuple].append(word_after)
            #chains[bigram_tuple] += [word_after[:] also works :)

        #.setfault() ?? to refactor this if-else as single line

    #print(chains)
    return chains

def make_chains_any_size(text_string, size):

    split_string = text_string.split()

    chains = {}

    for i in range(0, (len(split_string)-size)):
        ngram_word_list = []                            #empty list to work on

        for j in range(0, size):                        #increments how many words that compose the tuple
            ngram_word_list.append(split_string[i+j])   #adds all the words from 0 to n to a list
            ngram_tuple = tuple(ngram_word_list)        #makes the entire list a tuple

        word_after = split_string[i+size]               #saves the word after the n amount of words

        if ngram_tuple not in chains:       
            chains[ngram_tuple] = [word_after]

        else:
            chains[ngram_tuple].append(word_after)

    #print(chains)
    return chains

def make_bigram_text(chains):
    """Return text from chains."""

    words = []

    generative_key = choice(list(chains.keys()))
    # print("key initialized as " + str(generative_key))

    while True:

        try:
            markov_word = choice(chains[generative_key])
            # print("markov word from that key is " + markov_word)

            words.append(markov_word)
            # print("current word list is " + str(words))

            generative_key = (generative_key[-1], markov_word)
            # print("next generative key is " + str(generative_key))

        except KeyError:
            #print("Key Error, end of chain reached")
            break 

    return " ".join(words)

def make_ngram_text(chains):

    words = []

    generative_key = choice(list(chains.keys()))
    #print("key initialized as " + str(generative_key))

    while True:

        try:
            markov_word = choice(chains[generative_key])
            words.append(markov_word)

            generative_key_as_list = list(generative_key) #converts generative key(tuple) into list
            generative_key = tuple(generative_key_as_list[1:] + [markov_word]) #adds markov word to the list without first word and coverts into tuple
        
        except KeyError:
            break 

    return " ".join(words)


input_path = argv[1]

ngram_size = int(argv[2])

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
# chains = make_bigram_chains(input_text)
chains = make_chains_any_size(input_text, ngram_size)

# Produce random text
#random_text = make_bigram_text(chains)
random_text = make_ngram_text(chains)

print(random_text)
