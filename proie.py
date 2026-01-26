import random,time,socket
from os import getpid
from pickle import dumps
from signal import SIGTERM,signal,SIGINT,SIG_IGN

def proie_decision(energie,client_socket):
    if energie > 80:
        action="reproduce"

    elif energie <40 :
        action="eats"
    else :
        return None, energie-5

    return [action,"proie",f"{getpid()}"],energie-10
 


def kill_par_signal(signum, frame):
    global energie
    energie= -100 # on le super-tue pour pas qu'il puisse manger quelqu'un et revivre


def proie():
    #init proie
    time.sleep(2) #pour avoir le temps de lancer le serveur avant que la connection ne s'effectue
    global energie
    energie=100
    
    #init des signals handler
    signal(SIGTERM ,kill_par_signal) #nouveau handler pour sigterm afin de tuer proprement le process
    signal(SIGINT,SIG_IGN) #ne meurt que quand sigterm est appelé

    #init communication avec env
    HOST = "localhost"
    PORT = 1789
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        while energie>0:
            m,energie = proie_decision(energie,client_socket)
            if m != None:
                client_socket.send(dumps(m))
                try:
                    succes = client_socket.recv(1024)
                    if not succes:
                        break
                    succes = succes.decode()
                    if succes=="yes_ate":
                        energie+=20
                    elif succes=="no_reproduce":
                        print("Prey can't reproduce because lonely ); ")
                        
                except (ConnectionResetError, BrokenPipeError,ConnectionAbortedError,ConnectionRefusedError):
                    break
            time.sleep(random.randint(1,5)) #ne fait rien pendant un temps après chaque action

        client_socket.send(dumps(["died","proie",f"{getpid()}"]))
        client_socket.close()

    
    
if __name__=="__main__":
    proie()