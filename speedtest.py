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

import v1, v2, v3, v4, v5

if __name__ == '__main__':
    test_start_url = 'http://dmishin.github.io/js-revca/index.html?rule=0,2,8,3,1,5,6,7,4,9,10,11,12,13,14,15&rle_x0=24&rle_y0=20&rle=bo4b3obobo$2b6o3b2o$8ob3o$4bobo5bo$3bob3o$bo2bobo4bo$ob5ob5o$4o2bob3obo$4b2ob2obobo$3ob2o2bo3bo$bob2obo3b3o$2o3bo2bobobo$b2o2b2ob2o2bo$3o2bob2obobo$bob3obobo2bo&step=1&frame_delay=10&size=64x64&cell_size=8,1&phase=0'
    test_end_url = 'http://dmishin.github.io/js-revca/index.html?rule=0,2,8,3,1,5,6,7,4,9,10,11,12,13,14,15&rle_x0=1&rle_y0=1&rle=15bo$5bo2$30bo$6bo52bo$o3$31bo2$15bo$35bo23bo$7bo31bo2$25bo$25bo17bo18bo$58bo$20bo$54bo2$25b6obo$22bo2b6o$29bo$4bo23b2o$27bobo$26b4o2b4o$21bo4bo2b2ob2ob2o$14bo12b2o2bo3bo9bo$27b2ob2o2b2o4bo$22bo4bo2b3obo$28bo2bobo$24b2o3bo2bo11bo$24b2o4b2o10bo$57bo$25bo$4bo$3bo$33bo3$31bo$38bo$45bo$25bo4bo8$25bo2$15bo$58bo$24bobo5$24bo2$32bo&step=1024&frame_delay=10&size=64x64&cell_size=8,1&phase=0'
    test_iters = 467968

    test_start_state = parse_dmishin_url(test_start_url)
    test_end_state = parse_dmishin_url(test_end_url)

    # print format_state(test_start_state)
    evolve_modules = [
        v1,
        v2,
        v3,
        # v4,
        v5,
    ]

    for mod in evolve_modules:
        t0 = time.time()
        end_state = mod.evolve(test_start_state, SINGLE_ROT_RULE_SEQ, test_iters)
        dt = time.time() - t0
        # print format_state(end_state)
        assert states_equal(test_end_state, end_state)
        print '%9d iters/s - %s %s' % (int(test_iters/dt), mod.__name__, getattr(mod, 'description', None) or '')
