#!/bin/bash
gcc -std=c99 -Wall -O3 -o evolve_block_64_cgen_array_rule evolve_block_64_cgen_array_rule.c
gcc -std=c99 -Wall -O3 -o evolve_block_64_cgen_packed_rule evolve_block_64_cgen_packed_rule.c
gcc -std=c99 -Wall -O3 -o evolve_simple_uint8 evolve_simple_uint8.c
