import random,time,socket
from os import getpid
from pickle import dumps

def predateur_decision(energie):
    while energie>0:
        time.sleep(random.randint(1,5))
        if energie > 80:
            print("feed on prey (and more)")
            #gagne un peu d'energie from eating prey
            #reproduce
            #perd 5 energie en plus (ils baisent fort)

        elif energie > 60 :
            print("just feed on prey")
            #gagne un peu d'energie from eating prey
        else :
            print("se reposer")
            #gagne un petit peu
        return [],energie-10
    return ["died","pred",f"{getpid()}"],0


#["type","espece qui envoie l'info","pid"]
def predateur():
    #init du predateur
    time.sleep(1) #pour avoir le temps de lancer le serveur avant que la connection ne s'effectue
    energie=100
    
    #init communication avec env
    HOST = "localhost"
    PORT = 1789
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        while True:
            m,energie = predateur_decision(energie)
            if m != []:
                client_socket.sendall()

if __name__=="__main__":
    predateur()
