//testing the anagrammer modules
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "words.h" 
#include "lexicon.h"

#define LEXICON_LEN 23000
#define SINGLE_RESULT 15
#define WORD_LEN 27
#define MAX_RESULTS 10000
/* #define DEBUG */

void MainLoop(short lexicon[][WORD_LEN], short input[], short temp_results[], 
              short results[][SINGLE_RESULT], short next_temp_result, 
              lexiptr temp_lex, char orig_words[][MAX_STR]);

int c = 0;
int COUNT_RESULTS = 0;
int next_result = 0;
char orig_words[LEXICON_LEN][MAX_STR];

int main() {
    int counter = 0, orig_words_len = 0, i;
    char orig_words[LEXICON_LEN][MAX_STR];
    // Initialize orig_words
    for (counter=0;counter<LEXICON_LEN;counter++)
        orig_words[counter][0] = '\0';
    puts(" GET WORDS ");
    getWordList(orig_words);
    puts(" GOT 'EM ");
    for (counter=0;counter<LEXICON_LEN;counter++)
    {   if (orig_words[counter][0] == '\0')
        {   orig_words_len = counter;
            break;
        }
    }
    // Initialize original lexicon
    short lexicon[orig_words_len][WORD_LEN];
    for (i=0;i<orig_words_len;i++) 
    {   letterCount(orig_words[i], lexicon[i]);
        lexicon[i][END] = i;
    }
    
    // Initialize input
    short inpt[WORD_LEN];
    const char *inpt_str = "wellpunchmeinthefac";
    letterCount(inpt_str, inpt);
    
    // Create Original Lexicon Queue...
    /* Add to orig_lex the index of the 
    words that could possibly be spelled with the
    letters in the input.  This list will be 
    passed to the finding function */
    lexiptr orig_lex;
    for (i=0;i<orig_words_len;i++)
        if (wordCheck(inpt, lexicon[i])) 
            PushQ(&orig_lex, i);
    
    // Initialize results
    short temp_results[SINGLE_RESULT];
    for (i=0;i<SINGLE_RESULT;i++) 
        temp_results[i] = -1; 
    short results[MAX_RESULTS][SINGLE_RESULT];
    for (counter=0;counter<MAX_RESULTS;counter++)
        for (i=0;i<SINGLE_RESULT;i++)
            results[counter][i] = -1;
    
    /* Current Variables:
       char orig_words[][30], short lexicon[][27], short inpt[], 
       short temp_results[], short results[][15], next_result  */
    
    puts(" GO! ");
    printf("Start  = %d\n", time(NULL)); 
    MainLoop(lexicon, inpt, temp_results, results, 0, orig_lex, orig_words);
    printf("Finish = %d, %i results found.\n", time(NULL), COUNT_RESULTS);
    
    for (counter=0;counter<50;counter++)
    {   if (results[counter][0] == -1) continue;
        for (i=0;i<SINGLE_RESULT;i++)
            if (results[counter][i] != -1)
                printf("%s ", orig_words[results[counter][i]]);
        puts("");
    }
    return 1;
}

void MainLoop(short lexicon[][WORD_LEN], short input[], short temp_results[], 
              short results[][SINGLE_RESULT], short next_temp_result, 
              lexiptr temp_lex, char orig_words[][MAX_STR])
{   while (temp_lex.head != NULL && temp_lex.tail != NULL) 
    {   temp_results[next_temp_result] = PopQ(&temp_lex);
        inputRemove(input, lexicon[temp_results[next_temp_result]]);    
            
        if (isempty(input)) 
        {   COUNT_RESULTS++;
#ifdef DEBUG            
            puts("Found One!");
            printf("%i\t",COUNT_RESULTS);
            printf("%i => ", next_result);
#endif      
            if (next_result % 10000 == 0)
                printf("%i\n",next_result);
            if (next_result < MAX_RESULTS) 
            {   for (c=0;c<=next_temp_result;c++) 
                {   results[next_result][c] = temp_results[c]; 
#ifdef DEBUG                
                    printf("%s (%i) ", orig_words[temp_results[c]], temp_results[c]);
#endif             
                }
            }
#ifdef DEBUG
            printf("  length = %i\n",next_temp_result);
#endif
            inputAdd(input, lexicon[temp_results[next_temp_result]]);   
            temp_results[next_temp_result] = -1;
            next_result += 1;
        }
        else 
        {   /* CREATE NEW LEXICON */
            lexiptr new_lex;
            new_lex.tail = NULL; // in case nothing is added
            itemptr tmp_item = temp_lex.head;
            while (tmp_item != NULL) 
            {   if (wordCheck(input, lexicon[tmp_item->word]))
                    PushQ(&new_lex, tmp_item->word);
                tmp_item = (itemptr)tmp_item->next;
            }
            
            if (new_lex.tail == NULL)
            {   // empty lexicon, stay at this level and go to the next word.
                inputAdd(input, lexicon[temp_results[next_temp_result]]);
                temp_results[next_temp_result] = -1;
            }   
            else
            {   // full lexicon, full input, drill down.
#ifdef DEBUG                
                printf("Call again!\n");
#endif
                MainLoop(lexicon, input, temp_results, results,  
                        next_temp_result+1, new_lex, orig_words);
                inputAdd(input, lexicon[temp_results[next_temp_result]]);
                temp_results[next_temp_result] = -1;
            }
        }
    }
}

