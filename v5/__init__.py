import os

import subproc_util

description = 'C impl, one bit per cell, fancy code-gen even/odd inner loops handling 64 cells with 16-entry array rule lookup. better edge wrap handling on odd phase. based on v3, improved odd phase edge wrap'

def evolve(state, rule, iters):
    return subproc_util.evolve_block_64_cgen(os.path.join(os.path.dirname(__file__), 'evolve_bin'), state, rule, iters)

