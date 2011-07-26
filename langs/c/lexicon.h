/* Simple Queue */
typedef struct {
    short word;
    struct item *next;
} item, *itemptr;

typedef struct {
    itemptr head;
    itemptr tail;
} lexiptr;

void PushQ(lexiptr *, short);
short PopQ(lexiptr *); /* take an item off and return its value */
void PrintQ(lexiptr *); /* print the list (for debugging)*/

