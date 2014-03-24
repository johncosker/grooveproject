# UDP multicast sender
import socket
from time import sleep
UDP_IP = "192.168.1.16"
UDP_PORT = 4242
MESSAGE = "play"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM,      # UDP
             socket.IPPROTO_UDP)     # Multicast recvier
             
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

for x in range(0,1):
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sleep(3)