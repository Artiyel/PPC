from multiprocessing import Lock,Process,Array,Value,Queue,Event
import select,random,socket
import grass,predateur,proie,display
from pickle import loads
from concurrent.futures import ThreadPoolExecutor
import signal,os


def server_request_update(client_socket,serve):
    client_socket.setblocking(True)

    try:
        while True:
            with serve.get_lock(): #on stoppe de serve si c'est la fin
                if serve.value==0:
                    break

            data=client_socket.recv(1024)
            if not data: #si tu reçoit des données vides fin de connection
                break
            liste = loads(data) #format de liste : ["type","espece qui envoie l'info","pid"] type=eats,died,reproduce

            if liste[0] == 'died':
                with lock_pops:
                    with pid_log_lock:
                        delete_from_records(liste)

            elif liste[0] == "reproduce":
                reproduce_like_a_chad(liste,client_socket)

            else:
                try_to_kill(liste,client_socket)
            
    except OSError as e:
        if e.winerror in (10054,10053):
            pass #ignorer les erreur de connections fermées
        else:
            print("Client error:", e)

    client_socket.close()

def delete_from_records(liste):
            #delete du log des programmes vivants
    for i, pid in enumerate(pid_log[liste[1]]):
        if pid == liste[2]:
            del pid_log[liste[1]][i]
            break 

    #delete du compteur de vivant de son espèce
    match liste[1]:
        case "pred":
            populations[0]-=1
            send_data_to_display('pred')
        case "proie":
            populations[1]-=1
            send_data_to_display('proie')

def try_to_kill(liste,client_socket):
    succes='no'
    with lock_pops:
        match liste[1]:
            case "pred": # si c'est un predateur, on tue une proie au hasard
                if populations[1]>0:
                    succes='yes_ate'
                    with pid_log_lock: 
                        on_tue_ki_index=random.randint(0,len(pid_log["proie"])-1)
                        a=pid_log["proie"][on_tue_ki_index]
                        send_signal_kill(a)
                        delete_from_records(["died","proie",a])
                    send_data_to_display('proie')


            case "proie": #si c'est une proie qui mange elle enlève juste de l'herbe
                if populations[2]> 0:
                    populations[2]-=1
                    send_data_to_display('grass')
                    succes="yes_ate"
    if succes =="yes_ate":
        print(f"{liste[1]} ({liste[2]}) a mangé")
    client_socket.send(succes.encode())

def reproduce_like_a_chad(liste,client_socket):
    success="no_reproduce"
    match liste[1]:
        case "pred":
            with populations.get_lock():
                if populations[0]>1:
                    populations[0]+=1
                    p=Process(target=predateur.predateur, args=())
                    p.start()
                    success="yes"
                    with pid_log_lock:
                        pid_log["pred"].append(p.pid)
                send_data_to_display("pred")
        case "proie":
            with populations.get_lock():
                if populations[1]>1:
                    populations[1]+=1
                    p=Process(target=proie.proie, args=())
                    p.start()
                    success="yes"
                    with pid_log_lock:
                        pid_log["proie"].append(p.pid)
                send_data_to_display("proie")
    if success=="yes":
        print(f"{liste[1]} s'est reproduit")
    client_socket.send(success.encode())

def send_data_to_display(species):
    match species:
        case "grass":
            queue.put(("grass",populations[2]))
        case "proie":
            queue.put(("prey",populations[1]))
        case "pred":
            queue.put(("pred",populations[0]))
        case "all":
            queue.put(("pred",populations[0]))
            queue.put(("prey",populations[1]))
            queue.put(("grass",populations[2]))

def send_signal_kill(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"{pid} est mort")
    except (ProcessLookupError, PermissionError):
        pass

def init_population():
    for j in range(populations[0]):
        p=Process(target=predateur.predateur, args=())
        p.start()
        with pid_log_lock:
            pid_log["pred"].append((p.pid))
    print(f"Les {populations[0]} predateurs sont apparus")

    for j in range(populations[1]):
        p=Process(target=proie.proie, args=())
        p.start()
        with pid_log_lock:
            pid_log["proie"].append((p.pid))
    print(f"Les {populations[1]} proies sont apparues")

    herbe = Process(target=grass.herbe_growth,args=(grass_secheresse,populations,lock_pops))
    herbe.start()
    print(f"L'herbe est initialisée a {populations[2]} brins")
    return herbe.pid

def kill_all_alive(log,lock):
    print("on tue tout les vivants de l'environnement")
    with lock:
        for species in log.keys():
            for pid in log[species]:
                send_signal_kill(pid)
    
def stop_simulation():
    print("on stoppe tout!")
    global sim_running
    sim_running=False
    global serve
    with serve.get_lock():
        serve=0
    queue.put(("exit",))

def handler_signal(signum, frame):
    if signum == signal.SIGINT:
        stop_simulation()
    elif signum == signal.SIGUSR1:
        secher_hess()
    
def secher_hess():
    '''global grass_secheresse
    with grass_secheresse.get_lock():
        grass_secheresse.value = 1'''
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHH")


if __name__ == '__main__':

    #init du signal handler qui fini la simulation en cas de ctrl+c
    signal.signal(signal.SIGINT,handler_signal)
    #init du signal qui déclenchge la secheresse
    signal.signal(signal.SIGUSR1,handler_signal)

    #init des morceaux de mémoire qui sont accessible par tout les process,
    #donc protégés par des lock

    populations = Array('i', [10,10,10]) # nb de [pred,proie,herbe]
    lock_pops= populations.get_lock()

    global grass_secheresse
    grass_secheresse= Value('i',0) # 0 pour non, 1 pour oui
    global serve
    serve = Value('i',1) # 0 pour non, 1 pour oui


    pid_log={
        "pred":[],
        "proie":[],#liste de PIDs
    }
    pid_log_lock=Lock()

    # lancer tout les processssss qui sont client (lancés avec délais
    # pour permettre de lancer le serveur dans le meme fichier )

    with lock_pops:
        pid_herbe=init_population()

 
    #intit de la communication avec le display

    queue = Queue(10)
    evnquit = Event()
    displ = Process(target = display.display, args = (queue,evnquit,os.getpid()))
    displ.start()

    
    #init du serveur qui gère l'environnement
    HOST = "localhost"
    PORT = 1789
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    server_socket.setblocking(False)
    pool = ThreadPoolExecutor()
    
    print("L'environnement est setup : ")

    global sim_running
    sim_running = True
    while sim_running:
        if evnquit.wait(timeout=0.01):  
            sim_running=False  
            queue.put(("exit",))
            with serve.get_lock():
                serve.value = 0
        send_data_to_display("all")
        try:
            readable, _, _ = select.select([server_socket], [], [], 1)
            if server_socket in readable:
                client_socket, addr = server_socket.accept()
                pool.submit(server_request_update, client_socket, serve)

        except OSError:
            break

    print("debut de la fin, quittez vite ce monde numérique avant de vous faire effacer a jamais !\n(seulement si vous avez un Process ID)")
    server_socket.close()
    with serve.get_lock():
        serve=0
    pool.shutdown(wait=True)
    kill_all_alive(pid_log,pid_log_lock) #tue tout le monde a la fin du programme pour éviter les orphelins
    send_signal_kill(pid_herbe)
    print("\n\n\n\n C'est la fin du programme \n\n\n\n")

   