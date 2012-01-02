from Queue import Queue
from threads import WorkerThread, KThread

class ThreadPool(object):
    """
        Pool of threads consuming tasks from a queue
    """

    def __init__(self, num_threads):

        if num_threads < 1:
            raise ValueError("ThreadPool must have 1 thread or greenlet at least")

        elif num_threads == 1:
            self.__class__ = SingleThreadedPool
            return

        self.tasks = Queue(num_threads)

        for x in range(num_threads):
            WorkerThread(self.tasks)

    def spawn_n(self, func, *args, **kargs):
        """
            Add a task to the queue and asign a thread to do the work
        """

        self.tasks.put((func, args, kargs))

    def waitall(self):
        """
            Wait for completion of all the tasks in the queue
        """

        self.tasks.join()


class SingleThreadedPool(object):
    """
        One thread "pool" abstraction
    """

    def spawn_n(self, func, *args, **kargs):
        """
            Just executes the function in the same thread
        """

        func(*args, **kargs)

    def waitall(self):
        """
            SingleThreaded pool don't need to wait for anything
        """
        pass
