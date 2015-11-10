import threading, functools

def run_in_other_thread(function):
    """
    run a function on a new tread, in the background
    :param function: the fucntion that will adapted to run on new tread
    :return: the function that will run the backgroun when called
    """
    @functools.wraps(function)
    def fn_(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs)
        thread.start()
        thread.join()
    return fn_