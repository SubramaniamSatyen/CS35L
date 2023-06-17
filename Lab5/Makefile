# Make x86-64 random byte generators.

# Copyright 2015, 2020, 2021 Paul Eggert

# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

# Optimization level.  Change this -O2 to -Og or -O0 or whatever.
OPTIMIZE = -O2

# The C compiler and its options.
CC = gcc
CFLAGS = $(OPTIMIZE) -g3 -Wall -Wextra -fanalyzer \
  -march=native -mtune=native -mrdrnd 

# The archiver command, its options and filename extension.
TAR = tar
TARFLAGS = --gzip --transform 's,^,randall/,'
TAREXT = tgz

default: randall 

randall: rand64-hw.o rand64-sw.o output.o options.o randall.o
	$(CC) $(CFLAGS) $^ -o $@

options.o: options.c options.h
	$(CC) $(CFLAGS) options.c -o options.o -c

output.o: output.c output.h
	$(CC) $(CFLAGS) output.c -o output.o -c

rand64-sw.o: rand64-sw.c rand64-sw.h
	$(CC) $(CFLAGS) rand64-sw.c -o rand64-sw.o -c

randall.o: randall.c rand64-hw.h
	$(CC) $(CFLAGS) randall.c -o randall.o -c

rand64-hw.o: rand64-hw.c rand64-hw.h
	$(CC) $(CFLAGS) rand64-hw.c -o rand64-hw.o -c

assignment: randall-assignment.$(TAREXT)
assignment-files = COPYING Makefile randall.c
randall-assignment.$(TAREXT): $(assignment-files)
	$(TAR) $(TARFLAGS) -cf $@ $(assignment-files)

submission-tarball: randall-submission.$(TAREXT)
submission-files = $(assignment-files) \
  notes.txt options.c options.h output.c output.h rand64-hw.c rand64-hw.h rand64-sw.c rand64-sw.h # More files should be listed here, as needed.
randall-submission.$(TAREXT): $(submission-files)
	$(TAR) $(TARFLAGS) -cf $@ $(submission-files)

repository-tarball:
	$(TAR) -czf randall-git.tgz .git

.PHONY: default clean assignment submission-tarball repository-tarball

clean:
	rm -f *.o *.$(TAREXT) randall

testNum = 10
check: randall
	@if [ `./randall $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) - Passed"; \
		else echo "./randall $(testNum) - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i rdrand | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i rdrand | wc -c - Passed"; \
		else echo "./randall $(testNum) -i rdrand | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i mrand48_r  | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i mrand48_r  | wc -c - Passed"; \
		else echo "./randall $(testNum) -i mrand48_r  | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i rdrand | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i rdrand | wc -c - Passed"; \
		else echo "./randall $(testNum) -i rdrand | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i /dev/random | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i /dev/random | wc -c - Passed"; \
		else echo "./randall $(testNum) -i /dev/random | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -o stdio | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -o stdio | wc -c - Passed"; \
		else echo "./randall $(testNum) -o stdio | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -o 2 | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -o 2 | wc -c - Passed"; \
		else echo "./randall $(testNum) -o 2 | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -o 20 | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -o 20 | wc -c - Passed"; \
		else echo "./randall $(testNum) -o 20 | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i rdrand -o 2 | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i rdrand -o 2 | wc -c - Passed"; \
		else echo "./randall $(testNum) -i rdrand -o 2 | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i mrand48_r -o 2 | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i mrand48_r -o 2 | wc -c - Passed"; \
		else echo "./randall $(testNum) -i mrand48_r -o 2 | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i rdrand -o 2 | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i rdrand -o 2 | wc -c - Passed"; \
		else echo "./randall $(testNum) -i rdrand -o 2 | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i /dev/random -o 2 | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i /dev/random -o 2 | wc -c - Passed"; \
		else echo "./randall $(testNum) -i /dev/random -o 2 | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i rdrand -o 20 | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i rdrand -o 20 | wc -c - Passed"; \
		else echo "./randall $(testNum) -i rdrand -o 20 | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i mrand48_r -o 20 | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i mrand48_r -o 20 | wc -c - Passed"; \
		else echo "./randall $(testNum) -i mrand48_r -o 20 | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i rdrand -o 20 | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i rdrand -o 20 | wc -c - Passed"; \
		else echo "./randall $(testNum) -i rdrand -o 20 | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i /dev/random -o 20 | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i /dev/random -o 20 | wc -c - Passed"; \
		else echo "./randall $(testNum) -i /dev/random -o 20 | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i rdrand -o stdio | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i rdrand -o stdio | wc -c - Passed"; \
		else echo "./randall $(testNum) -i rdrand -o stdio | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i mrand48_r -o stdio | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i mrand48_r -o stdio | wc -c - Passed"; \
		else echo "./randall $(testNum) -i mrand48_r -o stdio | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i rdrand -o stdio | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i rdrand -o stdio | wc -c - Passed"; \
		else echo "./randall $(testNum) -i rdrand -o stdio | wc -c - FAILED"; \
	fi
	@if [ `./randall $(testNum) -i /dev/random -o stdio | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) -i /dev/random -o stdio | wc -c - Passed"; \
		else echo "./randall $(testNum) -i /dev/random -o stdio | wc -c - FAILED"; \
	fi
