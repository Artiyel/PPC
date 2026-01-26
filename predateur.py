import random,time,socket
from os import getpid
from pickle import dumps
from signal import SIGUSR2,signal,SIGINT,SIG_IGN

def predateur_decision(energie,client_socket):
    if energie > 80:
        action="reproduce"

    elif energie <40 :
        action="eats"

    else :
        return None,energie-5
    
    return [action,"pred",f"{getpid()}"],energie-10


def kill_par_signal(signum, frame):
    global dead
    dead=True

def predateur():
    #init des signal handler
    signal(SIGINT,SIG_IGN) #ne meurt que quand sigterm est appelé
    signal(SIGUSR2 ,kill_par_signal) #nouveau handler pour sigterm afin de tuer proprement le process


    #init du predateur
    time.sleep(3) #pour avoir le temps de lancer le serveur avant que la connection ne s'effectue
    global energie,dead  
    energie=70
    dead=False


    
    #init communication avec env
    HOST = "localhost"
    PORT = 1789
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        while energie>0:
            m,energie = predateur_decision(energie,client_socket)
            if m != None:
                try:
                    client_socket.send(dumps(m))
                except (BrokenPipeError,ConnectionRefusedError):
                    pass
                try:
                    succes = client_socket.recv(1024)
                    if not succes:
                        break
                    succes = succes.decode()
                    if succes=="yes_ate":
                        energie+=20
                    elif succes=="no_reproduce":
                        print("Pred can't reproduce because lonely ); ")

                except (ConnectionResetError, BrokenPipeError,ConnectionAbortedError,ConnectionRefusedError):
                    break


            time.sleep(random.randint(1,5)) # attend après chaque action
            if dead:
                break


        try:
            client_socket.send(dumps(["died","pred",f"{getpid()}"]))
        except (BrokenPipeError, OSError):
            pass

        client_socket.close()


if __name__=="__main__":
    predateur()
