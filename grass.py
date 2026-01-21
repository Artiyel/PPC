import time,random

def herbe_growth(condition,populations):
    while True:
        time.sleep(random.randint(2,6))
        if condition == "normal" :
             #send growth through socket