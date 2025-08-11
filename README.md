# ARP Spoofing & TCP Hijacking

Educational project demonstrating two well-known network attacks inside a controlled Docker-based lab.  

The network consists of four containers: **server**, **client**, **middle** (attacker), and **router**.

---

## ARP Spoofing – Attack Flow
1. The attacker sends forged ARP replies to both the server and the router.  
2. The server is tricked into associating the attacker's MAC address with the router's IP.  
3. The router is tricked into associating the attacker's MAC address with the server's IP.  
4. As a result, all traffic between server and router is routed through the attacker (Man-in-the-Middle).  
5. The attacker can now capture, read, and analyze the intercepted packets (e.g., HTTP requests and responses).

---

## TCP Hijacking – Attack Flow
1. The attacker must already be in a Man-in-the-Middle position (e.g., via ARP Spoofing).  
2. Using `NetfilterQueue`, packets from an active TCP connection are intercepted before they leave the attacker’s machine.  
3. The attacker inspects each packet and replaces the original payload with a modified version.  
4. Checksums and length fields are recalculated to ensure the modified packet is valid.  
5. The altered packet is forwarded to the destination, making the change invisible to both client and server.

---

The project uses:
- **Scapy** – crafting and sending custom packets  
- **NetfilterQueue** – intercepting packets at kernel level  
- **iptables** – routing traffic through the attacker  
- **tcpdump** – monitoring network activity  

