import time
import re
import struct
import urlparse
import subprocess

SINGLE_ROT_RULE_SEQ = (0, 2, 8, 3, 1, 5, 6, 7, 4, 9, 10, 11, 12, 13, 14, 15)

def states_equal(a, b):
    return a['width'] == b['width'] and a['height'] == b['height'] and a['phase'] == b['phase'] and a['cells'] == b['cells']

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

def evolve_py_simple_int(state, iters):
    width = state['width']
    height = state['height']
    phase = state['phase']
    assert (width % 2) == 0
    assert (height % 2) == 0
    assert phase in (0, 1)
    rule = SINGLE_ROT_RULE_SEQ

    icells = [int(x) for x in state['cells']]
    assert len(icells) == width*height

    for i in range(iters):
        x0 = y0 = phase
        for y in range(y0, height, 2):
            dy = width if ((y + 1) < height) else (width*(1 - height))
            a = y*width + x0
            for x in range(x0, width, 2):
                dx = 1 if ((x + 1) < width) else (1 - width)
                b = a + dx
                c = a + dy
                d = b + dy

                inp = icells[a] | (icells[b] << 1) | (icells[c] << 2) | (icells[d] << 3)
                out = rule[inp]

                if out != inp:
                    icells[a] = out & 1
                    icells[b] = (out >> 1) & 1
                    icells[c] = (out >> 2) & 1
                    icells[d] = (out >> 3) & 1

                a += 2

        phase = 1 - phase
        if ((i+1) % 1000) == 1:
            print i

    return {
        'width': width,
        'height': height,
        'phase': phase,
        'cells': [bool(x) for x in icells],
    }

def evolve_c_simple_uint8(state, iters):
    packed_pieces = []
    packed_pieces.append(struct.pack('=IIII', state['width'], state['height'], state['phase'], iters))

    for c in state['cells']:
        packed_pieces.append(struct.pack('=B', int(c)))

    subproc_input = ''.join(packed_pieces)

    pobj = subprocess.Popen(['./evolve_simple_uint8'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

def evolve_block_64_cgen(state, iters):
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

    pobj = subprocess.Popen(['./evolve_block_64_cgen'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

if __name__ == '__main__':
    test_start_url = 'http://dmishin.github.io/js-revca/index.html?rule=0,2,8,3,1,5,6,7,4,9,10,11,12,13,14,15&rle_x0=24&rle_y0=20&rle=bo4b3obobo$2b6o3b2o$8ob3o$4bobo5bo$3bob3o$bo2bobo4bo$ob5ob5o$4o2bob3obo$4b2ob2obobo$3ob2o2bo3bo$bob2obo3b3o$2o3bo2bobobo$b2o2b2ob2o2bo$3o2bob2obobo$bob3obobo2bo&step=1&frame_delay=10&size=64x64&cell_size=8,1&phase=0'
    test_end_url = 'http://dmishin.github.io/js-revca/index.html?rule=0,2,8,3,1,5,6,7,4,9,10,11,12,13,14,15&rle_x0=1&rle_y0=1&rle=15bo$5bo2$30bo$6bo52bo$o3$31bo2$15bo$35bo23bo$7bo31bo2$25bo$25bo17bo18bo$58bo$20bo$54bo2$25b6obo$22bo2b6o$29bo$4bo23b2o$27bobo$26b4o2b4o$21bo4bo2b2ob2ob2o$14bo12b2o2bo3bo9bo$27b2ob2o2b2o4bo$22bo4bo2b3obo$28bo2bobo$24b2o3bo2bo11bo$24b2o4b2o10bo$57bo$25bo$4bo$3bo$33bo3$31bo$38bo$45bo$25bo4bo8$25bo2$15bo$58bo$24bobo5$24bo2$32bo&step=1024&frame_delay=10&size=64x64&cell_size=8,1&phase=0'
    test_iters = 467968

    test_start_state = parse_dmishin_url(test_start_url)
    test_end_state = parse_dmishin_url(test_end_url)

    # print format_state(test_start_state)

    for ef in (evolve_c_simple_uint8, evolve_block_64_cgen):
        t0 = time.time()
        end_state = ef(test_start_state, test_iters)
        dt = time.time() - t0
        # print format_state(end_state)
        assert states_equal(test_end_state, end_state)
        print '%s: %d iters/s' % (ef.__name__, int(test_iters/dt))
