import random,time

def predateur():
    energie=100
    while energie>0:
        time.sleep(random.randint(0,5))
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
        #perd de l'énergie
