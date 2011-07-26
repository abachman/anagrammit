""" anagrammit.py
An anagram generator using a recursive function.
Created by: Adam Bachman
Current: 1 December 2006
Project notes at [bachman.infogami.com](http://bachman.infogami.com/anagrammer)
"""

from time import time
import sys

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
            new_dict.append((word, letterFrequency(word)))
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
def mainloop(lexi, inpt, rslt, limit, temp_rslt=[]):
    count = 0 # to remember where in the list we are.
    for next_word in lexi:
        count += 1

        temp_rslt.append(next_word[0])

        for x in next_word[1]:
            inpt[x] -= next_word[1][x]

        if sum(inpt.values()) == 0:
            ## Branch A
            ## Empty new input, full old lexicon.  We've got a winner!
            rslt[0] += 1

            # output result immediately
            stdout(' '.join(temp_rslt))

            # add results to list
            # rslt.append(' '.join(temp_rslt))

            if rslt[0] >= limit:
                return

            for l in temp_rslt.pop():
                inpt[l] += 1

        else:
            temp_lexi = createLexicon(lexi[count:], inpt)
            if len(temp_lexi) == 0:
                ## Branch B
                ## Full new input, empty new lexicon.
                for l in temp_rslt.pop():
                    inpt[l] += 1
            else:
                ## Branch C
                ## Full new input, full new lexicon. Go down one level
                mainloop(temp_lexi, inpt, rslt, temp_rslt)

                # end recursion if limit was reached
                if rslt[0] >= limit:
                    return

                for l in temp_rslt.pop():
                    inpt[l] += 1

def main(pre_inpt, limit):
    # generate initial counts for input phrase
    inpt = letterFrequency(pre_inpt)

    # first entry of the results array is a counter
    result = [0]

    # generate the lexicon
    dictionary = createOrigLex([x.strip() for x in open('./words/dictionary.txt')],inpt)

    # find all anagrams
    mainloop(dictionary, inpt, result, limit)

    # return result[0], result[1:]

if __name__=="__main__":
    # input phrase
    inpt = sys.argv[1]
    inpt = ''.join([l for l in inpt.lower() if l.isalpha()])

    print inpt

    # set limit
    limit = 10

    main(inpt, limit)

    # # Prompt for input
    # inpt = raw_input("Enter the phrase to be anagrammed: ")
    # inpt = ''.join([l for l in inpt.lower() if l.isalpha()])

    # # Or run straight away
    # #inpt = "puresoapunion"

    # # Time the run
    # start = time()
    # r_quant, results = main(inpt)
    # finish = time()
    # total = finish - start

    # # Display stats
    # print "   ", "-" * 20
    # print "    input = %s" % inpt
    # print "    results = %i" % r_quant
    # print "    lexicon generations = %i" % LEX_GEN
    # print "    word checks = %i" % WORD_CHECK
    # print "    running time = %f" % total
    # print "    "
    # print "    res / sec = %f" % (r_quant / total)
    # print "    lexgen / res = %i" % (r_quant != 0 and (LEX_GEN / r_quant) or 0)
    # print "    wdchk / res = %i" % (r_quant != 0 and (WORD_CHECK / r_quant) or 0)
    # print "   ", "-" * 20

    # # Save to file
    # print "Saving to '%s_results.txt'" % inpt
    # f = file("%s_results.txt" % inpt, 'w')
    # for res in results:
    #     print >> f, res

    # f.write("%s seconds used." % total)
    # f.write("%i results found" % r_quant)
    # f.close()
