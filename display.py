from multiprocessing import Event, Pipe,Queue, Process
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


import numpy as np

def b_quit(events):
    events[1].set()
    print("quitter")
def b_event(events):
    print("event")
    events[0].set()

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

def servertest(events):
        events[1].wait()
        print("ca fonctionne")

def display(queue,events):
    '''
    '''
    run = True
    reftime = time.perf_counter()

    log = [[0,0,0]]
    
    #on lance l'animation
    plt.ion()

    fig, ax = plt.subplots()
    #on initialise les courbes
    line_grass, = ax.plot([0], [0], label="Grass")
    line_prey,  = ax.plot([0], [0], label="Prey")
    line_pred,  = ax.plot([0], [0], label="Pred")
    fig.legend()

    cgrass = [0]
    cprey = [0]
    cpred = [0]

    #on gère les boutons
    axevent = fig.add_axes([0.7, 0.05, 0.1, 0.075])
    axquit = fig.add_axes([0.81,0.05,0.1, 0.075])
    bevent = Button(axevent, 'Event')
    bevent.on_clicked(lambda _: events[1].set())
    bquit = Button(axquit, 'Quit')
    bquit.on_clicked(lambda _: events[0].set())

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
                cgrass.append(cgrass[-1])
                cprey.append(cprey[-1])
                cpred.append(cpred[-1])

            match data[0]:
                case "grass":
                    log[-1][0]=data[1]
                case "prey":
                    log[-1][1]=data[1]
                case "pred":
                    log[-1][2]=data[1]
    

        #on crée les courbes en récupérant les données
        cgrass[-1] = log[-1][0]
        cprey[-1] = log[-1][1]
        cpred[-1] = log[-1][2]

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
    queue = Queue(10)
    event = Event()
    quit = Event()
    events = [event,quit]
    worker = Process(target = workertest, args = (queue,))
    read = Process(target=display,args=(queue,events))
    serv = Process(target=servertest, args = (events,))
    worker.start()
    read.start()
    serv.start()
    worker.join()
    read.join()
    serv.join()