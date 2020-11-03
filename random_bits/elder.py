# m=8, n=8, l=1, t=100

def print_field(m, n, l, t):
    for i in range(0, n):
        tl = [max((i ^ j) - l, 0) % t for j in range(0, m)]
        print(sum(tl), sum(tl) % t, tl)


# print_field(8, 8, 1, 100)

print_field(13, 100, 1, 100)
