# HomeHacks
Collection of little projects used at my home...

=======

## IP Cam Home Security Alarm

I have a cheap IPcam that has the motion detection which is not usable bc it gives too many false alarms.

I have made use of **tensorflow.js** for making a functional person detector.

When a person is detected frames are saved and an email is sent to ALERT me of the detection with attached the pics of the villan.

Future developments:

In the future I might add facial recognition if I wanted to use it as a Welcome IP cam...

Also I might want to add some PIR sensor for detecting in other rooms possible unexpected bodies...

Since the IPcam has PAN&TILT, I might add (for fun) the follow a person as it moves... (spookie).

Check the WIKI page for more details.

=======

## Kinect
It has always affascinated me the ability of sensing distance in an image and detection of direction for sound sources.

Kinect is an affordable device that just do that.
1. has a depth sensor for measuring distance of light for each pixel
2. has mic array wich can be used to calculate the Direction of Arrival for the sound

These could be used, for example, for a robot whom is able to recognise the room in which it is located and, if anybody talks to it, where to turn to and how to select the sound coming from the human mouth for better listening....

In this section I am going to record my experiments with Kinect.

It looks like the easyest way to access programmatically from Linux PC to the Kinect is using PYLIBFREENECT2 python library.

I am not very happy bc I don't like Python...

This lib comes with 2 examples (in the example folder).

I have modified selective_streams.py and added a graphical control for playing with some parameters.

By playing manually with the parameters I can make the background to disappear (black color) and the RGB image be centered into the depth mask.

Three parameters: LL (Close Layer), UL (Far Layer), CAL (camera calibration)

Everything closer than the LL is blocked (masked), everything farther than UL is bolcked. In this way I can select what to show in the image. For example I can block the background.

The CAL allows to shift left the RGB image so that can be centered to the mask.

for running the program:
make sure the evironment varible ``export LD_LIBRARY_PATH="/home/matteo/dev/HomeHacks/Kinect/freenect2/lib"`` is set to where the ``freenect2`` libs are found.
```
python3 examples/selective_streams.py
```
to stop just press TWICE **Ctrl-C**



python3 
=======

## Current Alarm
Measuring total draw current consuption for my condo, dispaly measurement on a current monitor display, and if the current value gets higher than a threshold, a disco light turns on to alarm the ppl around.

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
