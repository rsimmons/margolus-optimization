import re
import struct
import urlparse
import subprocess

def format_state(state):
    idx = 0
    cs = []
    for y in range(state['height']):
        for x in range(state['width']):
            cs.append('X' if state['cells'][idx] else '.')
            idx += 1
        cs.append('\n')
    return ''.join(cs)

RLE_RE = re.compile(r'([0-9]+)?(b|o|\$)')
def parse_dmishin_url(url):
    result = {}
    qargs = urlparse.parse_qs(urlparse.urlparse(url).query)
    result['width'], result['height'] = [int(x) for x in qargs['size'][0].split('x')]
    result['phase'] = int(qargs['phase'][0])

    rle_x0 = int(qargs['rle_x0'][0])
    rle_y0 = int(qargs['rle_y0'][0])

    rle = qargs['rle'][0]

    pattern = (result['width']*result['height'])*[False]

    x = rle_x0
    y = rle_y0
    for match in RLE_RE.finditer(rle):
        count = int(match.group(1) or 1)
        tag = match.group(2)
        if tag == 'b':
            x += count
        elif tag == 'o':
            for i in range(count):
                pattern[x + y*result['width']] = True
                x += 1
        elif tag == '$':
            x = rle_x0
            y += count
        else:
            assert False

    result['cells'] = pattern

    return result

def format_dmishin_url(state):
    pass

def evolve_using_subproc(state, iters):
    # pack up width, height, phase, data
    assert (state['width'] % 8) == 0
    assert (state['height'] % 8) == 0
    width_blocks = state['width'] / 8
    height_blocks = state['height'] / 8

    packed_pieces = []
    packed_pieces.append(struct.pack('=IIII', width_blocks, height_blocks, state['phase'], iters))

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

    pobj = subprocess.Popen(['./test'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (subproc_output, subproc_err) = pobj.communicate(subproc_input)
    assert pobj.returncode == 0
    print 'debug output:', subproc_err

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

if __name__ == '__main__':
    test_url = 'http://dmishin.github.io/js-revca/index.html?rule=0,2,8,3,1,5,6,7,4,9,10,11,12,13,14,15&rle_x0=24&rle_y0=20&rle=bo4b3obobo$2b6o3b2o$8ob3o$4bobo5bo$3bob3o$bo2bobo4bo$ob5ob5o$4o2bob3obo$4b2ob2obobo$3ob2o2bo3bo$bob2obo3b3o$2o3bo2bobobo$b2o2b2ob2o2bo$3o2bob2obobo$bob3obobo2bo&step=1&frame_delay=10&size=64x64&cell_size=8,1&phase=0'

    start_state = parse_dmishin_url(test_url)
    print format_state(start_state)
    end_state = evolve_using_subproc(start_state, 2)
    print format_state(end_state)
