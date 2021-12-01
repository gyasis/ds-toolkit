# for loop send each element of the list to a thread for execution
def thread_pool_executor(function, list_of_args):  # function, list_of_args
    threads = []
    for arg in list_of_args:
        t = threading.Thread(target=function, args=(arg,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return