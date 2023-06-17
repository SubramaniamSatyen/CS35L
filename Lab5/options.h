#ifndef OPTIONS_H_
#define OPTIONS_H_

#include <stdbool.h>

struct optionInfo{
    bool valid;
    bool rdrand;
    bool mrand48_r;
    bool file;
    bool stdio;
    bool N;
    char* path;
    unsigned int nInt;
    long long nbytes;
};

void parseOptions(int argc, char **argv, struct optionInfo* ret);

#endif //OPTIONS_H_