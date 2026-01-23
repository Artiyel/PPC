import time,random

def herbe_growth(condition,populations):
    time.sleep(10) #pour avoir le temps de lancer le serveur avant que la connection ne s'effectue
    while True:
        time.sleep(random.randint(2,6))
        if condition == "normal" :
             #send growth through socket
             print("berbe")