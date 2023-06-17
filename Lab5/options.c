#include "options.h"
#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

void 
parseOptions(int argc, char **argv, struct optionInfo* ret){
  /* Check arguments.  */
  bool valid = true;
  long long nbytes = 0;

  bool rdrand = true;
  bool mrand48_r = false;
  bool file = false;
  char* path = "";

  bool stdio = true;
  bool N = false;
  unsigned int nInt = 0;
  
  int c;
  while ((c = getopt(argc, argv, ":i:o:")) != -1) {
    switch(c){
    case 'i':
      if (strcmp(optarg, "rdrand") == 0){
	rdrand = true;
	mrand48_r = false;
	file = false;
	break;
      }
      else if (strcmp(optarg, "mrand48_r") == 0){
	rdrand = false;
	mrand48_r = true;
	file = false;
      }
      else if (optarg[0] == '/'){
	rdrand = false;
	mrand48_r = false;
	file = true;
	path = optarg;
      }
      else{
	fprintf (stderr, "Option -i requires an operand 'rdrand', 'mrand48_r', '/...'\n");
	valid = false;
      }
      break;
    case 'o':
      if (strcmp(optarg, "stdio") == 0){
	stdio = true;
  N = false;
      }
      else {
  stdio = false;
  N = true;

    char *endptr;
    errno = 0;
	  nInt = strtoul (optarg, &endptr, 10);
    if (errno){
      perror (optarg);
      valid = false;
      }
    else{ 
      valid = !*endptr && 0 <= nbytes && valid;
    }

	if (nInt == 0){
	  fprintf (stderr, "Option -o requires an integer operand\n");
	  valid = false;
	}

      }
      break;
    case ':':
      fprintf (stderr, "Option -%c requires an operand\n", optopt);
      valid = false;
      break;
    case '?':
      fprintf (stderr, "Unrecognized option: '-%c'\n", optopt);
      valid = false;
      break;
    }
  }

  if (optind != argc - 1 || valid == false){
    valid = false;
  } 
  else {
    char *endptr;
    errno = 0;
    nbytes = strtoll (argv[optind], &endptr, 10);
    if (errno) {
      perror (argv[optind]);
      valid = false;
    }
    else {
      valid = !*endptr && 0 <= nbytes && valid;
    }
  }

  ret->nInt = nInt;
  ret->path = path;
  ret->valid = valid;
  ret->stdio = stdio;
  ret->N = N;
  ret->rdrand = rdrand;
  ret->mrand48_r = mrand48_r;
  ret->file = file;
  ret->nbytes = nbytes;
}