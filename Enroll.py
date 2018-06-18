'''
Created on 08/04/2014

author: jeanmachuca
modder: pdpablo
front-end: Josephine Rubio



This script Enrolls your finger in the device internal database
you have 3000 ids available for enroll
Each time you executes this enroll script, enrollid is autoincrement for a free number

'''
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

def LegacyEnroll(fps):
    '''
    Enroll test
    '''
    enrollid = SlotFinder()
    
    if enrollid <3000:
        #press finger to Enroll enrollid
        tkMessageBox.showinfo("", "PLACE YOUR FINGER TO ENROLL")
        print 'Press finger to Enroll %s' % str(enrollid)
        fps.EnrollStart(enrollid)
        while not fps.IsPressFinger():
            FPS.delay(3)
        iret = 0
        if fps.CaptureFinger(True):
            #remove finger
            print 'remove finger'
            fps.Enroll1()
            while not fps.IsPressFinger():
                FPS.delay(3)
            #Press same finger again
            print 'Press same finger again'
            while not fps.IsPressFinger():
                FPS.delay(3)
            if fps.CaptureFinger(True):
                #remove finger
                print 'remove finger'
                fps.Enroll2()
                while not fps.IsPressFinger():
                    FPS.delay(3)
                #Press same finger again
                print 'press same finger yet again'
                while not fps.IsPressFinger():
                    FPS.delay(3)
                if fps.CaptureFinger(True):
                    #remove finger
                    iret = fps.Enroll3()
                    if iret == 0:
                        tkMessageBox.showinfo("", "ENROLLING SUCCESSFUL")
                        print 'Enrolling Successfull'
			addrprivate = RSA.generate(1024)
			addrpublic = addrprivate.publickey()
                        PrivKey = addrprivate.exportKey()
			PublKey = addrpublic.exportKey()
                        dBaseSync(enrollid, PrivKey, PublKey)
                    else:
                        tkMessageBox.showinfo("", "ENROLLING FAILED")
                        print 'Enrolling Failed with error code: %s' % str(iret)
                else:
                    print 'Failed to capture third finger'
            else:
                print 'Failed to capture second finger'
        else:
            print 'Failed to capture first finger'
    else:
        print 'Failed: enroll storage is full' 

def SlotFinder():
    eid=0
    eAlready=True
    while eAlready is True and eid < 3000:
        eAlready = fps.CheckEnrolled(eid)
        if eAlready == True:
            eid += 1
    print('slot available is '+ str(eid))
    return eid

def dBaseSync(kid, key1, key2):
    conn = sqlite3.connect("/home/pi/python-GT511c3/finger.db")
    row = [kid, key1, key2]
    print(row)
    c = conn.cursor()
    c.execute("INSERT INTO codes VALUES(?, ?, ?)", row)
    conn.commit()
    conn.close
                

if __name__ == '__main__':
    fps = FPS.FPS_GT511C3(device_name=DEVICE_LINUX,baud=9600,timeout=2,is_com=False) #settings for raspberry pi GPIO
    fps.Open()
    if fps.SetLED(True):
        LegacyEnroll(fps)
        fps.SetLED(False)
        fps.Close()
