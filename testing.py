from time import sleep


def testing(num):
    r = 1
    for i in range(num, num+10):
        r += r * i
        # sleep(0.1)
    return r
