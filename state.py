import re
import urlparse
import urllib

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

class RLEHelper(object):
    def __init__(self):
        self.last_tag = None
        self.last_count = 0
        self.result_parts = []

    def emit(self):
        if self.last_count > 1:
            self.result_parts.append('%d%s' % (self.last_count, self.last_tag))
        elif self.last_count == 1:
            self.result_parts.append(self.last_tag)
        else:
            assert False
        self.last_tag = None
        self.last_count = 0

    def add_tag(self, tag):
        if self.last_tag is not None and tag != self.last_tag:
            self.emit()

        self.last_tag = tag
        self.last_count += 1

    def get_result(self):
        if self.last_tag is not None:
            self.emit()

        return ''.join(self.result_parts)

def format_dmishin_url(state, rule=None):
    params = {}
    params['size'] = '%dx%d' % (state['width'], state['height'])
    params['phase'] = str(state['phase'])

    if any(state['cells']):
        y_count = {} # hacky but works
        rle_y0 = None
        last_y = None
        for y in range(state['height']):
            y_count[y] = 0
            for x in range(state['width']):
                idx = y*state['width'] + x
                if state['cells'][idx]:
                    if rle_y0 is None:
                        rle_y0 = y
                    y_count[y] += 1
            if y_count[y] > 0:
                last_y = y

        rle_x0 = None
        for x in range(state['width']):
            for y in range(state['height']):
                idx = y*state['width'] + x
                if state['cells'][idx] and rle_x0 is None:
                    rle_x0 = x

        params['rle_x0'] = str(rle_x0)
        params['rle_y0'] = str(rle_y0)

        helper = RLEHelper()

        for y in range(rle_y0, last_y+1):
            seen_count = 0
            idx = y*state['width'] + rle_x0
            while seen_count < y_count[y]:
                if state['cells'][idx]:
                    helper.add_tag('o')
                    seen_count += 1
                else:
                    helper.add_tag('b')
                idx += 1
            helper.add_tag('$')

        params['rle'] = helper.get_result()

    params['step'] = '1'
    params['frame_delay'] = '1'
    params['cell_size'] = '1,1'

    if rule is not None:
        params['rule'] = ','.join(str(x) for x in rule)

    return 'http://dmishin.github.io/js-revca/index.html?' + urllib.urlencode(params)

if __name__ == '__main__':
    test_url = 'http://dmishin.github.io/js-revca/index.html?rule=0,8,4,3,2,5,9,7,1,6,10,11,12,13,14,15&rle_x0=24&rle_y0=20&rle=bo4b3obobo$2b6o3b2o$8ob3o$4bobo5bo$3bob3o$bo2bobo4bo3$4b2ob2obobo$3ob2o2bo3bo$bob2obo3b3o$2o3bo2bobobo$b2o2b2ob2o2bo$3o2bob2obobo$bob3obobo2bo&step=1&frame_delay=10&size=128x64&cell_size=8,1&phase=0'

    before_args = urlparse.parse_qs(urlparse.urlparse(test_url).query)
    state = parse_dmishin_url(test_url)
    after_url = format_dmishin_url(state)
    after_args = urlparse.parse_qs(urlparse.urlparse(test_url).query)
    assert before_args['rle_x0'] == after_args['rle_x0']
    assert before_args['rle_y0'] == after_args['rle_y0']
    assert before_args['rle'] == after_args['rle']
