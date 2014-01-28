def evolve_64_even(rule, src):
    dst = 0
    qind0 = ((src & 3) << 2) | ((src & 768) >> 4)
    res0 = ((rule & (15 << qind0)) >> qind0)
    dst |= (res0 & 3)
    dst |= ((res0 & 12) << 6)
    qind1 = (src & 12) | ((src & 3072) >> 6)
    res1 = ((rule & (15 << qind1)) >> qind1)
    dst |= ((res1 & 3) << 2)
    dst |= ((res1 & 12) << 8)
    qind2 = ((src & 48) >> 2) | ((src & 12288) >> 8)
    res2 = ((rule & (15 << qind2)) >> qind2)
    dst |= ((res2 & 3) << 4)
    dst |= ((res2 & 12) << 10)
    qind3 = ((src & 192) >> 4) | ((src & 49152) >> 10)
    res3 = ((rule & (15 << qind3)) >> qind3)
    dst |= ((res3 & 3) << 6)
    dst |= ((res3 & 12) << 12)
    qind4 = ((src & 196608) >> 14) | ((src & 50331648) >> 20)
    res4 = ((rule & (15 << qind4)) >> qind4)
    dst |= ((res4 & 3) << 16)
    dst |= ((res4 & 12) << 22)
    qind5 = ((src & 786432) >> 16) | ((src & 201326592) >> 22)
    res5 = ((rule & (15 << qind5)) >> qind5)
    dst |= ((res5 & 3) << 18)
    dst |= ((res5 & 12) << 24)
    qind6 = ((src & 3145728) >> 18) | ((src & 805306368) >> 24)
    res6 = ((rule & (15 << qind6)) >> qind6)
    dst |= ((res6 & 3) << 20)
    dst |= ((res6 & 12) << 26)
    qind7 = ((src & 12582912) >> 20) | ((src & 3221225472) >> 26)
    res7 = ((rule & (15 << qind7)) >> qind7)
    dst |= ((res7 & 3) << 22)
    dst |= ((res7 & 12) << 28)
    qind8 = ((src & 12884901888) >> 30) | ((src & 3298534883328) >> 36)
    res8 = ((rule & (15 << qind8)) >> qind8)
    dst |= ((res8 & 3) << 32)
    dst |= ((res8 & 12) << 38)
    qind9 = ((src & 51539607552) >> 32) | ((src & 13194139533312) >> 38)
    res9 = ((rule & (15 << qind9)) >> qind9)
    dst |= ((res9 & 3) << 34)
    dst |= ((res9 & 12) << 40)
    qind10 = ((src & 206158430208) >> 34) | ((src & 52776558133248) >> 40)
    res10 = ((rule & (15 << qind10)) >> qind10)
    dst |= ((res10 & 3) << 36)
    dst |= ((res10 & 12) << 42)
    qind11 = ((src & 824633720832) >> 36) | ((src & 211106232532992) >> 42)
    res11 = ((rule & (15 << qind11)) >> qind11)
    dst |= ((res11 & 3) << 38)
    dst |= ((res11 & 12) << 44)
    qind12 = ((src & 844424930131968) >> 46) | ((src & 216172782113783808) >> 52)
    res12 = ((rule & (15 << qind12)) >> qind12)
    dst |= ((res12 & 3) << 48)
    dst |= ((res12 & 12) << 54)
    qind13 = ((src & 3377699720527872) >> 48) | ((src & 864691128455135232) >> 54)
    res13 = ((rule & (15 << qind13)) >> qind13)
    dst |= ((res13 & 3) << 50)
    dst |= ((res13 & 12) << 56)
    qind14 = ((src & 13510798882111488) >> 50) | ((src & 3458764513820540928) >> 56)
    res14 = ((rule & (15 << qind14)) >> qind14)
    dst |= ((res14 & 3) << 52)
    dst |= ((res14 & 12) << 58)
    qind15 = ((src & 54043195528445952) >> 52) | ((src & 13835058055282163712) >> 58)
    res15 = ((rule & (15 << qind15)) >> qind15)
    dst |= ((res15 & 3) << 54)
    dst |= ((res15 & 12) << 60)
    return dst

