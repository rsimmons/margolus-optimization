import sys
import time

import util
import rule

if __name__ == '__main__':
    rule = rule.encode_rule((0, 2, 8, 3, 1, 5, 6, 7, 4, 9, 10, 11, 12, 13, 14, 15))
    print 'rule:', rule
    pat = util.load_64('pat.txt')
    print pat

    for i in range(1, 10):
        print util.iterate_64(rule, pat, i)
    sys.exit(0)

    reps = 24

    t0 = time.time()
    pat = util.iterate_64(rule, pat, reps)
    dt = time.time() - t0
    print util.dump_64(pat)
    print float(reps)/dt, 'iters per second'
