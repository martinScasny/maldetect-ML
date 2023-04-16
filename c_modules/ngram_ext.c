#include <stdio.h>
#include <stdlib.h>

unsigned char* read_file(char* filename, size_t* length) {
    FILE* file = fopen(filename, "rb");
    if (!file) {
        printf("Error: File not found or cannot be opened.\n");
        exit(1);
    }
    
    // Get the file length
    fseek(file, 0, SEEK_END);
    *length = ftell(file);
    fseek(file, 0, SEEK_SET);
    
    // Read the file into a buffer
    unsigned char* buffer = (unsigned char*) malloc(*length);
    if (!buffer) {
        printf("Error: Memory allocation failed.\n");
        exit(1);
    }
    size_t bytes_read = fread(buffer, 1, *length, file);
    if (bytes_read != *length) {
        printf("Error: Failed to read file.\n");
        exit(1);
    }
    
    fclose(file);
    return buffer;
}

unsigned int* get_ngram(char* filename, int n, int* num_ngrams) {
    unsigned char* buffer;
    size_t length;
    unsigned int* result;
    int i,j;
    
    buffer = read_file(filename, &length);
    *num_ngrams = length - n + 1;
    result = (unsigned int*) malloc(*num_ngrams * sizeof(unsigned int));
    if (!result) {
        printf("Error: Memory allocation failed.\n");
        exit(1);
    }
    
    for (i = 0; i < *num_ngrams; i++) {
        char* value = calloc(n,sizeof(char));
        unsigned int combined = 0;

        for (j = 0; j < n; j++) {
            combined |= (unsigned char)(*(buffer + i + j)) << (8 * (3 -j));
        }
        result[i] = combined;
    }
    
    free(buffer);
    return result;
}

// int main() {
//     char* filename = "../sample50mb";
//     int n = 4;
//     int* ngrams;
//     int num_ngrams, i;
    
//     ngrams = get_ngram(filename, n, &num_ngrams);
//     for (i = 0; i < num_ngrams; i++) {
//         printf("%u\n", ngrams[i]);
//     }
//     free(ngrams);
    
//     return 0;
// }
