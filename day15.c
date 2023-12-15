#if 0 
set -xe
cc day15.c -o day15 -ggdb
./day15
exit
#endif
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <stdbool.h>

#define LENS_COUNT 9
#define BOX_COUNT 256

typedef struct Lens {
    uint8_t focalLength;
    const char* label;
} Lens;

uint8_t hash_str(char *token) {
    size_t tlen = strlen(token);
    uint8_t hash = 0;
    for (int i = 0; i < tlen; i++) {
        char c = token[i];
        if (c == '\n') continue;
        hash = ((hash + (uint8_t)c) * 17) & 0xFF;
    }
    return hash;
}

int findLens(Lens lenses[][LENS_COUNT], uint8_t box, const char *label) {
    for (int i = 0; i < LENS_COUNT; i++ ){
        const char *check = lenses[box][i].label;
        if (check != NULL && strcmp(check, label) == 0) {
            return i;
        }
    }
    return -1;
}

void opDash(Lens lenses[][LENS_COUNT], uint8_t box, const char *label) {
    int lens = findLens(lenses, box, label);
    if (lens >= 0) {
        lenses[box][lens].label = NULL;
        for(int i = lens; i < LENS_COUNT-1; i++) {
            lenses[box][i] = lenses[box][i+1];
        }
        lenses[box][LENS_COUNT-1].label = NULL;
    }
}

void opEq(Lens lenses[][LENS_COUNT], uint8_t box, const char *label, uint8_t focalLength) {
    int lens = findLens(lenses, box, label);
    if (lens >= 0) {
        lenses[box][lens].label = label;
        lenses[box][lens].focalLength = focalLength;
    } else {
        int i;
        for (i = 0; i < LENS_COUNT && lenses[box][i].label != NULL; i++);
        if (i == LENS_COUNT) assert(false && "LENS OVERFLOW");
        else {
            lenses[box][i].label = label;
            lenses[box][i].focalLength = focalLength;
        }
    }
}

long long eval(Lens lenses[][LENS_COUNT]) {
    long long ret = 0;
    for(int i = 0; i < BOX_COUNT; i++) {
        for(int j = 0; j < LENS_COUNT; j++){ 
            if (lenses[i][j].label != NULL) {
                ret += (i+1)*(j+1)*lenses[i][j].focalLength;
            }
        }
    }
    return ret;
}

int main(void) {
    char *line = NULL;
    size_t len = 0;
    ssize_t res;
    FILE *file = fopen("input15", "r");
    if (file == NULL) {
        puts("Failed to open file!");
        exit(-1);
    }

    long long sum = 0;
    char delim[2] = {0, 0};

    Lens lenses[BOX_COUNT][LENS_COUNT] = {};

    char *tokState1 = NULL;
    while ((res = getline(&line, &len, file)) != -1) {
        char *token = strtok_r(line, ",", &tokState1);
        while (token != NULL) {
            char *tokState2 = NULL;

            uint8_t hash = hash_str(token);
            sum += hash;

            char *dash = strchr(token, '-');
            char *eq = strchr(token, '=');
            char op = dash == NULL ? '=' : '-';
            delim[0] = op;

            char *label = strtok_r(token, delim, &tokState2);
            char *cmd = strtok_r(NULL, delim, &tokState2);

            uint8_t box = hash_str(label);

            switch(op) {
                case '-':
                    opDash(lenses, box, strdup(label));
                break;
                case '=':
                    int fl = atoi(cmd);
                    opEq(lenses, box, strdup(label), fl);
                break;
                default:
                    assert(false && "WHAT");
                break;
            }

            token = strtok_r(NULL, ",", &tokState1);
        }
    }
    printf("part1: %lld\n", sum);
    printf("part2: %lld\n", eval(lenses));

    fclose(file);
    // the OS will free the memory (^.^)
    return 0;
}
