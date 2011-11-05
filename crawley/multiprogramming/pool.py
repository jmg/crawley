from Queue import Queue
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
    
    def __init__(self, tasks):
        
        Thread.__init__(self)
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
        
        while self.tasks:
            try:            
                self.tasks = [self.tasks.join(0.1) for t in self.tasks if t is not None and t.isAlive()]
            except KeyboardInterrupt:
                for t in self.tasks:
                    t.killed = True


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
