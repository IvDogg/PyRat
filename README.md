# PyRat
Python Remote Access Tool (RAT) - Persistent RAT, connects to Listening RAT server.  Rot13 encoded C2 traffic. 90% success rate at evading AV/IDS even when compiled.

Credit where credit is due:

Base code developed by Mark Bagget for SANS 573, originally developed for C2 in the clear to a Netcat listener.

1 - Modified traffic to use rot13 encoding to evade Shell Code IDS signatures, in term had to create a listening controller that spoke the same encoding.  I know rot13 isn't that evasive, just testing with rot13 for now.  Will probably use multiple encoding or XOR key to actually hide C2.

2 - Obfuscated some of the module calls to additionally evade IDS/AV.

