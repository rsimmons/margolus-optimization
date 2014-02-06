#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint64_t UInt64;

void evolve_64_even(UInt64 *rule, UInt64 src, UInt64 *dst) {
    UInt64 result = 0;
    UInt64 qind0 = (src & 3ULL) | ((src & 768ULL) >> 6);
    UInt64 res0 = (rule[qind0]);
    result |= (res0 & 3ULL);
    result |= ((res0 & 12ULL) << 6);
    UInt64 qind1 = ((src & 12ULL) >> 2) | ((src & 3072ULL) >> 8);
    UInt64 res1 = (rule[qind1]);
    result |= ((res1 & 3ULL) << 2);
    result |= ((res1 & 12ULL) << 8);
    UInt64 qind2 = ((src & 48ULL) >> 4) | ((src & 12288ULL) >> 10);
    UInt64 res2 = (rule[qind2]);
    result |= ((res2 & 3ULL) << 4);
    result |= ((res2 & 12ULL) << 10);
    UInt64 qind3 = ((src & 192ULL) >> 6) | ((src & 49152ULL) >> 12);
    UInt64 res3 = (rule[qind3]);
    result |= ((res3 & 3ULL) << 6);
    result |= ((res3 & 12ULL) << 12);
    UInt64 qind4 = ((src & 196608ULL) >> 16) | ((src & 50331648ULL) >> 22);
    UInt64 res4 = (rule[qind4]);
    result |= ((res4 & 3ULL) << 16);
    result |= ((res4 & 12ULL) << 22);
    UInt64 qind5 = ((src & 786432ULL) >> 18) | ((src & 201326592ULL) >> 24);
    UInt64 res5 = (rule[qind5]);
    result |= ((res5 & 3ULL) << 18);
    result |= ((res5 & 12ULL) << 24);
    UInt64 qind6 = ((src & 3145728ULL) >> 20) | ((src & 805306368ULL) >> 26);
    UInt64 res6 = (rule[qind6]);
    result |= ((res6 & 3ULL) << 20);
    result |= ((res6 & 12ULL) << 26);
    UInt64 qind7 = ((src & 12582912ULL) >> 22) | ((src & 3221225472ULL) >> 28);
    UInt64 res7 = (rule[qind7]);
    result |= ((res7 & 3ULL) << 22);
    result |= ((res7 & 12ULL) << 28);
    UInt64 qind8 = ((src & 12884901888ULL) >> 32) | ((src & 3298534883328ULL) >> 38);
    UInt64 res8 = (rule[qind8]);
    result |= ((res8 & 3ULL) << 32);
    result |= ((res8 & 12ULL) << 38);
    UInt64 qind9 = ((src & 51539607552ULL) >> 34) | ((src & 13194139533312ULL) >> 40);
    UInt64 res9 = (rule[qind9]);
    result |= ((res9 & 3ULL) << 34);
    result |= ((res9 & 12ULL) << 40);
    UInt64 qind10 = ((src & 206158430208ULL) >> 36) | ((src & 52776558133248ULL) >> 42);
    UInt64 res10 = (rule[qind10]);
    result |= ((res10 & 3ULL) << 36);
    result |= ((res10 & 12ULL) << 42);
    UInt64 qind11 = ((src & 824633720832ULL) >> 38) | ((src & 211106232532992ULL) >> 44);
    UInt64 res11 = (rule[qind11]);
    result |= ((res11 & 3ULL) << 38);
    result |= ((res11 & 12ULL) << 44);
    UInt64 qind12 = ((src & 844424930131968ULL) >> 48) | ((src & 216172782113783808ULL) >> 54);
    UInt64 res12 = (rule[qind12]);
    result |= ((res12 & 3ULL) << 48);
    result |= ((res12 & 12ULL) << 54);
    UInt64 qind13 = ((src & 3377699720527872ULL) >> 50) | ((src & 864691128455135232ULL) >> 56);
    UInt64 res13 = (rule[qind13]);
    result |= ((res13 & 3ULL) << 50);
    result |= ((res13 & 12ULL) << 56);
    UInt64 qind14 = ((src & 13510798882111488ULL) >> 52) | ((src & 3458764513820540928ULL) >> 58);
    UInt64 res14 = (rule[qind14]);
    result |= ((res14 & 3ULL) << 52);
    result |= ((res14 & 12ULL) << 58);
    UInt64 qind15 = ((src & 54043195528445952ULL) >> 54) | ((src & 13835058055282163712ULL) >> 60);
    UInt64 res15 = (rule[qind15]);
    result |= ((res15 & 3ULL) << 54);
    result |= ((res15 & 12ULL) << 60);
    *dst = result;
}

