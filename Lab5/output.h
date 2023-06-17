#ifndef OUTPUT_H_
#define OUTPUT_H_

#include <stdbool.h>

bool
writebytes (unsigned long long x, int nbytes);

int
handleOutput( unsigned long long (*rand64) (void), bool stdio, long long nbytes, unsigned int nInt);

#endif //OUTPUT_H_