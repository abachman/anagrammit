#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "words.h"

#define END 26
#define MAX_STR 24

void letterCount(char *s, short c[]) 
{   int i;
    for (i = 0; i < END; c[i++] = 0); 
    for ( ;*s!='\0';s++) c[*s-97] += 1;
}

int wordCheck(short a[], short b[]) 
{   /* can word b be spelled with the letters from word a?
       a is primary (input string) b is secondary (old lexicon word)
    Unrolled loop, generated in Python 
    for x in range(26): 
        print "else if (a[%i] < b[%i])\n    return 0;"%(x,x) */
    if (a[0] < b[0]) return 0;
    else if (a[1] < b[1]) return 0;
    else if (a[2] < b[2]) return 0;
    else if (a[3] < b[3]) return 0;
    else if (a[4] < b[4]) return 0;
    else if (a[5] < b[5]) return 0;
    else if (a[6] < b[6]) return 0;
    else if (a[7] < b[7]) return 0;
    else if (a[8] < b[8]) return 0;
    else if (a[9] < b[9]) return 0;
    else if (a[10] < b[10]) return 0;
    else if (a[11] < b[11]) return 0;
    else if (a[12] < b[12]) return 0;
    else if (a[13] < b[13]) return 0;
    else if (a[14] < b[14]) return 0;
    else if (a[15] < b[15]) return 0;
    else if (a[16] < b[16]) return 0;
    else if (a[17] < b[17]) return 0;
    else if (a[18] < b[18]) return 0;
    else if (a[19] < b[19]) return 0;
    else if (a[20] < b[20]) return 0;
    else if (a[21] < b[21]) return 0;
    else if (a[22] < b[22]) return 0;
    else if (a[23] < b[23]) return 0;
    else if (a[24] < b[24]) return 0;
    else if (a[25] < b[25]) return 0;
    return 1;
}

void inputAdd(short inpt[], const short update[])
{   int c = 0;
    for ( ; c < END; c++)
	if (update[c] > 0)
            inpt[c] += update[c];    
}

void inputRemove(short inpt[], const short update[]) 
{   int c = 0;
    for ( ; c < END; c++)
	if (update[c] > 0)
	   inpt[c] -= update[c];    
}

void getWordList(char words[][MAX_STR])
{   /* Read a list of strings from a dictionary file. 
       Make sure the words array is longer than the file.*/
    FILE *fPtr;
    int next = 0;
    char temp[MAX_STR], c;
    printf(" Opening dictionary.txt. ");
    if ((fPtr = fopen("dictionary.txt", "r")) == NULL)
	printf("File could not be opened!");
    else 
    {   while(!feof(fPtr)) 
	{   fscanf(fPtr, "%s", words[next++]);
	    //printf(".");
	}
    } 
    fclose(fPtr);  
}

int isempty(short word[])
{   short c=0;
    for (;c<END;c++) if (word[c]) return 0;
    return 1;	    
}

