"""                      
Created on 04/20/2018

author: pdpablo
front-end: Josephine Rubio

This module logs in the user and determines if he is enrolled in the
FPS' internal database.  It then retrieves the ID number of his 
fingerprint and accesses the sqlite to find his corresponding 
Private and Public Keys.  A file named 'Session.a' is created 
containing the private key and a file named 'Session.b' is created
containing the public key.  These temporary files will be deleted after 
the encryption/decryption session is over.

"""


import FPS, sys, sqlite3, hashlib
from unidecode import unidecode
DEVICE_GPIO = '/dev/ttyAMA0'
DEVICE_LINUX = '/dev/ttyUSB0'
DEVICE_MAC = '/dev/cu.usbserial-A601EQ14'
DEVICE_WINDOWS = 'COM9'
FPS.BAUD = 9600
FPS.DEVICE_NAME = DEVICE_MAC
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Tkinter import *
import tkMessageBox



root = Tk()
w = Label(root)
w.pack()

def Loggin(fps):
    '''
    Log in and retrieve ID
    '''
    enrollid = SlotFinder()
    while not fps.IsPressFinger():
        FPS.delay(3)
        iret = 0
    if fps.CaptureFinger(True):
        tkMessageBox.showinfo("", "PLACE YOUR FINGER")
            #remove finger
        print 'remove finger'
        iret = fps.Identify1_N()
        print(iret)
        vs = str(iret)
        idkey = open('/home/pi/python-GT511c3/Session.idk', 'w')
        idkey.write(vs)
	idkey.close()
        
   

  

def SlotFinder():
    eid=0
    eAlready=True
    while eAlready is True and eid < 3000:
        eAlready = fps.CheckEnrolled(eid)
        if eAlready == True:
            eid += 1
    print('slot available is '+ str(eid))
    return eid

               

if __name__ == '__main__':
    fps = FPS.FPS_GT511C3(device_name=DEVICE_LINUX,baud=9600,timeout=2,is_com=False) #settings for raspberry pi GPIO
    fps.Open()
    if fps.SetLED(True):
        Loggin(fps)
        tkMessageBox.showinfo("", "LOGIN SUCCESSFUL")
        fps.SetLED(False)
        fps.Close()
        
