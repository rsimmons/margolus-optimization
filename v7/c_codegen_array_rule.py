def fourbits_move(var, src_start_bitnum, dst_start_bitnum):
    mask = (1 << src_start_bitnum) | (1 << (src_start_bitnum+1)) | (1 << (src_start_bitnum+2)) | (1 << (src_start_bitnum+3))
    masked_expr = '(%s & %dULL)' % (var, mask)
    shift = dst_start_bitnum - src_start_bitnum
    if shift == 0:
        return masked_expr
    elif shift > 0:
        return '(%s << %d)' % (masked_expr, shift)
    else:
        return '(%s >> %d)' % (masked_expr, -shift)

def rule_lookup_expr(rule_var, qindex_var):
    # return '((%s & (15ULL << %s)) >> %s)' % (rule_var, qindex_var, qindex_var)
    return '(%s[%s])' % (rule_var, qindex_var)

def evolve_four_bits_contig(tmpind, bitnum, src_var, dst_var):
    s = ''
    s += '    UInt64 qind%d = %s;\n' % (tmpind, fourbits_move(src_var, bitnum, 0))
    s += '    UInt64 res%d = %s;\n' % (tmpind, rule_lookup_expr('rule', 'qind%d' % tmpind))
    s += '    %s |= %s;\n' % (dst_var, fourbits_move('res%d' % tmpind, 0, bitnum))
    return s

def evolve_64_even_func():
    s = 'void evolve_64_even(UInt64 *rule, UInt64 src, UInt64 *dst) {\n'
    s += '    UInt64 result = 0;\n'
    count = 0
    for dx in (0, 16, 32, 48):
        for dy in (0, 4, 8, 12):
            s += evolve_four_bits_contig(count, dx+dy, 'src', 'result')
            count += 1
    s += '    *dst = result;\n'
    s += '}\n'
    return s

if __name__ == '__main__':
    print evolve_64_even_func()
