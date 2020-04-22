# coding: utf-8

# An example using startStreams

# !/usr/bin/python3
import logging
#import concurrent.futures
from tkinter import *
import threading

class Value:
    """
    Class to allow a single element value between producer and consumer.
    """
    def __init__(self):
        self.value = 0
        #self.producer_lock = threading.Lock()
        #self.consumer_lock = threading.Lock()
        #self.consumer_lock.acquire()

    def get_value(self, name):
        #self.consumer_lock.acquire()
        value = self.value
        #self.producer_lock.release()
        return value

    def set_value(self, value, name):
        #logging.info("%s:about to acquire setlock", name)
        #self.producer_lock.acquire()
        #logging.info("%s:have setlock", name)
        self.value = value
        #logging.info("%s:about to release getlock", name)
        #self.consumer_lock.release()
        #logging.info("%s:getlock released", name)
        print(value)

valueLL = Value()
valueUL = Value()
valueCAL = Value()

def setLL(val):
    valueLL.set_value(int(val), 'Producer')

def setUL(val):
    valueUL.set_value(int(val), 'Producer')

def setCAL(val):
    valueCAL.set_value(int(val), 'Producer')

def slider():
    root = Tk()
    #var = DoubleVar()
    #scale = Scale( root, variable = var, to = 4500, command = sel )
    scale = Scale( root, label = 'LL', resolution = 5, tickinterval = 100, length = 2000, orient = HORIZONTAL, to = 4500, command = setLL )
    scale.pack(anchor = CENTER)
    
    scale = Scale( root, label = 'UL', resolution = 5, tickinterval = 100, length = 2000, orient = HORIZONTAL, to = 4500, command = setUL )
    scale.pack(anchor = CENTER)
    
    scale = Scale( root, label = 'CAL', resolution = 1, tickinterval = 10, length = 2000, orient = HORIZONTAL, to = 100, command = setCAL )
    scale.pack(anchor = CENTER)
    
    button = Button(root, text = "Get Scale Value")
    button.pack(anchor = CENTER)
    
    label = Label(root)
    label.pack()
    
    root.mainloop()


x = threading.Thread(target=slider)
x.start()

import numpy as np

import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
try:
    from pylibfreenect2 import OpenGLPacketPipeline
    pipeline = OpenGLPacketPipeline()
except:
    try:
        from pylibfreenect2 import OpenCLPacketPipeline
        pipeline = OpenCLPacketPipeline()
    except:
        from pylibfreenect2 import CpuPacketPipeline
        pipeline = CpuPacketPipeline()
print("Packet pipeline:", type(pipeline).__name__)

enable_rgb = True
enable_depth = True

fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    print("No device connected!")
    sys.exit(1)

serial = fn.getDeviceSerialNumber(0)
device = fn.openDevice(serial, pipeline=pipeline)

types = 0
if enable_rgb:
    types |= FrameType.Color
if enable_depth:
    types |= (FrameType.Ir | FrameType.Depth)
listener = SyncMultiFrameListener(types)

# Register listeners
device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)

if enable_rgb and enable_depth:
    device.start()
else:
    device.startStreams(rgb=enable_rgb, depth=enable_depth)

# NOTE: must be called after device.start()
if enable_depth:
    registration = Registration(device.getIrCameraParams(),
                                device.getColorCameraParams())

undistorted = Frame(512, 424, 4)
registered = Frame(512, 424, 4)
bigdepth = Frame(1920, 1082, 4)
color_depth_map = np.zeros((424, 512),  np.int32).ravel()

rows = 424
cols = 512
ll = 0.
ul = 4500.
rowStr = ''
distance = 0.
#newDepthImg = [[0] * cols for i in range(rows)]
newBigDepthArr = np.zeros([1082, 1920], dtype=float)
newBigDcrop = np.zeros([420, 420], dtype=float)
newDepthArr = np.zeros([rows, cols], dtype=float)
newDepthImg = np.zeros([360, 640], dtype=float)
#newRGBarr = np.zeros([288, cols, 4], dtype=np.uint8)
newRGBarr = np.zeros([1080, 2020, 4], dtype=np.uint8)
newRGBimg = np.zeros([420, 420], dtype=float)
bkground = np.zeros([420, 420], dtype=float)
me = np.zeros([420, 420], dtype=float)

