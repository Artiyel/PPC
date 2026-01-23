import random,time,socket
from os import getpid
from pickle import dumps

def predateur_decision(energie,client_socket):
    while energie>0:
        time.sleep(random.randint(1,5))
        if energie > 80:
            action="reproduce"

        elif energie <40 :
            action="eats"
            succes = client_socket.recv(1024).decode()
            if succes=="yes":
                energie+=20
        else :
            return None,energie-5
        
        return [action,"pred",f"{getpid()}"],energie-10
    return ["died","pred",f"{getpid()}"],0


#["type","espece qui envoie l'info","pid"]
def predateur():
    #init du predateur
    time.sleep(10) #pour avoir le temps de lancer le serveur avant que la connection ne s'effectue
    energie=70
    alive=True
    
    #init communication avec env
    HOST = "localhost"
    PORT = 1789
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        while alive:
            m,energie = predateur_decision(energie,client_socket)
            if m != None:
                client_socket.send(dumps(m))
            if energie==0:
                alive=False

if __name__=="__main__":
    predateur()
