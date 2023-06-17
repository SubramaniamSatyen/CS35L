#include "rand64-hw.h"
#include <immintrin.h>
#include <cpuid.h>
#include <time.h>

/* Description of the current CPU.  */
struct cpuid { unsigned eax, ebx, ecx, edx; };

/* Return information about the CPU.  See <http://wiki.osdev.org/CPUID>.  */
static struct cpuid
cpuid (unsigned int leaf, unsigned int subleaf)
{
  struct cpuid result;
  asm ("cpuid"
       : "=a" (result.eax), "=b" (result.ebx),
	 "=c" (result.ecx), "=d" (result.edx)
       : "a" (leaf), "c" (subleaf));
  return result;
}

/* Return true if the CPU supports the RDRAND instruction.  */
bool
rdrand_supported (void)
{
  struct cpuid extended = cpuid (1, 0);
  return (extended.ecx & bit_RDRND) != 0;
}

/* Initialize the hardware rand64 implementation.  */
void
hardware_rand64_init (void)
{
}

/* Return a random value, using hardware operations.  */
unsigned long long
hardware_rand64 (void)
{
  unsigned long long int x;
  while (! _rdrand64_step (&x))
    continue;
  return x;
}

/* Finalize the hardware rand64 implementation.  */
void
hardware_rand64_fini (void)
{
}


static struct drand48_data buffer;
/* Initialize the hardware rand64 implementation.  */
void
hardware_rand48_init (void)
{
  srand48_r(time(NULL), &buffer);
}

/* Return a random value, using hardware operations.  */
unsigned long long
hardware_rand48 (void)
{
  long int x;
  srand48_r(time(NULL), &buffer);
  mrand48_r (&buffer, &x);
  return (unsigned long long) x;
}

/* Finalize the hardware rand64 implementation.  */
void
hardware_rand48_fini (void)
{
}