reminder = np.zeros([136, cols, 4], dtype=np.uint8)

while True:
    ll = valueLL.get_value('consumer')
    ul = valueUL.get_value('consumer')
    cal = valueCAL.get_value('consumer')
#if True:
    frames = listener.waitForNewFrame()

    if enable_rgb:
        color = frames["color"]
    if enable_depth:
        ir = frames["ir"]
        depth = frames["depth"]

    if enable_rgb and enable_depth:
        enable_filter = True
        registration.apply(color, depth, undistorted, registered,
                        enable_filter,
                        bigdepth=bigdepth, 
                        color_depth_map=color_depth_map)
    elif enable_depth:
        registration.undistortDepth(depth, undistorted)

    if enable_depth:
        #cv2.imshow("ir", ir.asarray() / 65535.)

        #newDepthArr = depth.asarray()
        #newDepthImg[newDepthArr < ul] = 1.
        #newDepthImg[newDepthArr > ul] = 0.
        #newDepthImg[newDepthArr < ll] = 0.
        
        #with open("depthArray.txt", mode="wt", encoding="utf-8") as f:
        #for row in range(0, rows, 8):
        #    for col in range(0, cols, 8):
        #        distance = depthArray[row][col]
        #        if (distance > ll and distance < ul):
        #            for i in range(8):
        #                newDepthImg[row][col+i] = 1.
        #        else:
        #            for i in range(8):
        #                newDepthImg[row][col+i] = 0.

                    #rowStr += str(newDepthImg[row][col]) + ':' + str(depthArray[row][col]) + '\t' 
                #f.write(rowStr + '\n')
                #rowStr = ''
        #cv2.imshow("depth", newDepthImg)
        #cv2.imshow("depth", depthArray)

        #with open("depthArray.txt", mode="wt", encoding="utf-8") as f:
        #    for row in newDepthImg:
        #        f.write('\t'.join(str(elm) for elm in row))
        #        f.write('\n')

        #cv2.imshow("undistorted", undistorted.asarray(np.float32) / 4500.)
        newBigDepthArr = cv2.resize(bigdepth.asarray(np.float32),
                                          (int(1920), int(1082)))
        newBigDcrop = newBigDepthArr[200:620, 700:1120]
        cv2.imshow("bigdepth", newBigDepthArr / 4500)
    if enable_rgb:
        newRGBarr[:,50:1970] = cv2.resize(color.asarray(),
                                       (int(1920), int(1080)))
    if enable_rgb and enable_depth:
        fake = True
        #newRGBarr = cv2.resize(color.asarray(),
        #                               (int(1920 / 2.547), int(1080 / 2.547)))
        #print(str(newRGBarr[:,120:632].shape))
        newRGBimg = newRGBarr[200:620:,700+cal:1120+cal]

        #print(str(newRGBimg.shape))
        #print(str(newBigDcrop.shape))
        #newRGBimg = registered.asarray(np.uint8)
        #newRGBimg[newBigDcrop > ul] = 0
        newBigDcrop[newBigDcrop > 4444] = 4444
        cv2.imshow("Dcrop", newBigDcrop / 4500)
        newRGBimg[newBigDcrop > ul] = np.array([0,255,0,0]) # blue, green, red, alpha 
        #me = np.subtract(newRGBimg, bkground)
        cv2.imshow("ME", newRGBimg)

        #cv2.imshow("registered", registered.asarray(np.uint8))

        

    listener.release(frames)

    key = cv2.waitKey(delay=1)
    if key == ord('q'):
        break

device.stop()
device.close()

sys.exit(0)
