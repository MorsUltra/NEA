import queue
import threading


class solver():

    def __init__(self, cube, multithreading=False):
        self._running = True
        self.phase1 = phase1
        self.phase21 = phase2
        self.cc = cube
        self.solution = [] if multithreading else None
        self.multithreading = multithreading
        self.solution_count = 0

    def solve(self):
        if self.multithreading:
            self.multi()

        self.solution = self.phase2(self.phase1(self.cc))
        return self.solution

    def multi(self):
        # start phase 1 which starts appending things to it's queue
        self.phase1_thread = threading.Thread(target=self.phase1, args=self.cc)
        # start phase 2 workers which will work through the solutions in phase 1 as they occur
        self.phase2_workers = threading.Thread(target=self.phase2_worker, args=self.cc)
        # checker to terminate process if all phase 1 solutions have been found
        checker = threading.Thread(target=self.checker)

    def phase2_worker(self, cc):
        # phase1.solutions holds current solutions to phase 1
        while self._running:
            phase1 = self.phase1.solutions.get() # get solution to phase 1
            if phase1:
                self.solution_count += 1
                self.phase1.solutions.task_done()
                cc = self.do_moves(phase1)
                self.soluion.append(self.phase2(cc))



    def do_moves(self, moves):
        pass

    def checker(self):
        while True:
            if not self.phase1_thread.isAlive() and self.solution_count == len(self.solutions):
                self.terminate()




    def terminate(self):
        self._running = False # shuts down workers
        self.phase1.terminate() # stops IDA* search
        self.phase2.terminate() # stops IDA* search


# Start phase one thread, appending solutions to the queue
# Start phase two threads, checking the queue for inputs