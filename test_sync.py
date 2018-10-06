from pooled_multiprocessing import *
from time import time


def testing(num):
    r = 1
    for i in range(1, num):
        r += r * i
    return r


def main():
    t = list()
    t.append(time())
    s = time()
    result = mp_map(fnc=testing, data_list=list(range(10)))
    t.append(time())
    print("Get!", result)
    result = mp_map(fnc=testing, data_list=list(range(10, 20)))
    t.append(time())
    print("Get!", result)
    result = mp_map(fnc=testing, data_list=list(range(20, 30)))
    t.append(time())
    print("Get!", result)
    for i, t in enumerate(t):
        print(i, round((t-s)*1000, 3), "mSec")
    mp_close()


if __name__ == '__main__':
    main()
