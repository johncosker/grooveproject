import socket
import fcntl
import struct
import subprocess
import sys
from time import sleep

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
        )[20:24])

def check_for_open_port(port):
    port = 5055
    process = subprocess.Popen(['netstat', '-tulpn'], stdout=subprocess.PIPE)
    pid = ''
    output = ''
    while True:
        out = process.stdout.read()
        if out == '' and process.poll() != None:
            break
        if out != '':
            output += str(out)

    output = output.split('\n')
    for line in output:
        if str(port) in line:
            phrase = line.split(' ')
            for word in phrase:
                if len(word) > 1:
                    pid = word.split('/')[0]
    if pid != '':
        process = subprocess.Popen(['kill', '-9', pid], stdout=subprocess.PIPE)
    sleep(1)