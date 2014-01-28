def encode_rule(table):
    result = 0
    assert len(table) == 16
    for i, v in enumerate(table):
        assert (v >= 0) and (v < 16)
        result |= v << (4*i)
    return result

