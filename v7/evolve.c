#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint64_t UInt64;

void evolve_64_even(UInt64 *rule, UInt64 src, UInt64 *dst) {
    UInt64 result = 0;
    UInt64 qind0 = (src & 15ULL);
    UInt64 res0 = (rule[qind0]);
    result |= (res0 & 15ULL);
    UInt64 qind1 = ((src & 240ULL) >> 4);
    UInt64 res1 = (rule[qind1]);
    result |= ((res1 & 15ULL) << 4);
    UInt64 qind2 = ((src & 3840ULL) >> 8);
    UInt64 res2 = (rule[qind2]);
    result |= ((res2 & 15ULL) << 8);
    UInt64 qind3 = ((src & 61440ULL) >> 12);
    UInt64 res3 = (rule[qind3]);
    result |= ((res3 & 15ULL) << 12);
    UInt64 qind4 = ((src & 983040ULL) >> 16);
    UInt64 res4 = (rule[qind4]);
    result |= ((res4 & 15ULL) << 16);
    UInt64 qind5 = ((src & 15728640ULL) >> 20);
    UInt64 res5 = (rule[qind5]);
    result |= ((res5 & 15ULL) << 20);
    UInt64 qind6 = ((src & 251658240ULL) >> 24);
    UInt64 res6 = (rule[qind6]);
    result |= ((res6 & 15ULL) << 24);
    UInt64 qind7 = ((src & 4026531840ULL) >> 28);
    UInt64 res7 = (rule[qind7]);
    result |= ((res7 & 15ULL) << 28);
    UInt64 qind8 = ((src & 64424509440ULL) >> 32);
    UInt64 res8 = (rule[qind8]);
    result |= ((res8 & 15ULL) << 32);
    UInt64 qind9 = ((src & 1030792151040ULL) >> 36);
    UInt64 res9 = (rule[qind9]);
    result |= ((res9 & 15ULL) << 36);
    UInt64 qind10 = ((src & 16492674416640ULL) >> 40);
    UInt64 res10 = (rule[qind10]);
    result |= ((res10 & 15ULL) << 40);
    UInt64 qind11 = ((src & 263882790666240ULL) >> 44);
    UInt64 res11 = (rule[qind11]);
    result |= ((res11 & 15ULL) << 44);
    UInt64 qind12 = ((src & 4222124650659840ULL) >> 48);
    UInt64 res12 = (rule[qind12]);
    result |= ((res12 & 15ULL) << 48);
    UInt64 qind13 = ((src & 67553994410557440ULL) >> 52);
    UInt64 res13 = (rule[qind13]);
    result |= ((res13 & 15ULL) << 52);
    UInt64 qind14 = ((src & 1080863910568919040ULL) >> 56);
    UInt64 res14 = (rule[qind14]);
    result |= ((res14 & 15ULL) << 56);
    UInt64 qind15 = ((src & 17293822569102704640ULL) >> 60);
    UInt64 res15 = (rule[qind15]);
    result |= ((res15 & 15ULL) << 60);
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
            src = ((start_pattern[nw_idx] >> 63) & 0x1ULL) | ((start_pattern[n_idx] >> 13) & 0x2000200020002ULL) | ((start_pattern[n_idx] << 1) & 0x1000100010000ULL) | ((start_pattern[w_idx] >> 47) & 0x5554ULL) | ((start_pattern[c_idx] & 0x1555155515551555ULL) << 3) | ((start_pattern[c_idx] & 0x2aaa2aaa2aaaULL) << 17);

            evolve_64_even(rule, src, &dst);

            end_pattern[nw_idx] |= (dst & 0x1ULL) << 63;
            end_pattern[n_idx] |= (dst & 0x2000200020002ULL) << 13;
            end_pattern[n_idx] |= (dst & 0x1000100010000ULL) >> 1;
            end_pattern[w_idx] |= (dst & 0x5554ULL) << 47;
            end_pattern[c_idx] |= (dst >> 3) & 0x1555155515551555ULL;
            end_pattern[c_idx] |= (dst >> 17) & 0x2aaa2aaa2aaaULL;

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
