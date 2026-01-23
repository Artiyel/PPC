import random,time

def proie():
    time.sleep(10) #pour avoir le temps de lancer le serveur avant que la connection ne s'effectue
    energie=100
    while energie>0:
        time.sleep(random.randint(0,5))
        if energie > 80:
            print("feed on grass (and more)")
            #gagne de l'energie from eating grass
            #reproduce
            #perd 5 energie en plus (ils baisent fort)

        elif energie > 60 :
            print("just feed on grass")
            #gagne de energie from eating grass
        else :
            print("se reposer")
            #gagne de l'energie
        #perd de l'énergie
