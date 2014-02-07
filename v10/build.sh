#!/bin/bash
gcc -std=c99 -Wall -O3 -o evolve_bin evolve.c

gcc -std=c99 -Wall -O3 -S -fverbose-asm -g -o evolve.s evolve.c
