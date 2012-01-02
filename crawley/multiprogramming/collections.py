class WorkersList(list):
    """
        A list of workers
    """

    def start(self):

        for worker in self:
            worker.start()

    def waitall(self):

        for worker in self:
            worker.join()
