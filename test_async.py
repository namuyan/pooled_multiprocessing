from pooled_multiprocessing import *
from testing import testing
from time import time


# Warning
# Don't write a object with "if __name__ == '__main__':"
# def testing(num):
#    r = 1
#    for i in range(1, num):
#        r += r * i
#    return r


def _callback(data_list):
    print("Get!", data_list)


def main():
    t = list()
    s = time()
    mp_map_async(testing, range(11), callback=_callback)
    t.append(time())
    mp_map_async(testing, range(11, 20), callback=_callback)
    t.append(time())
    mp_map_async(testing, range(20, 30), callback=_callback)
    t.append(time())
    event, result = mp_map_async(testing, range(30, 40))
    t.append(time())
    event.wait()
    print(result)
    t.append(time())
    for i, t in enumerate(t):
        print(i, round((t-s)*1000, 3), "mSec")
    mp_close()


if __name__ == '__main__':
    main()
