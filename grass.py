import time,random

def herbe(condition,lock):
    with lock:
        while brins_dherbe >0:
            time.sleep(random.randint(2,6))
            if condition == "normal" : 
                brins_dherbe = int(brins_dherbe*1.25)