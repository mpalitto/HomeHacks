# !/usr/bin/python3
import logging
import concurrent.futures
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

value = Value()

def sel(val):
    #print(val)
    value.set_value(val, 'Producer')

def slider():
    root = Tk()
    var = DoubleVar()
    scale = Scale( root, variable = var, command = sel )
    scale.pack(anchor = CENTER)
    
    button = Button(root, text = "Get Scale Value")
    button.pack(anchor = CENTER)
    
    label = Label(root)
    label.pack()
    
    root.mainloop()


x = threading.Thread(target=slider)
x.start()

#if __name__ == "__main__":
#    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#        executor.submit(producer, value)
