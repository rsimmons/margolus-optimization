def onebit_move(var, src_bitnum, dst_bitnum):
    mask = 1 << src_bitnum
    masked_expr = '(%s & %d)' % (var, mask)
    shift = dst_bitnum - src_bitnum
    if shift == 0:
        return masked_expr
    elif shift > 0:
        return '(%s << %d)' % (masked_expr, shift)
    else:
        return '(%s >> %d)' % (masked_expr, -shift)

def twobits_move(var, src_start_bitnum, dst_start_bitnum):
    mask = (1 << src_start_bitnum) | (1 << (src_start_bitnum+1))
    masked_expr = '(%s & %d)' % (var, mask)
    shift = dst_start_bitnum - src_start_bitnum
    if shift == 0:
        return masked_expr
    elif shift > 0:
        return '(%s << %d)' % (masked_expr, shift)
    else:
        return '(%s >> %d)' % (masked_expr, -shift)

def rule_lookup_expr(rule_var, qindex_var):
    return '((%s & (15 << %s)) >> %s)' % (rule_var, qindex_var, qindex_var)

def py_evolve_four_bits_paired(tmpind, low_bitnum, src_low_var, dst_low_var, high_bitnum, src_high_var, dst_high_var):
    s = ''
    s += '    qind%d = %s | %s\n' % (tmpind, twobits_move(src_low_var, low_bitnum, 2), twobits_move(src_high_var, high_bitnum, 4))
    s += '    res%d = %s\n' % (tmpind, rule_lookup_expr('rule', 'qind%d' % tmpind))
    s += '    %s |= %s\n' % (dst_low_var, twobits_move('res%d' % tmpind, 0, low_bitnum))
    s += '    %s |= %s\n' % (dst_high_var, twobits_move('res%d' % tmpind, 2, high_bitnum))
    return s

def py_evolve_four_bits_indiv(tmpind, bitnum_0, src_var_0, dst_var_0, bitnum_1, src_var_1, dst_var_1, bitnum_2, src_var_2, dst_var_2, bitnum_3, src_var_3, dst_var_3):
    s = ''
    s += '    qind%d = %s | %s | %s | %s\n' % (tmpind, onebit_move(src_var_0, bitnum_0, 2), onebit_move(src_var_1, bitnum_1, 3), onebit_move(src_var_2, bitnum_2, 4), onebit_move(src_var_3, bitnum_3, 5))
    s += '    res%d = %s\n' % (tmpind, rule_lookup_expr('rule', 'qind%d' % tmpind))
    s += '    %s |= %s\n' % (dst_var_0, onebit_move('res%d' % tmpind, 0, bitnum_0))
    s += '    %s |= %s\n' % (dst_var_1, onebit_move('res%d' % tmpind, 1, bitnum_1))
    s += '    %s |= %s\n' % (dst_var_2, onebit_move('res%d' % tmpind, 2, bitnum_2))
    s += '    %s |= %s\n' % (dst_var_3, onebit_move('res%d' % tmpind, 3, bitnum_3))
    return s

def py_evolve_64_even_func():
    s = 'def evolve_64_even(rule, src):\n'
    s += '    dst = 0\n'
    count = 0
    for dy in (0, 16, 32, 48):
        for dx in (0, 2, 4, 6):
            s += py_evolve_four_bits_paired(count, dx+dy, 'src', 'dst', dx+dy+8, 'src', 'dst')
            count += 1
    s += '    return dst\n'
    return s

def py_evolve_64_odd_func():
    s = 'def evolve_64_odd(rule, src_c, src_n, src_nw, src_w):\n'
    s += '    dst_c = dst_n = dst_nw = dst_w = 0\n'
    count = 0

    # nw corner
    s += py_evolve_four_bits_indiv(count, 63, 'src_nw', 'dst_nw', 56, 'src_n', 'dst_n', 7, 'src_w', 'dst_w', 0, 'src_c', 'dst_c')
    count += 1

    # n edge
    for dx in (0, 2, 4):
        s += py_evolve_four_bits_paired(count, 57+dx, 'src_n', 'dst_n', 1+dx, 'src_c', 'dst_c')
        count += 1

    # w edge
    for dy in (0, 16, 32):
        s += py_evolve_four_bits_indiv(count, 15+dy, 'src_w', 'dst_w', 8+dy, 'src_c', 'dst_c', 23+dy, 'src_w', 'dst_w', 16+dy, 'src_c', 'dst_c')
        count += 1

    for dy in (9, 25, 41):
        for dx in (0, 2, 4):
            s += py_evolve_four_bits_paired(count, dx+dy, 'src_c', 'dst_c', dx+dy+8, 'src_c', 'dst_c')
            count += 1
    s += '    return (dst_c, dst_n, dst_nw, dst_w)\n'
    return s

if __name__ == '__main__':
    print py_evolve_64_even_func()
    print py_evolve_64_odd_func()
