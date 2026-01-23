from multiprocessing import Lock,Process,Array,Value,Queue,Event
import select,random,socket
import grass,predateur,proie,display
from pickle import loads
from concurrent.futures import ThreadPoolExecutor


def server_request_update(client_socket):
    global serve 
    client_socket.setblocking(True)
    try:
        data=client_socket.recv(1024)
        liste = loads(data) #format de liste : ["type","espece qui envoie l'info","pid"] type=eats,died,reproduce
        
        if liste[0] == 'died':
            dies_like_a_bozo(liste)

        elif liste[0] == "reproduce":
            reproduce_like_a_chad(liste)

        else:
            try_to_kill(liste,client_socket)
            
    except Exception as e:
        print("Client error:", e)

    finally:
        try:
            client_socket.shutdown(socket.SHUT_WR)
        except:
            pass
        client_socket.close()



def dies_like_a_bozo(liste):
    with pid_log_lock:
        for i, (pid, processus) in enumerate(pid_log[liste[1]]): #rework pour attendre de finir une étape!!!!!
            if pid == liste[2]:
                processus.terminate()
                processus.join()
                del pid_log[liste[1]][i]
                break #until ici !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    with populations.get_lock():
        match liste[1]:
            case "pred":
                populations[0]-=1
                send_data_to_display('pred')
            case "proie":
                populations[1]-=1
                send_data_to_display('proie')

def try_to_kill(liste,client_socket):
    succes='no'
    with populations.get_lock():
        match liste[1]:
            case "pred":
                if populations[1]>0:
                    succes='yes'
                    with pid_log_lock:  #rework ce block !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        on_tue_ki_index=random.randint(0,len(pid_log["pred"])-1)
                        (a,b)=pid_log["pred"][on_tue_ki_index]
                        b.terminate()
                        b.join()
                        del pid_log["pred"][pid_log["pred"][on_tue_ki_index]] #until ici !!!!!!!!!!!!!!!!!
                    populations[1]-=1
                    send_data_to_display('proie')

            case "proie":
                if populations[2]> 0:
                    populations[2]-=1
                    send_data_to_display('grass')
                    succes="yes"

    client_socket.send(succes.encode())

def reproduce_like_a_chad(liste):
    match liste[1]:
        case "pred":
            Process(target=predateur.predateur, args=()).start()
            with populations.get_lock():
                populations[0]+=1
                Queue.put(("pred",populations[0]))
        case "proie":
            Process(target=proie.proie, args=()).start()
            with populations.get_lock():
                populations[1]+=1
                Queue.put(("proie",populations[1]))
        case "grass":
            with populations.get_lock():
                populations[2]= int(populations[2]*1.25)
                Queue.put(("grass",populations[2]))

def send_data_to_display(species):
    match species:
        case "grass":
            Queue.put("grass",populations[2])
        case "proie":
            Queue.put("proie",populations[1])
        case "pred":
            Queue.put("pred",populations[0])

if __name__ == '__main__':
    
    populations = Array('i', [10,10,10])
    lock_pops= populations.get_lock()
    grass_status= Value("c")
    pid_log={
        "pred":[],
        "proie":[],#liste de tuples (pid:process)
    }
    pid_log_lock=Lock()

    
    # lancer tout les processssss qui sont client (lancés avec délais
    # pour permettre de lancer le serveur dans le meme fichier )

    for i in range(len(populations)):
        match i:
            case 0:
                for j in range(populations[i]):
                    p=Process(target=predateur.predateur, args=())
                    p.start()
                    with pid_log_lock:
                        pid_log["pred"].append((p.pid,p))

            case 1:
                for j in range(populations[i]):
                    p=Process(target=proie.proie, args=())
                    p.start()
                    with pid_log_lock:
                        pid_log["proie"].append((p.pid,p))
            case 2:
                Process(target=grass.herbe_growth,args=(populations,grass_status)).start()

 
    #intialiser le serveur qui gere la commmunication avec la population.

    HOST = "localhost"
    PORT = 1789
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    server_socket.setblocking(False)
    queue = Queue(10)
    evnevent = Event()
    evnquit = Event()
    events = [evnevent,evnquit]
    displ = Process(target = display.display, args = (queue,events))
    displ.start()

    pool = ThreadPoolExecutor()
    
    print("L'environnement est setup : ")

    sim_running = True
    while sim_running:
        queue.put(("pred",populations[0]))
        if  evnquit:
            queue.put(("exit",))
            sim_running = False
            # mettre comment arrêter le reste
        try:
            readable, _, _ = select.select([server_socket], [], [], 1)
            if server_socket in readable:
                client_socket, addr = server_socket.accept()
                pool.submit(server_request_update, client_socket)
        except OSError:
            break




    