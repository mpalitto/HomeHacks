# HomeHacks
Collection of little projects used at my home...
=======
## Current Alarm
Measure total draw current consuption for my condo, current than gets dispalyed by a current monitor display, and if the current value gets higher than a threshold a dico light turns on to alarm the ppl around
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
