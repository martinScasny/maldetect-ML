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

void printItem(ITEM* item) {
    printf("id: %d priority: %d\n",item->id,(int)item->priority);
}

void qPrintItems(PQUEUE* q) {
    for (size_t i = 0; i < q->len; i++)
    {
        printItem(q->items[i]);
    }
    
}

void swap(void* a, void* b) {
    void* c = a;
    a = b;
    b = c;
    c = NULL;
}

int findElementBi(PQUEUE* q, ITEM* curr) {
    ITEM** items = q->items;
    ITEM* target = NULL;
    uint16_t a = 0;
    uint16_t b = q->len;
    uint16_t c;
    if(curr->priority >= q->first->priority) {
        return 0;
    }
    if(curr->priority <= q->last->priority) {
        return q->len;
    }
    while(b-a > 1) {
        c = (b+a)/2;
        if(items[c]->priority < curr->priority && items[c-1]->priority >= curr->priority) {
            return (int)c;
        } else if (items[c]->priority > curr->priority) {
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
    int target = -1;
    if(q->len == 0) {
        q->first = item;
        q->last = item;
        q->items[0] = item;
        q->len++;

    } else if(q->len < q->maxLen) {
        target = findElementBi(q, item);
        if(!target) {
            memmove(&q->items[1],&q->items[0],sizeof(ITEM*)*(q->len));
            q->items[0] = item;
            q->first = item;
        } else if(target == q->len){
            q->items[q->len+1] = item;
            q->last = item;
        } else {
            memmove(&q->items[target+1],&q->items[target],sizeof(ITEM*)*(q->len-target));
            q->items[target] = item;
        }     
        q->len++;

    } else {
        if(item->priority <= q->last->priority) {
            free(item);
        } else {
            target = findElementBi(q, item);
            memmove(&q->items[target+1],&q->items[target],sizeof(ITEM*)*(q->len));
            free(q->last);
            q->last = (q->items[q->len]);
        }
    }
}

int** findNTopValues(int n, uint16_t arr[],int len) {
    int **result = calloc(sizeof(int*),n);
    PQUEUE* q = malloc(sizeof(PQUEUE));
    q->first = NULL;
    q->last = NULL;
    q->len = 0;
    q->maxLen = n;
    q->items = calloc(sizeof(ITEM*),q->maxLen);

    for(int i = 0; i < len; i++) {
        push(q,arr[i],i);
        qPrintItems(q);

    }

    for (int i = 0; i < n; i++)
    {
        (*result)[i] = (*q->items)[i].id;
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
    int** result = NULL;
    for(int i = 0; i < n; i++) {
        arr[i] = rand()%n;
    }
    result = findNTopValues(1000,arr,n);
    for (int i = 0; i < 1000; i++)
    {
        printf("%d\n",(*result[i]));
    }

    free(result);
    

    return 0;
}
