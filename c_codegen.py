def onebit_move(var, src_bitnum, dst_bitnum):
    mask = 1 << src_bitnum
    masked_expr = '(%s & %dULL)' % (var, mask)
    shift = dst_bitnum - src_bitnum
    if shift == 0:
        return masked_expr
    elif shift > 0:
        return '(%s << %d)' % (masked_expr, shift)
    else:
        return '(%s >> %d)' % (masked_expr, -shift)

def twobits_move(var, src_start_bitnum, dst_start_bitnum):
    mask = (1 << src_start_bitnum) | (1 << (src_start_bitnum+1))
    masked_expr = '(%s & %dULL)' % (var, mask)
    shift = dst_start_bitnum - src_start_bitnum
    if shift == 0:
        return masked_expr
    elif shift > 0:
        return '(%s << %d)' % (masked_expr, shift)
    else:
        return '(%s >> %d)' % (masked_expr, -shift)

def rule_lookup_expr(rule_var, qindex_var):
    return '((%s & (15ULL << %s)) >> %s)' % (rule_var, qindex_var, qindex_var)

def evolve_four_bits_paired(tmpind, low_bitnum, src_low_var, dst_low_var, high_bitnum, src_high_var, dst_high_var):
    s = ''
    s += '    UInt64 qind%d = %s | %s;\n' % (tmpind, twobits_move(src_low_var, low_bitnum, 2), twobits_move(src_low_var, high_bitnum, 4))
    s += '    UInt64 res%d = %s;\n' % (tmpind, rule_lookup_expr('rule', 'qind%d' % tmpind))
    s += '    %s |= %s;\n' % (dst_low_var, twobits_move('res%d' % tmpind, 0, low_bitnum))
    s += '    %s |= %s;\n' % (dst_high_var, twobits_move('res%d' % tmpind, 2, high_bitnum))
    return s

def evolve_four_bits_indiv(tmpind, bitnum_0, src_var_0, dst_var_0, bitnum_1, src_var_1, dst_var_1, bitnum_2, src_var_2, dst_var_2, bitnum_3, src_var_3, dst_var_3):
    s = ''
    s += '    UInt64 qind%d = %s | %s | %s | %s;\n' % (tmpind, onebit_move(src_var_0, bitnum_0, 2), onebit_move(src_var_1, bitnum_1, 3), onebit_move(src_var_2, bitnum_2, 4), onebit_move(src_var_3, bitnum_3, 5))
    s += '    UInt64 res%d = %s;\n' % (tmpind, rule_lookup_expr('rule', 'qind%d' % tmpind))
    s += '    %s |= %s;\n' % (dst_var_0, onebit_move('res%d' % tmpind, 0, bitnum_0))
    s += '    %s |= %s;\n' % (dst_var_1, onebit_move('res%d' % tmpind, 1, bitnum_1))
    s += '    %s |= %s;\n' % (dst_var_2, onebit_move('res%d' % tmpind, 2, bitnum_2))
    s += '    %s |= %s;\n' % (dst_var_3, onebit_move('res%d' % tmpind, 3, bitnum_3))
    return s

def evolve_64_even_func():
    s = 'void evolve_64_even(UInt64 rule, UInt64 src, UInt64 *dst) {\n'
    s += '    UInt64 result = 0;\n'
    count = 0
    for dy in (0, 16, 32, 48):
        for dx in (0, 2, 4, 6):
            s += evolve_four_bits_paired(count, dx+dy, 'src', 'result', dx+dy+8, 'src', 'result')
            count += 1
    s += '    *dst = result;\n'
    s += '}\n'
    return s

def evolve_64_odd_func():
    s = 'void evolve_64_odd(UInt64 rule, UInt64 src_c, UInt64 src_n, UInt64 src_nw, UInt64 src_w, UInt64 *dst_c, UInt64 *dst_n, UInt64 *dst_nw, UInt64 *dst_w) {\n'
    s += '    UInt64 result_c = 0, result_n = 0, result_nw = 0, result_w = 0;\n'
    count = 0

    # nw corner
    s += evolve_four_bits_indiv(count, 63, 'src_nw', 'result_nw', 56, 'src_n', 'result_n', 7, 'src_w', 'result_w', 0, 'src_c', 'result_c')
    count += 1

    # n edge
    for dx in (0, 2, 4):
        s += evolve_four_bits_paired(count, 57+dx, 'src_n', 'result_n', 1+dx, 'src_c', 'result_c')
        count += 1

    # w edge
    for dy in (0, 16, 32):
        s += evolve_four_bits_indiv(count, 15+dy, 'src_w', 'result_w', 8+dy, 'src_c', 'result_c', 23+dy, 'src_w', 'result_w', 16+dy, 'src_c', 'result_c')
        count += 1

    for dy in (9, 25, 41):
        for dx in (0, 2, 4):
            s += evolve_four_bits_paired(count, dx+dy, 'src_c', 'result_c', dx+dy+8, 'src_c', 'result_c')
            count += 1
    s += '    *dst_c |= result_c;\n'
    s += '    *dst_n |= result_n;\n'
    s += '    *dst_nw |= result_nw;\n'
    s += '    *dst_w |= result_w;\n'
    s += '}\n'
    return s

if __name__ == '__main__':
    print evolve_64_even_func()
    print evolve_64_odd_func()
