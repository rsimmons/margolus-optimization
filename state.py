import re
import urlparse

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
