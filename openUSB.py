'''
Created on 04/20/2018

author: pdpablo
front-end: Josephine Rubio

This script will open directly the mass storage that is conneccted to the 
Raspberry Pi so the user can check the content of the Mass Storage.
'''

import sys, os, subprocess
import shutil

hdd = "/media/pi/"
ObjDir = os.listdir(hdd)
EncDir = hdd + ObjDir[0] + os.sep
os.system('xdg-open "%s"' % str(EncDir))
