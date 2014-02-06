import os

import subproc_util

description = 'C impl, one bit per cell, even-only inner loop handling 64 cells in 2-bit columns with 16-entry array rule lookup. based on v6, changed cell to bit mapping order'

def evolve(state, rule, iters):
    return subproc_util.evolve_block_64_columns(os.path.join(os.path.dirname(__file__), 'evolve_bin'), state, rule, iters)

