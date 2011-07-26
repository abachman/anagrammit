/* word.  27 cell array.  first 26 cells = letter count, 27th = original word index */

#define END 26
#define MAX_STR 24

void letterCount(char *, short []);
int wordCheck(short [], short []);
void inputAdd(short inpt[], const short update[]);
void inputRemove(short inpt[], const short update[]);
void getWordList(char [][MAX_STR]);
int isempty(short []);

