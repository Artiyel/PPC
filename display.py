import multiprocessing
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


import numpy as np

class Index():
    def event(self,action):
        ''''''
        self.pipe.send("event")
    def quit(self, action):
        ''''''
        self.pipe.send("quit")

def workertest(queue):
    while True:
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

def servertest(pipe):
    while True:
        print(pipe.recv())

def display(queue,pipe):
    '''
    '''
    run = True
    reftime = time.perf_counter()

    log = [[0,0,0]]
    
    #on lance l'animation
    plt.ion()

    fig, ax = plt.subplots()
    #on initialise les courbes
    line_grass, = ax.plot([], [], label="Grass")
    line_prey,  = ax.plot([], [], label="Prey")
    line_pred,  = ax.plot([], [], label="Pred")
    fig.legend()

    #on gère les boutons
    callback = Index()
    callback.pipe=pipe
    axevent = fig.add_axes([0.7, 0.05, 0.1, 0.075])
    axquit = fig.add_axes([0.81,0.05,0.1, 0.075])
    bevent = Button(axevent, 'Event')
    bevent.on_clicked(callback.event)
    bquit = Button(axquit, 'Quit')
    bquit.on_clicked(callback.quit)

    while run:
        try :
            data = queue.get(timeout = 0.1) #on récupère les données (avec un timeout pour ne pas etre bloqué)
        except :
           data = (None,None)

        if data[0]=="exit": #condition de sortie de boucle
            run = False

        else :
            #on ajoute les données des secondes où il n'y a pas eu de changement
            while time.perf_counter()-reftime > len(log):
                log.append(list(log[-1]))

            match data[0]:
                case "grass":
                    log[-1][0]=data[1]
                case "prey":
                    log[-1][1]=data[1]
                case "pred":
                    log[-1][2]=data[1]
    

        #on crée les courbes en récupérant les données
        cgrass = [elem[0] for elem in log]
        cprey = [elem[1] for elem in log]
        cpred = [elem[2] for elem in log]

        t=np.arange(0,len(log),1) #axe des x
        #on assigne les données à leurs courbes respectives
        line_grass.set_data(t, cgrass)
        line_prey.set_data(t, cprey)
        line_pred.set_data(t, cpred)
        #on remet à jour les axes
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
    read = multiprocessing.Process(target=display,args=(queue,pipe[1]))
    serv = multiprocessing.Process(target=servertest, args = (pipe[0],))
    worker.start()
    read.start()
    serv.start()
    worker.join()
    read.join()
    serv.join()