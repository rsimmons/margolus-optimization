import evolve

def load_64(fn):
    yind = 0
    result = 0
    with open(fn) as f:
        for line in f:
            sline = line.strip()
            if sline.startswith('#'):
                continue
            assert len(sline) == 8
            for i, c in enumerate(sline):
                v = 1 if c in 'xX' else 0
                result |= (v << (i + 8*yind))
            yind += 1
    return result

def dump_64(pat):
    cs = []
    shift = 0
    for y in range(8):
        for x in range(8):
            v = ((1 << shift) & pat) >> shift
            cs.append('X' if v else '.')
            shift += 1
        cs.append('\n')
    return ''.join(cs)

def iterate_64(rule, pat, iters):
    for i in range(iters>>1):
        pat = evolve.evolve_64_even(rule, pat)
        pat_c, pat_n, pat_nw, pat_w = evolve.evolve_64_odd(rule, pat, pat, pat, pat)
        pat = pat_c | pat_n | pat_nw | pat_w

    if iters & 1:
        pat = evolve.evolve_64_even(rule, pat)

    return pat

