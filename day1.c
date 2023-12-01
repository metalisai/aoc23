#if 0
set -e
gcc day1.c -o day1 -ggdb
./day1
exit
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char *lookfor[] = {
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"
};

int findAny(char *haystack, int offset) {
    int count = sizeof(lookfor)/sizeof(lookfor[0]);
    for (int i = 0; i < count; i++) {
        int found = 0;
        for (int j = 0; j < strlen(lookfor[i]); j++) {
            if (haystack[offset+j] != lookfor[i][j]) {
                found = -1;
                break;
            }
        }
        if (found >= 0) {
            return i;
        }
    }
    return -1;
}

int main(void) {
    FILE * input = fopen("./input", "r");

    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    int sum = 0;
    while ((read = getline(&line, &len, input)) != -1) {
        line[read-1] = '\0';
        int first = -1;
        int last = -1;
        for (int i = 0; i < read; i++) {
            int result = findAny(line, i);
            if (result >= 0) {
                if (first < 0) {
                    first = result;
                }
                last = result;
            }
        }
#define getInt(x) (((x) < 9) ? ((x)+1) : ((x)-9+1))
        int firstNum = getInt(first);
        int lastNum = getInt(last);
        sum += 10*firstNum + lastNum;
    }
    printf("sum %d\n", sum);
    return 0;
}
