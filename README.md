# HomeHacks
Collection of little projects used at my home...

=======

## Current Alarm
Measure total draw current consuption for my condo, current than gets dispalyed by a current monitor display, and if the current value gets higher than a threshold a dico light turns on to alarm the ppl around

* current sensor (managed by ESP12 NODE MCU) connects throug WIFI to home server
* Home Server (Linux OrangePi) hosting server side scripts
* home server reads current values and send them to LED Matrix Display  (managed by ESP12 NODE MCU)
* home server checks for threshold and eventually turns Rotating Disco Light as an alarm (using sONOFF)

### FILEs: (see CurrentAlarm folder)
#### Home Server Scripts
* startCurrentAlarm.sh - start a "screen" detached session for running the "currentAlarm.sh" script
* currentAlarm.sh - runs the NODE.JS script implementing the server for the current sensor connection and controls sONOFF light and ESP12 display
* currentSocketServer.js - socket Server for receiving the current measurements and printing on stdout the values

#### Current Sensor
work in progress (need to add ino file)

A current sensor (with a little analog circuit: 2 resistors and a diode) connected to the analog input of a ESP12 NODE MCU.

The NODE MCU connects to home server and sends current readings.

#### LED Matrix Display
work in progress (need to add ino file)

implements a socket server (connected to LAN using WIFI on a NODE MCU) to which anyone can connect to and send text to be displayed.

=======
## HP Printer Hack
HP Printer (HP Color LaserJet MFP M281fdw) did not work when using the **Scan to email** feature, no matter the settings.

I was able to go around this issue with the following strategy:

1. I have used the Little 10 EURO OrangePi Linux Server for getting a SAMBA Network-drive.
2. **Scan to network-drive** from printer
3. Linux Server check for new file in Network-drive and send to email using the FREE smtp gmail server.

Look into the [HP-Printer-Hack](https://github.com/mpalitto/HomeHacks/tree/HP-Printer-Hack/HP-Printer_Hack) folder for the Sever bash code

Look into the [WiKi](https://github.com/mpalitto/HomeHacks/wiki/HP-Printer-Hack) for datailed instructions

========

## CurrentDrawMonitor-MQTT
Questa versione non piu' mantenuta connette il sensore di corrente (gestito da ESP12 NODE-MCU) ad un servizio MQTT.

Uno script su server 'subscribes' al canale e scrive i valori su foglio google-sheet

Interessante ma poco utile...

E' stato sostituito dalla versione in uso di **CurrentAlarm*
