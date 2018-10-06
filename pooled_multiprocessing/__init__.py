import multiprocessing as mp
from threading import Thread, Lock, Event
from time import time
from psutil import cpu_count
from more_itertools import chunked
import logging


cpu_num = cpu_count(False) or cpu_count(True)
processes = list()
lock = Lock()


def _process(index, input_que, output_que):
    while True:
        try:
            fnc, args_list, kwargs, t = input_que.get()
            # print("S", index, round((time() - t) * 1000, 3), "mSec")
            result = list()
            for args in args_list:
                if isinstance(args, tuple) or isinstance(args, list):
                    result.append(fnc(*args, **kwargs))
                else:
                    result.append(fnc(args, **kwargs))
            # print("E", index, round((time() - t) * 1000, 3), "mSec")
            output_que.put(result)
        except Exception as e:
            error = "Error on pool {}: {}".format(index, e)
            logging.error(error)
            output_que.put([error])


def _create():
    if mp.current_process().name != "MainProcess":
        return
    with lock:
        # create
        for index in range(1, cpu_num + 1):
            event = Event()
            event.set()
            input_que = mp.Queue()
            output_que = mp.Queue()
            p = mp.Process(target=_process, name="Pool{}".format(index), args=(index, input_que, output_que))
            p.daemon = True
            p.start()
            processes.append((p, input_que, output_que, event))
            print("Start pooled process {}".format(index))


def mp_map(fnc, data_list, **kwargs):
    assert len(processes) > 0, "It's not main process?"
    data_list = list(data_list)
    chunk = len(data_list) // cpu_num
    if len(data_list) % cpu_num != 0:
        chunk += 1
    result = list()
    work = list()
    task = 0
    # throw a tasks
    with lock:
        for (process, input_que, output_que, event), args_list in zip(processes, chunked(data_list, chunk)):
            if not process.is_alive():
                raise RuntimeError('Pool process is dead. (task throw)')
            event.wait()
            event.clear()
            input_que.put((fnc, args_list, kwargs, time()))
            work.append(process)
            task += 1
    # wait results
    for process, input_que, output_que, event in processes:
        if process not in work:
            continue
        if not process.is_alive():
            raise RuntimeError('Pool process is dead. (waiting)')
        if not event.is_set():
            result.extend(output_que.get())
            event.set()
            task -= 1
    if task != 0:
        raise RuntimeError('complete task is 0 but {}'.format(task))
    # return result
    return result


def mp_map_async(fnc, data_list, callback=None, **kwargs):
    def _return():
        r = mp_map(fnc, data_list, **kwargs)
        if callback:
            callback(r)
        result.extend(r)
        event.set()
    assert len(processes) > 0, "It's not main process?"
    Thread(target=_return, name="Pooled", daemon=True).start()
    event = Event()
    result = list()
    return event, result


def mp_close():
    for process, input_que, output_que, event in processes:
        process.terminate()
        input_que.close()
        output_que.close()
    processes.clear()


# pre-create
_create()


__all__ = [
    "mp_map", "mp_map_async", "mp_close"
]
