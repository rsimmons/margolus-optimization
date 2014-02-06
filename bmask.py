import sys

x = 0
for arg in sys.argv[1:]:
    x |= 1 << int(arg)

print hex(x)
