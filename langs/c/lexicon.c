/* the lexicon, based on simple_stack.c (03_linked_lists)
From the original lexicon (that actually holds all the words)
we create stacks of pointers to words.
*/
#include <stdlib.h>
#include <stdio.h>
#include "words.h"
#include "lexicon.h"

void PushQ(lexiptr *sPtr, short val)
{   /* put an item on top. */
    itemptr newPtr;
    newPtr = malloc(sizeof(item));

    if (newPtr != NULL) {   
        newPtr->word = val;
        if (sPtr->tail == NULL) {
            newPtr->next = NULL;
            sPtr->head = newPtr;
            sPtr->tail = newPtr;            
        }
        else {
            sPtr->tail->next = (void *)newPtr;
            newPtr->next = NULL;
            sPtr->tail = newPtr;
        }
    }
}

short PopQ(lexiptr *sPtr)
{   /* take an item off the end and return its value */
    itemptr currentPtr = sPtr->head;
    short temp;
    if (currentPtr != NULL) {
        temp = currentPtr->word;
        sPtr->head = (void *)currentPtr->next;
        free(currentPtr);
        //printf("Popping the value '%i'\n", temp);
        return temp;
    }
    else {}
}

void PrintQ(lexiptr *sPtr)
{   itemptr nextPtr = sPtr->head;
    while (nextPtr!=NULL) {
        printf("%i ",nextPtr->word);
        nextPtr = nextPtr->next;
    }
}

