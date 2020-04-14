import time

def f1():
    while True:
        print("\033[31myield前:我是f1\033[0m")
        yield
        print("\033[31myield后:我是f1\033[0m")
        time.sleep(2)


def f2():
    while True:
        print("yield前:我是f2")
        yield
        print("yield后:我是f2")
        time.sleep(2)


if __name__ == '__main__':
    t1 = f1()
    t2 = f2()
    for i in range(5):
        next(t1)
        print("我是main")
        next(t2)
