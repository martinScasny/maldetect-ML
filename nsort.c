#include <stdio.h>
#include <ctype.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

typedef struct item
{
    uint16_t priority;
    int id;
}ITEM;


typedef struct pQueue {
    uint16_t maxLen;
    uint16_t len;
    ITEM *first;
    ITEM *last;
    ITEM **items;
}PQUEUE;

// void swap(void* a, void* b) {
//     void* c = a;
//     a = b;
//     b = c;
//     c = NULL;
// }

ITEM* findElementBi(PQUEUE* q, ITEM* curr) {
    ITEM** items = q->items;
    ITEM* target = NULL;
    uint16_t a = 0;
    uint16_t b = q->len;
    uint16_t c;
    if(curr->priority >= q->first) {
        return (*q->items);
    }
    if(curr->priority <= q->last) {
        return(*q->items+q->len);
    }
    while(b-a != 0) {
        c = b-a/2;
        target = (*items + c);
        if(target->priority >= curr->priority && ((*(target+1)).priority < curr->priority)) {
            return target;
        } else if (target->priority > curr->priority) {
            a = c;
        } else {
            b = c;
        }
    }
}

void push(PQUEUE* q, uint16_t priority, int id) {
    ITEM *item = malloc(sizeof(ITEM));
    item->id = id;
    item->priority = priority;
    ITEM *target = NULL;
    if(q->len == 0) {
        q->first = item;
        q->len++;

    } else if(q->len < q->maxLen) {
        target = findElementBi(q, item);
        memmove(target,target+1,q->len);
        q->len++;

    } else {
        if(item->priority <= q->last->priority) {
            free(item);
        } else {
            target = findElementBi(q, item);
            memmove(target,target+1,q->len);
            free(q->last);
            q->last = (*q->items + q->len);
        }
    }
}

int** findNTopValues(int n, uint16_t** arr,int len) {
    uint16_t result[n];
    PQUEUE* q = malloc(sizeof(PQUEUE));
    q->first = NULL;
    q->last = NULL;
    q->len = 0;
    q->maxLen = n*2;
    q->items = malloc(sizeof(ITEM)*q->maxLen);

    for(int i; i < len, i++) {
        push(q,arr[i],i);
    }

    for (int i = 0; i < n; i++)
    {
        result[i] = q->items[i]->id;
    }
    

    // Free used memory --------------------------------------
    for(ITEM* curr = *q->items; curr != NULL; curr++) {
        free(curr);
    }

    free(q->items);
    free(q);

    return result;
}

int main(char** argv,int argc) {
    int n = 10000;
    uint16_t arr[n];
    uint16_t** result;
    for(int i = 0; i < n; i++) {
        arr[i] = rand()%n;
    }
    result = findNTopValues(1000,arr,n);
    for (int i = 0; i < 1000; i++)
    {
        printf("%hu\n",result[i]);
    }
    

    return 0;
}
