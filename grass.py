import time,random,signal

def herbe_growth(condition,populations,pop_lock):
    global sim_running
    sim_running=True
    while sim_running:
        time.sleep(random.randint(0,500)/100)
        if condition.value == 0 :
            with pop_lock:
                if populations[2]<20:
                    populations[2]+=+2
        elif condition.value == 1 :
            print("secheresse pendant 10 secondes !")
            time.sleep(10)
            print("fin de secheresse !")
            condition.value==0

def stop_that_grass_from_growing_nowwww(signum,frame):
    global sim_running 
    sim_running=False

#init des signals handlers
signal.signal(signal.SIGUSR2,stop_that_grass_from_growing_nowwww)
signal.signal(signal.SIGINT, signal.SIG_IGN) #ingore le siginterrupt (histoire qu'il ne meure qu'avec le sigterm)


if __name__=="__main__":
    herbe_growth()