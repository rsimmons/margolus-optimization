description = 'Python impl, one int per cell, simple/dumb inner loop handling four cells per iteration'

def evolve(state, rule, iters):
    width = state['width']
    height = state['height']
    phase = state['phase']
    assert (width % 2) == 0
    assert (height % 2) == 0
    assert phase in (0, 1)

    icells = [int(x) for x in state['cells']]
    assert len(icells) == width*height

    for i in range(iters):
        x0 = y0 = phase
        for y in range(y0, height, 2):
            dy = width if ((y + 1) < height) else (width*(1 - height))
            a = y*width + x0
            for x in range(x0, width, 2):
                dx = 1 if ((x + 1) < width) else (1 - width)
                b = a + dx
                c = a + dy
                d = b + dy

                inp = icells[a] | (icells[b] << 1) | (icells[c] << 2) | (icells[d] << 3)
                out = rule[inp]

                if out != inp:
                    icells[a] = out & 1
                    icells[b] = (out >> 1) & 1
                    icells[c] = (out >> 2) & 1
                    icells[d] = (out >> 3) & 1

                a += 2

        phase = 1 - phase
        if ((i+1) % 1000) == 1:
            print i

    return {
        'width': width,
        'height': height,
        'phase': phase,
        'cells': [bool(x) for x in icells],
    }
