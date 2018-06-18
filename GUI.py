'''
Created on 04/20/2018

@author: Josephine Rubio

SAMPLE CODE:

GUI for the FingerCrypt. Provide your own image for that buttons for the following:
-Enroll
-Login
-Encrypt
-Decrypt
-Exit
-OpenUSB	
'''



from tkinter import *
from PIL import Image
from subprocess import call
import os, sys, subprocess

def donothing():
    pass

def shutdown():
    os.system("sudo shutdown -h now")



root = Tk()
root.title('Mass Storage Encryption Device')

img1 = PhotoImage(file="INSERT IMAGE FOR BUTTON")
img2 = PhotoImage(file="INSERT IMAGE FOR BUTTON")
img3 = PhotoImage(file="INSERT IMAGE FOR BUTTON")
img4 = PhotoImage(file="INSERT IMAGE FOR BUTTON")
img5 = PhotoImage(file="INSERT IMAGE FOR BUTTON")
img6 = PhotoImage(file="INSERT IMAGE FOR BUTTON")

pyprog1 = '/home/pi/FingerCrypt/Enroll.py'
def callpy(): call(['python', pyprog1] )
butt2 = Button(root, image=img1, command=callpy).place(relx=.45, rely=.18, anchor="e")

pyprog2 = '/home/pi/FingerCrypt/login.py'
def callpy(): call(['python', pyprog2] )
butt3 = Button(root, image=img2, command=callpy).place(relx=.55, rely=.18, anchor="w")

pyprog3 = '/home/pi/FingerCrypt/encrypt.py'
def callpy(): call(['python', pyprog3] )
butt2 = Button(root, image=img3, command=callpy).place(relx=.45, rely=.5, anchor="e")

pyprog4 = '/home/pi/FingerCrypt/decrypt.py'
def callpy(): call(['python', pyprog4] )
butt3 = Button(root, image=img4, command=callpy).place(relx=.55, rely=.5, anchor="w")

pyprog5 = '/home/pi/FingerCrypt/openUSB.py'
def callpy(): call(['python', pyprog5] )
butt4 = Button(root, image=img5, command=callpy).place(relx=.45, rely=.82, anchor="e")

butt5 = Button(root, image=img6, command = shutdown).place(relx=.55, rely=.82, anchor="w")


root.configure(bg="#EDE5A6")
root.geometry('951x602')
root.mainloop()
