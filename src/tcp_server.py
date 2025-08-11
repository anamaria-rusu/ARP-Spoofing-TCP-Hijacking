import socket
import logging
import time
import random
import sys

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 10000
adresa = '0.0.0.0'
server_address = (adresa, port)

try:
    sock.bind(server_address)
    logging.info("Serverul a pornit pe %s si portul %d", adresa, port)
    sock.listen(1)

    conexiune, address = sock.accept()
    print(f"[SERVER]: Conexiune de la {address}")

    while True:
        data = conexiune.recv(1024)
        if not data:
            print("[SERVER]: Clientul s-a deconectat.")
            break

        print(f"[SERVER]: Primit - {data.decode()}")
        time.sleep(3)

        mesaj = random.randint(60, 70)
        print(f"[SERVER]: Trimis - {mesaj}")
        conexiune.send(str(mesaj).encode())

except Exception as e:
    logging.error(f"Eroare server: {e}")
finally:
    #conexiune.close()
    sock.close()