void evolve_even(UInt64 *rule, int width_blocks, int height_blocks, UInt64 *start_pattern, UInt64 *end_pattern) {
    for (int i = 0; i < width_blocks*height_blocks; i++) {
        // don't need to zero dest for evolve_64_even
        evolve_64_even(rule, start_pattern[i], end_pattern + i);
    }
}

void evolve_odd(UInt64 *rule, int width_blocks, int height_blocks, UInt64 *start_pattern, UInt64 *end_pattern) {
    int c_idx, n_idx, nw_idx, w_idx;
    UInt64 src, dst;

    // necessary because evolve_64_odd or bits into dest
    bzero(end_pattern, width_blocks*height_blocks*sizeof(UInt64));

    int wh = width_blocks*height_blocks;

    c_idx = 0; n_idx = wh - width_blocks; nw_idx = wh - 1; w_idx = width_blocks - 1;
    for (int y = 0; y < height_blocks; y++) {
        for (int x = 0; x < width_blocks; x++) {
            src = ((start_pattern[nw_idx] >> 63) & 0x1ULL) | ((start_pattern[n_idx] >> 55) & 0xfeULL) | ((start_pattern[w_idx] << 1) & 0x101010101010100ULL) | ((start_pattern[c_idx] & 0x7f7f7f7f7f7f7fULL) << 9);

            evolve_64_even(rule, src, &dst);

            end_pattern[nw_idx] |= (dst & 0x1ULL) << 63;
            end_pattern[n_idx] |= (dst & 0xfeULL) << 55;
            end_pattern[w_idx] |= (dst & 0x101010101010100ULL) >> 1;
            end_pattern[c_idx] |= (dst >> 9) & 0x7f7f7f7f7f7f7fULL;

            w_idx = c_idx; c_idx++; nw_idx = n_idx; n_idx++;
        }
        n_idx = c_idx - width_blocks; w_idx = c_idx + width_blocks - 1; nw_idx = w_idx - width_blocks;
    }
}

void iterate(UInt64 *rule, int width_blocks, int height_blocks, UInt64 *start_pattern, UInt64 *end_pattern, int start_phase, int iters) {
    UInt64 *temp_patterns[2];

    for (int i = 0; i < 2; i++) {
        // not sure if alignment makes a difference, but just in case
        posix_memalign((void *)(temp_patterns+i), 64, width_blocks*height_blocks*sizeof(UInt64));
    }

    memcpy(temp_patterns[0], start_pattern, width_blocks*height_blocks*sizeof(UInt64));

    int cur_idx = 0;

    if (start_phase) {
        evolve_odd(rule, width_blocks, height_blocks, temp_patterns[cur_idx], temp_patterns[!cur_idx]);
        cur_idx = !cur_idx;
        iters--;
    }

    while (iters >= 2) {
        evolve_even(rule, width_blocks, height_blocks, temp_patterns[cur_idx], temp_patterns[!cur_idx]);
        cur_idx = !cur_idx;

        evolve_odd(rule, width_blocks, height_blocks, temp_patterns[cur_idx], temp_patterns[!cur_idx]);
        cur_idx = !cur_idx;

        iters -= 2;
    }

    if (iters) {
        evolve_even(rule, width_blocks, height_blocks, temp_patterns[cur_idx], temp_patterns[!cur_idx]);
        cur_idx = !cur_idx;
        iters--;
    }

    memcpy(end_pattern, temp_patterns[cur_idx], width_blocks*height_blocks*sizeof(UInt64));
}

int main(void) {
    uint32_t width_blocks, height_blocks, start_phase, iterations;
    fread(&width_blocks, sizeof(uint32_t), 1, stdin);
    fread(&height_blocks, sizeof(uint32_t), 1, stdin);
    fread(&start_phase, sizeof(uint32_t), 1, stdin);
    fread(&iterations, sizeof(uint32_t), 1, stdin);

    uint8_t rule[16];
    fread(rule, 16*sizeof(uint8_t), 1, stdin);

    UInt64 rule_64[16];
    for (int i = 0; i < 16; i++) {
        rule_64[i] = rule[i];
    }

    UInt64 *start_pattern = (UInt64 *)malloc(width_blocks*height_blocks*sizeof(UInt64));
    UInt64 *end_pattern = (UInt64 *)malloc(width_blocks*height_blocks*sizeof(UInt64));

    fread(start_pattern, width_blocks*height_blocks*sizeof(UInt64), 1, stdin);

    // fprintf(stderr, "%d %d %d %d\n", width_blocks, height_blocks, start_phase, iterations);

    iterate(rule_64, width_blocks, height_blocks, start_pattern, end_pattern, start_phase, iterations);

    fwrite(end_pattern, width_blocks*height_blocks*sizeof(UInt64), 1, stdout);

    return 0;
}
