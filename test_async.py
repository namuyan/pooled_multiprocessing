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

outputs = 0
inputs = 0


def _callback(data_list):
    global outputs
    outputs += len(data_list)
    print("Get!", data_list)


def main():
    t = list()
    t.append(time())
    add_pool_process(cpu_num)
    s = time()
    global inputs
    for start, stop in ((0, 1), (1, 11), (11, 20), (20, 30), (30, 45), (45, 60), (60, 500)):
        event, *dummy = mp_map_async(testing, range(start, stop), callback=_callback)
        t.append(time())
        inputs += stop - start
    event.wait()
    print(event)
    t.append(time())
    for i, t in enumerate(t):
        print(i, round((t-s)*1000, 3), "mSec")
    mp_close()
    print("Status ok? =", inputs == outputs)


if __name__ == '__main__':
    main()
