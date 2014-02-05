import subprocess
import struct

def evolve_block_64_cgen(exename, state, rule, iters):
    # pack up width, height, phase, data
    assert (state['width'] % 8) == 0
    assert (state['height'] % 8) == 0
    width_blocks = state['width'] / 8
    height_blocks = state['height'] / 8

    packed_pieces = []
    packed_pieces.append(struct.pack('=IIII', width_blocks, height_blocks, state['phase'], iters))

    packed_pieces.append(struct.pack('=16B', *rule))

    for by in range(height_blocks):
        for bx in range(width_blocks):
            qw = 0
            bit_idx = 0
            for suby in range(8):
                for subx in range(8):
                    cell_idx = state['width']*(8*by + suby) + (8*bx + subx)
                    qw |= int(state['cells'][cell_idx]) << bit_idx
                    bit_idx += 1

            packed_pieces.append(struct.pack('=Q', qw))

    subproc_input = ''.join(packed_pieces)

    pobj = subprocess.Popen([exename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (subproc_output, subproc_err) = pobj.communicate(subproc_input)
    assert pobj.returncode == 0
    # print 'debug output:', subproc_err

    assert len(subproc_output) == 8*width_blocks*height_blocks

    end_state = {}
    end_state['width'] = state['width']
    end_state['height'] = state['height']
    end_state['phase'] = (1 - state['phase']) if iters & 1 else state['phase']
    end_state['cells'] = (end_state['width']*end_state['height'])*[False]

    qwi = 0
    for by in range(height_blocks):
        for bx in range(width_blocks):
            (qw,) = struct.unpack('=Q', subproc_output[8*qwi:][:8])
            bit_idx = 0
            for suby in range(8):
                for subx in range(8):
                    cell_idx = end_state['width']*(8*by + suby) + (8*bx + subx)
                    end_state['cells'][cell_idx] = bool(qw & (1 << bit_idx))
                    bit_idx += 1            
            qwi += 1

    return end_state
