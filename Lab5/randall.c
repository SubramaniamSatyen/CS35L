/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

#include <cpuid.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include "options.h"
#include <unistd.h>
#include <string.h>
#include "output.h"
#include "rand64-hw.h"
#include "rand64-sw.h"

/* Main program, which outputs N bytes of random data.  */
int
main (int argc, char **argv)
{
  struct optionInfo optionStatus;
  parseOptions(argc, argv, &optionStatus);

  if (!optionStatus.valid) {
    fprintf (stderr, "%s: usage: %s NBYTES\n", argv[0], argv[0]);
    return 1;
  }  
  
  /* If there's no work to do, don't worry about which library to use.  */
  if (optionStatus.nbytes == 0)
    return 0;

  /* Now that we know we have work to do, arrange to use the
     appropriate library.  */

  unsigned long long (*rand64) (void);
  void (*finalize) (void);

  if (optionStatus.file) {
    int errFile = software_rand64_init(optionStatus.path);
    if (errFile){
      return 1;
    }
    rand64 = software_rand64;
    finalize = software_rand64_fini;
  }
  if (optionStatus.mrand48_r) {
    hardware_rand48_init();
    rand64 = hardware_rand48;
    finalize = hardware_rand48_fini;
  }
  else {
    if (!rdrand_supported ()){
      fprintf (stderr, "x86-64 random hardware 'rdrand' not available.\n");
      return 1;
    }
    hardware_rand64_init();
    rand64 = hardware_rand64;
    finalize = hardware_rand64_fini;
  }

  int output_errno = handleOutput(rand64, optionStatus.stdio, optionStatus.nbytes, optionStatus.nInt);

  finalize ();
  return !!output_errno;
}
