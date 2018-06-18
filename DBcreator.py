'''
Created on 04/20/2018

@author: pdpablo

SAMPLE CODE:

This is for to creating a database for the private and public key.
Execute this script only once
'''


import sqlite3

conn = sqlite3.connect("/home/pi/FingerCrypt/finger.db")
c = conn.cursor()
c.execute("CREATE TABLE codes(idk integer, prvkey blob, pbckey blob)")
conn.commit()
conn.close