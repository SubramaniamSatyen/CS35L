#include "output.h"
#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>


bool
writebytes (unsigned long long x, int nbytes)
{
  do
    {
      if (putchar (x) < 0)
	return false;
      x >>= CHAR_BIT;
      nbytes--;
    }
  while (0 < nbytes);

  return true;
}

int
handleOutput( unsigned long long (*rand64) (void), bool stdio, long long nbytes, unsigned int nInt){
  int wordsize = sizeof rand64 ();
  int output_errno = 0;

  if (stdio){
    do
    {
      unsigned long long x = rand64 ();
      int outbytes = nbytes < wordsize ? nbytes : wordsize;
      if (!writebytes (x, outbytes)) {
        output_errno = errno;
        break;
      }
      nbytes -= outbytes;
    }
    while (0 < nbytes);

    if (fclose (stdout) != 0)
      output_errno = errno;

    if (output_errno) {
      errno = output_errno;
      perror ("output");
      return 1;
    }
  }
  else {
    unsigned long long x;
    char* buffer = malloc(nInt);

    int outbytes;
    long long bufSize = nInt; 

    do {
      outbytes = nbytes < bufSize ? nbytes : bufSize;
      for (size_t k = 0; k < outbytes; k+= sizeof(x) ){
        x = rand64();
        for (size_t i = 0; i < sizeof(x); i++){
          if (i + k >= outbytes){
            break;
          }
          unsigned char byte= *((unsigned char *)&x + i);
          buffer[k + i] = byte;
        }
      }
      int written = write(1, buffer, outbytes);
      if (written == -1){
        free(buffer);
        fprintf (stderr, "Error while writing bytes\n");
        return 1;
      }
      nbytes -= written;
    }
    while (0 < nbytes);
    
    free(buffer);
  }
  return output_errno;
}