import time
import json


def f1():
    with open('lb_en.json') as f:
        data = json.loads(f.read())

    for d in data:
        pass


if __name__ == '__main__':
    start = time.perf_counter()
    f1()
    end = time.perf_counter()
    print(end - start)
