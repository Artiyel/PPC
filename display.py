import multiprocessing
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


import numpy as np

class Index():
    def event(self,action, pipe):
        ''''''
def workertest(queue):
    queue.put(("pred",5))
    time.sleep(3)
    queue.put(("prey",3))
    time.sleep(1)
    queue.put(("pred",7))
    queue.put(("pred",4))
    time.sleep(1)
    queue.put(("prey",6))
    time.sleep(1)
    queue.put(("pred",12))
    queue.put(("pred",1))
    time.sleep(1)
    queue.put(("prey",2))
    time.sleep(1)
    queue.put(("pred",3))
    queue.put(("exit",))

def display(queue,pipe):
    ''''''
    run = True
    reftime = time.perf_counter()
    log = [[0,0,0]]
    plt.ion()
    fig, ax = plt.subplots()
    
    line_grass, = ax.plot([], [], label="Grass")
    line_prey,  = ax.plot([], [], label="Prey")
    line_pred,  = ax.plot([], [], label="Pred")

    while run:
        try :
            data = queue.get(timeout = 0.1)
        except :
            continue

        if data[0]=="exit":
            run = False
        else :

            while time.perf_counter()-reftime > len(log):
                log.append(list(log[-1]))
        
            if data[0] == "grass":
                log[-1][0]=data[1]
            elif data[0]=="prey":
                log[-1][1]=data[1]
            elif data[0]=="pred":
                log[-1][2]=data[1]
        print(log)
    
        #on crée les courbes

        cgrass = [elem[0] for elem in log]
        cprey = [elem[1] for elem in log]
        cpred = [elem[2] for elem in log]

        t=np.arange(0,len(log),1)
        line_grass.set_data(t, cgrass)
        line_prey.set_data(t, cprey)
        line_pred.set_data(t, cpred)
        ax.relim()
        ax.autoscale_view()
        plt.pause(0.01)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()
    plt.ioff()
    '''action = Index(pipe)
    event = Button("event","Event")
    event.on_clicked(pipe.send)'''


if __name__ == '__main__':
    queue = multiprocessing.Queue(10)
    pipe = multiprocessing.Pipe()
    worker = multiprocessing.Process(target = workertest, args = (queue,))
    read = multiprocessing.Process(target=display,args=(queue,pipe))
    worker.start()
    read.start()
    worker.join()
    read.join()