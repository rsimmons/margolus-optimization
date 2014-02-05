#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

int main(void) {
    uint32_t arg_width, arg_height, arg_phase, arg_iterations;
    fread(&arg_width, sizeof(uint32_t), 1, stdin);
    fread(&arg_height, sizeof(uint32_t), 1, stdin);
    fread(&arg_phase, sizeof(uint32_t), 1, stdin);
    fread(&arg_iterations, sizeof(uint32_t), 1, stdin);
    int width = arg_width;
    int height = arg_height;
    int phase = arg_phase;
    int iterations = arg_iterations;

    assert((width % 2) == 0);
    assert((height % 2) == 0);
    assert((phase == 0) || (phase == 1));

    uint8_t rule[16];

    fread(rule, 16*sizeof(uint8_t), 1, stdin);

    uint8_t *cells = (uint8_t *)malloc(width*height*sizeof(uint8_t));

    fread(cells, width*height*sizeof(uint8_t), 1, stdin);

    int x0, y0;
    int x, y;
    int dx, dy, a, b, c, d;
    uint8_t inp, out;
    for (int i = 0; i < iterations; i++) {
        x0 = y0 = phase;
        for (y = y0; y < height; y += 2) {
            dy = ((y + 1) < height) ? width : (width*(1 - height));
            a = y*width + x0;
            for (x = x0; x < width; x += 2) {
                dx = ((x + 1) < width) ? 1 : (1 - width);
                b = a + dx;
                c = a + dy;
                d = b + dy;

                inp = cells[a] | (cells[b] << 1) | (cells[c] << 2) | (cells[d] << 3);
                out = rule[inp];

                if (out != inp) {
                    cells[a] = out & 1;
                    cells[b] = (out >> 1) & 1;
                    cells[c] = (out >> 2) & 1;
                    cells[d] = (out >> 3) & 1;
                }

                a += 2;
            }
        }

        phase = 1 - phase;
    }

    fwrite(cells, width*height*sizeof(uint8_t), 1, stdout);

    return 0;
}
