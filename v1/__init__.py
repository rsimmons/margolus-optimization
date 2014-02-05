import os

import subproc_util

description = 'C impl, one bit per cell, fancy code-gen even/odd inner loops handling 64 cells with 16-entry shift-based rule lookup'

def evolve(state, rule, iters):
    # TODO: make use of rule
    return subproc_util.evolve_block_64_cgen(os.path.join(os.path.dirname(__file__), 'evolve_block_64_cgen_packed_rule'), state, rule, iters)

