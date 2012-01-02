from threading import Thread

class KThread(Thread):

    def __init__(self, *args, **kwargs):

        Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def run(self):

        while not self.killed:
            Thread.run(self)


class WorkerThread(KThread):
    """
        Thread executing tasks from a given tasks queue
    """

    def __init__(self, tasks, *args, **kwargs):

        KThread.__init__(self, *args, **kwargs)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        """
            Runs the thread functionality
        """

        while not self.killed:

            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception, e:
                print e
            self.tasks.task_done()
