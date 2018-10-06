def testing(num):
    r = 1
    for i in range(1, num):
        r += r * i
    return r
