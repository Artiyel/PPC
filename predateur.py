import random, time, socket, os
from pickle import dumps
from signal import signal, SIGTERM

def predateur_decision(energie, client_socket):
    if energie > 80:
        action = "reproduce"
    elif energie < 60:
        action = "eats"
    else:
        return None, energie - 5
    return [action, "pred", f"{os.getpid()}"], energie - 10

# signal handler pour mort forcée  
def die_now(signum, frame):
    os._exit(0)
signal(SIGTERM, die_now)

def predateur(): 
    energie = 70
    HOST, PORT = "localhost", 1789

    # setup socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.settimeout(15)

        while energie > 0:
            m, energie = predateur_decision(energie, client_socket)
            if m:
                try:
                    client_socket.send(dumps(m))
                except (BrokenPipeError, ConnectionRefusedError):
                    break

                try:
                    succes = client_socket.recv(1024)
                    if not succes:
                        break
                    succes = succes.decode()
                    if succes == "you_die":
                        break
                    elif succes == "yes_ate":
                        energie += 40
                    elif succes == "no_reproduce":
                        print("Pred can't reproduce because lonely );")
                    elif succes == "reproduced":
                        energie -= 10
    
                except (ConnectionResetError, BrokenPipeError, TimeoutError, OSError):
                    break

            time.sleep(random.randint(1, 5))

        # mort naturelle : notifier serveur
        try:
            client_socket.send(dumps(["died", "pred", f"{os.getpid()}"]))
        except:
            pass
