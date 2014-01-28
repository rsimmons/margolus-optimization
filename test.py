import rule
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

if __name__ == '__main__':
    rule = rule.encode_rule((0, 2, 8, 3, 1, 5, 6, 7, 4, 9, 10, 11, 12, 13, 14, 15))
    x = load_64('pat.txt')
    print x
    print dump_64(x)
    x = evolve.evolve_64_even(rule, x)
    print dump_64(x)
