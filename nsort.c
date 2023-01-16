#include <stdio.h>
#include <ctype.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

typedef struct item {
    uint16_t priority;
    unsigned int id;
}ITEM;


typedef struct pQueue {
    uint16_t maxLen;
    uint16_t len;
    ITEM *first;
    ITEM *last;
    ITEM **items;
}PQUEUE;

void printItem(ITEM* item,unsigned int i) {
    printf("%p\n",item);
    printf("no.%d - id: %d priority: %d\n",i,item->id,(int)item->priority);
}

void qPrintItems(PQUEUE* q) {
    for (int i = 0; i < q->len; i++)
    {
        printItem(q->items[i],i);
    }
    
}

int findElementBi(PQUEUE* q, ITEM* curr) {
    ITEM** items = q->items;
    uint16_t a = 0;
    uint16_t b = q->len;
    uint16_t c;
    if(curr->priority >= q->first->priority) {
        return 0;
    }
    if(curr->priority <= q->last->priority) {
        return q->len;
    }
    while(b-a > 0) {
        c = (b+a)/2;
        uint16_t cpriority = items[c]->priority;
        if(cpriority < curr->priority && items[c-1]->priority >= curr->priority 
            || cpriority == curr->priority) {
            return (int)c;

        } else if (cpriority > curr->priority) {
            a = c;
        } else {
            b = c;
        }
    }
}

void push(PQUEUE* q, uint16_t priority, unsigned int id) {
    ITEM *item = calloc(sizeof(ITEM),1);
    item->id = id;
    item->priority = priority;
    int target = 0;
    uint16_t len = q->len;
    if(len == 0) {
        q->first = item;
        q->last = item;
        q->items[0] = item;
        q->len++;

    } else if(len < q->maxLen) {
        target = findElementBi(q, item);
        if(!target) {
            memmove(&q->items[1],&q->items[0],sizeof(ITEM*)*(len));
            q->items[0] = item;
            q->first = item;
        } else if(target == len){
            q->items[q->len] = item;
            q->last = item;
        } else {
            memmove(&q->items[target+1],&q->items[target],sizeof(ITEM*)*(len-target));
            q->items[target] = item;
        }     
        q->len++;

    // queue is full
    } else {
        if(item->priority <= q->last->priority) {
            free(item);
        } else {
            target = findElementBi(q, item);
            memmove(&q->items[target+1],&q->items[target],sizeof(ITEM*)*(len-target));
            q->items[target] = item;
            free(q->last);
            q->last = (q->items[len-1]);
        }
    }
}

unsigned int** findNTopValues(int queueSize, uint16_t *arr, unsigned int n) {
    unsigned int **result = calloc(sizeof(unsigned int*),queueSize);
    for (int i = 0; i < queueSize; i++)
    {
        result[i] = calloc(sizeof(unsigned int),1);
    }
    
    PQUEUE* q = malloc(sizeof(PQUEUE));
    q->first = NULL;
    q->last = NULL;
    q->len = 0;
    q->maxLen = queueSize;
    q->items = calloc(sizeof(ITEM*),q->maxLen+1);

    for(unsigned long long i = 0; i <= n; i++) {
        push(q,arr[i],i);
        // qPrintItems(q);
    }
    
    for (int i = 0; i < queueSize; i++)
    {
        (*result[i]) = q->items[i]->id;
    }

    // Free used memory --------------------------------------
    for(ITEM* curr = q->items[0]; curr != NULL; curr++) {
        free(curr);
    }

    free(q->items);
    free(q);

    return result;
}
// int main(char** argv,int argc) {
//     int queueLen = 10;
//     unsigned int n = 4294967295;
//     char* directory = "C:\\Users\\Martin\\Desktop\\mysamples\\binary_gen\\binary_gen\\testfiles\\";
//     uint16_t *frequency = calloc(sizeof(uint16_t), n);
//     unsigned int** result = NULL;

//     for (int i = 0; i < 100; i++) {
//         char filepath[100];
//         sprintf(filepath,"%sfile%d.bin",directory,i);
//         FILE *file = fopen(filepath, "rb");
//         if (file == NULL) {
//             printf("Error opening file %s",filepath);
//         }

//         fseek(file, 0, SEEK_END);
//         int size = ftell(file);
//         rewind(file);

//         char *buffer = (char*)malloc(size);
//         fread(buffer, size, 1, file);
//         fclose(file);

//         for (int i = 0; i <= size - 1; i += 4) {
//             unsigned int number = *(unsigned int*)(buffer + i);
//             printf("number is %d\n",number);
//             frequency[number]++;
//         }
//         free(buffer);
//         }

//     result = findNTopValues(queueLen,frequency,n);
//     for (unsigned int i = 0; i < queueLen; i++)
//     {
//         printf("%d\n",(*result[i]));
//     }
//     free(result);
    
//     return 0;
// }
