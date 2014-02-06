import os

import subproc_util

description = 'C impl, one bit per cell, fancy code-gen even-only inner loop handling 64 cells with 16-entry array rule lookup. based on v5, removed odd-phase inner code, doing shifting in outer func instead'

def evolve(state, rule, iters):
    return subproc_util.evolve_block_64_cgen(os.path.join(os.path.dirname(__file__), 'evolve_bin'), state, rule, iters)

