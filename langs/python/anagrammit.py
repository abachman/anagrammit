""" anagrammit.py
An anagram generator using a recursive function.
Created by: Adam Bachman
Current: 1 December 2006
Project notes at [bachman.infogami.com](http://bachman.infogami.com/anagrammer)
"""

from optparse import OptionParser
from time import time
import sys
from random import shuffle

try:
    import psyco
    psyco.full()
except ImportError:
    pass # Sorry, no optimizations for you.

# global counters for tracking performance
WORD_CHECK = 0
LEX_GEN = 0

# write to stdout
def stdout(message):
    print message

def letterFrequency(instr):
    """ Create a letter frequency dictionary for a given word.  This function
    is only run through the dictionary once. """
    d = {}
    for l in instr:
        d[l]=instr.count(l)
    return d

#####################  LEXICON FUNCTION  #######################
def createOrigLex(lexi,inpt):
    """ generate initial lexicon """
    new_dict = []
    for word in lexi:
        bad = False
        for letter in word:
            # if it doesn't have too many of any particular letter and
            # doesn't have any foreign letters...
            if letter not in inpt:
                bad = True
                break
            elif word.count(letter) > inpt[letter]:
                bad = True
                break
        # add it to the original lexicon
        if not bad:
            new_dict.append( (word, letterFrequency(word)) )
    return new_dict

def createLexicon(lexi, inpt, reqs=None):
    '''generate lexicon'''
    global WORD_CHECK, LEX_GEN
    LEX_GEN += 1
    new_dict = []
    for word in lexi:
        WORD_CHECK += 1
        bad = False
        for l in word[1]:
            # if it doesn't have too many of any particular letter and
            # doesn't have any foreign letters...
            if inpt[l] == 0:
                bad = True
                break
            elif word[1][l] > inpt[l]:
                bad = True
                break
        # add it to the original lexicon
        if not bad:
            new_dict.append(word)
    return new_dict

####################  MAIN FUNCTION  #######################
# The main program loop, it calls itself once for every new word in
# an anagram.  That means if a particular anagram has eight words,
# our max recursion depth is eight.
#
# stop at limit, output results to stdout as they're found
def mainloop(lexi, inpt, rslt, limit, temp_result=[]):
    count = 0 # to remember where in the list we are.

    for next_word in lexi:
        count += 1

        temp_result.append(next_word[0])

        for x in next_word[1]:
            inpt[x] -= next_word[1][x]

        if sum(inpt.values()) == 0:
            ## Branch A
            ## Empty new input, full old lexicon.  We've got a winner!
            rslt[0] += 1

            # output result immediately
            stdout(' '.join(temp_result))

            # add results to list
            # rslt.append(' '.join(temp_result))

            if rslt[0] >= limit and limit != 0:
                return

            for l in temp_result.pop():
                inpt[l] += 1

        else:
            temp_lexi = createLexicon(lexi[count:], inpt)
            if len(temp_lexi) == 0:
                ## Branch B
                ## Full new input, empty new lexicon.
                for l in temp_result.pop():
                    inpt[l] += 1
            else:
                ## Branch C
                ## Full new input, full new lexicon. Go down one level
                mainloop(temp_lexi, inpt, rslt, limit, temp_result)

                # end recursion if limit was reached
                if rslt[0] >= limit and limit != 0:
                    return

                for l in temp_result.pop():
                    inpt[l] += 1

def main(pre_inpt, **kwds):
    limit = kwds.get('limit', 10)
    word_len = kwds.get('word_len', 3)
    exclude = kwds.get('exclude', '')
    include = kwds.get('include', '')
    subtract = kwds.get('subtract', '')
    dump_lexicon = kwds.get('dump_lexicon', False)

    [ pre_inpt.remove(l) for l in subtract ]

    # remove include's letters from input phrase
    if len(include) > 0:
        [ pre_inpt.remove(l) for l in include ]

    # generate initial counts for input phrase
    inpt = letterFrequency(pre_inpt)

    # generate the lexicon, filtering by word_len
    word_list = []
    for w in open('./words/dictionary.txt'):
        w = w.strip()
        if len(w) > word_len and w != include and w != exclude:
            word_list.append(w)

    # shuffle every time
    shuffle(word_list)

    dictionary = createOrigLex(word_list, inpt)

    # write lexicon
    if dump_lexicon:
        with open('./words/lexicon.tmp', 'w') as lex:
            lex.write("# input:  {0}\n".format(pre_inpt))
            lex.write("# length: {0}\n".format(len(dictionary)))
            [ lex.write(w[0] + "\n") for w in dictionary ]

    # find all anagrams
    temp_result = []
    if len(include) > 0:
        print "always include \"{0}\"".format(include)
        temp_result = [include]

    # first entry of the results array is a counter
    result = [0]

    mainloop(dictionary, inpt, result, limit, temp_result)

if __name__=="__main__":
    # input phrase
    inpt = sys.argv[-1]
    inpt = [l.lower() for l in inpt if l.isalpha()]

    parser = OptionParser()

    # parser.add_option("-o", "--output", dest="output",
    #                   help="write results to OUTPUT", metavar="FILE")
    parser.add_option('-n', '--number',
                      dest="limit", default=10, type=int,
                      help="number of results to return")
    parser.add_option('-l', '--length', dest='word_length', type=int,
                      help="minimum word length in results")
    parser.add_option('-i', '--include', dest='include',
                      help="include a word in the results")
    parser.add_option('-e', '--exclude', dest='exclude',
                      help="exclude a word from the results")
    parser.add_option('-s', '--subtract', dest='subtract',
                      help="subtract a word from the input phrase")
    parser.add_option('-d', '--dump', action="store_true", dest='dump_lexicon',
                      help="write initial lexicon to words/lexicon.tmp")
    parser.add_option('-q', '--quiet', action="store_true", dest='quiet',
                      help="don't output anything")

    (options, args) = parser.parse_args()

    # set limits
    word_len = options.word_length or 3
    limit    = options.limit
    if limit is None:
        limit = 10
    exclude  = options.exclude or '' # always exclude
    include  = options.include or '' # always include
    subtract = options.subtract or '' # always include

    exclude = exclude.lower()
    include = include.lower()
    subtract = subtract.lower()

    main(inpt, limit=limit, word_len=word_len, dump_lexicon=options.dump_lexicon,
         exclude=exclude, include=include, subtract=subtract)
