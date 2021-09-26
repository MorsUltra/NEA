import queue

def remove_task(t):
    t.get()




q = queue.Queue()

for x in range(10):
    q.put(x)

remove_task(q)
print(q.unfinished_tasks)

