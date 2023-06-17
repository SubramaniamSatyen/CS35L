#ifndef HW_H_
#define HW_H_

#include <stdbool.h>

/* Return true if the CPU supports the RDRAND instruction.  */
bool
rdrand_supported (void);

/* Initialize the hardware rand64 implementation.  */
void
hardware_rand64_init (void);

/* Return a random value, using hardware operations.  */
unsigned long long
hardware_rand64 (void);


/* Finalize the hardware rand64 implementation.  */
void
hardware_rand64_fini (void);

/* Initialize the hardware rand64 implementation.  */
void
hardware_rand48_init (void);

/* Return a random value, using hardware operations.  */
unsigned long long
hardware_rand48 (void);

/* Finalize the hardware rand64 implementation.  */
void
hardware_rand48_fini (void);

#endif //HW_H_