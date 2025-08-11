import socket
import logging
import time
import sys
import random


logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 10000
adresa = '198.7.0.2' 
server_address = (adresa, port)


try:
    sock.connect(server_address)

    while True:
        mesaj = random.randint(400, 500)
        print(f"[CLIENT]: Trimis - {mesaj}")
        sock.send(str(mesaj).encode())
        
        data = sock.recv(1024).decode()
        print(f"[CLIENT]: Primit - {data}")
        time.sleep(4)

except Exception as e:
    logging.error(f"Eroare: {e}")
    sock.close()
    sys.exit(1)

