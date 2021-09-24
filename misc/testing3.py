from datetime import time
import queue


class testing:
    def __init__(self):
        self.count = 0
        self.phase1 = queue.Queue()
        self.phase2 = []
        self._running = True

    def terminate(self):
        self._running = False

    def main(self):
        pass

    def add_solutions(self):
        while self._running:
            self.phase1.put(self.count)
            self.count += 1

    def search_solutions(self):
        self.phase1.task_done()
        if self.phase1:
            self.phase2.append(self.phase1.get * -1)


import threading

t = testing()
thread = threading.Thread(target=t.add_solutions)
thing = threading.Thread(target=t.add_solutions)
thread.start()
thing.start()

for x in range(100):
    pass

print(t.phase1.qsize())

t.terminate()
