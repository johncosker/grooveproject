#!/usr/bin/python
import socket
import subprocess
import sys, os
from time import sleep
import logging

currentDir = os.path.dirname(os.path.realpath(__file__))
baseDir = currentDir[0:currentDir.find('grooveproject')] + 'grooveproject/'
DIR_DEVIDER = "PC"


partyDir = baseDir + "waveAPI/apps/3rdParty"
logDir = baseDir + "log/python.log"
pidDir = baseDir + "waveAPI/apps/config/wv_interfaceInformer.pid"
mainDir = baseDir + "waveAPI/apps/py/"
dbDir = baseDir + "waveAPI/db/"
keyDir = baseDir + "waveAPI/apps/config/keys/"
webDir = baseDir + "waveAPI/web/"

sys.path.insert(0, partyDir)
sys.path.insert(0, mainDir)

# Set logging
logging.basicConfig(filename=logDir,
                    format='Wave Player - %(message)s',
                    level=logging.DEBUG)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return "192.168.1.7"

def get_port():
    return 5055

def get_buffer_size():
    return 1024

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

def wait():
    sleep(15)
