import time 

def timer(view):
    def dec(*args, **kwargs):
        start = time.time()
        value = view(*args, **kwargs)
        stop = time.time()
        print(f"view : {view.__name__} time : {stop-start}")
        return value
    return dec

