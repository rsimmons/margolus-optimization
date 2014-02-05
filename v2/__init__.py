import os
import struct
import subprocess

description = 'C impl, one byte per cell, simple/dumb inner loop handling four cells per iteration'

def evolve(state, rule, iters):
    packed_pieces = []

    packed_pieces.append(struct.pack('=IIII', state['width'], state['height'], state['phase'], iters))

    packed_pieces.append(struct.pack('=16B', *rule))

    for c in state['cells']:
        packed_pieces.append(struct.pack('=B', int(c)))

    subproc_input = ''.join(packed_pieces)

    pobj = subprocess.Popen([os.path.join(os.path.dirname(__file__), 'evolve_simple_uint8')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (subproc_output, subproc_err) = pobj.communicate(subproc_input)
    assert pobj.returncode == 0
    # print 'debug output:', subproc_err

    assert len(subproc_output) == state['width']*state['height']

    return {
        'width': state['width'],
        'height': state['height'],
        'phase': (1 - state['phase']) if iters & 1 else state['phase'],
        'cells': [bool(ord(c)) for c in subproc_output],
    }
