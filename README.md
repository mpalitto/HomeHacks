# HomeHacks
Collection of little projects used at my home...
## HP Printer Hack
HP Printer (HP Color LaserJet MFP M281fdw) did not work when using the **Scan to email** feature, no matter the settings.

I was able to go around this issue with the following strategy:

1. I have used the Little 10 EURO OrangePi Linux Server for getting a SAMBA Network-drive.
2. **Scan to network-drive** from printer
3. Linux Server check for new file in Network-drive and send to email using the FREE smtp gmail server.

Look into the [HP-Printer-Hack](https://github.com/mpalitto/HomeHacks/tree/HP-Printer-Hack/HP-Printer_Hack) folder for the Sever bash code

Look into the [WiKi](https://github.com/mpalitto/HomeHacks/wiki/HP-Printer-Hack) for datailed instructions

## sONOFF Local Server
sONOFF are WIFI relais that can be controlled by APP.

They way it works is that each relay connects to a cloud server which is the HUB for all the switches and the APP connects to.
APP sends commands to the Cloud Server which are forwarded to the sONOFF devices, sONOFF device send status info to the Cloud Server which sends it to the APP.

With this hack I will get the sONOFF to connetct to a local server, thus sONOFF devices can be operated even without internet connection.

See [WiKi sONOFF Local Server](https://github.com/mpalitto/HomeHacks/wiki/sONOFF-Local-Server) for details.

### files

[sONOFFserver/socket.js](https://github.com/mpalitto/HomeHacks/blob/sONOFFserver/sONOFFserver/socket.js) is the nodeJS program implementig the sONOFFserver
[sONOFFserver/iptables.rules.sh](https://github.com/mpalitto/HomeHacks/blob/sONOFFserver/sONOFFserver/iptables.rules.sh) the shell script for setting the IPTABLEs rules for redirecting the sONOFF sent packet to local port and address
