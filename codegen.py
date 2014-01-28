def twobits_move(var, src_low_bitnum, dst_low_bitnum):
    mask = (1 << src_low_bitnum) | (1 << (src_low_bitnum+1))
    masked_expr = '(%s & %d)' % (var, mask)
    shift = dst_low_bitnum - src_low_bitnum
    if shift == 0:
        return masked_expr
    elif shift > 0:
        return '(%s << %d)' % (masked_expr, shift)
    else:
        return '(%s >> %d)' % (masked_expr, -shift)

def rule_lookup_expr(rule_var, qindex_var):
    return '((%s & (15 << %s)) >> %s)' % (rule_var, qindex_var, qindex_var)

def py_evolve_64_even_func():
    s = 'def evolve_64_even(rule, src):\n'
    s += '    dst = 0\n'
    count = 0
    for dy in (0, 16, 32, 48):
        for dx in (0, 2, 4, 6):
            s += '    qind%d = %s | %s\n' % (count, twobits_move('src', dx+dy, 2), twobits_move('src', dx+dy+8, 4))
            s += '    res%d = %s\n' % (count, rule_lookup_expr('rule', 'qind%d' % count))
            s += '    dst |= %s\n' % twobits_move('res%d' % count, 0, dx+dy)
            s += '    dst |= %s\n' % twobits_move('res%d' % count, 2, dx+dy+8)
            count += 1
    s += '    return dst\n'
    return s

if __name__ == '__main__':
    print py_evolve_64_even_func()
