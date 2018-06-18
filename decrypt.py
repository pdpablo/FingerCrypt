"""
author: platisd
modder: pdpablo
front-end: Josephine Rubio

This file was from the author's cryptopuck project.
https://github.com/platisd/cryptopuck

Script to encrypt the files.

User must login using the login.py to use this script.

"""

import sqlite3
import sys
import os
import struct
import argparse
import json
import tempfile
import shutil
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Tkinter import *
import tkMessageBox

root = Tk()
w = Label(root)
w.pack()

def initializer():
	# Check to see if there is actually a public key file
	if not os.path.isfile("/home/pi/FingerCrypt/Session.idk"):
                tkMessageBox.showinfo("FAILED", "YOU ARE NOT LOGGED IN OR ENROLLED")
		print('You are not logged in or enrolled!')
		sys.exit(1)

	hdd = "/media/pi/"
	ObjDir = os.listdir(hdd)
	DecDir = hdd + ObjDir[0] + os.sep
	Sikreto = DecDir + "secret"
	EncDir = hdd + ObjDir[0] + os.sep
	try:
                rmSVI = EncDir + "System Volume Information/"
                shutil.rmtree(rmSVI)
        except:
                return DecDir, Sikreto
	
def wrapup():
		os.remove("/home/pi/FingerCrypt/Session.idk")


def decrypt_file(key, in_filename, out_filename=None, chunksize=64*64):
    """ Decrypts a file using AES (CBC mode) with the given key.

        Adopted from Eli Bendersky's example:
        http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/

    Arguments:
        key             AES secret to decrypt the file.
        in_filename     Path to the decrypted file.
        out_filename    The name (and path) of the decrypted file. If no name
                        is supplied the decrypted file name will be the
                        original one minus the last ending
                        (e.g. example.txt.enc -> example.txt).
        chunksize       Size of the chunks to read while decrypting.
    """
    if not out_filename:
        out_filename = os.path.basename(os.path.splitext(in_filename)[0])

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


def decrypt_string(text_to_decrypt, Priv_Key):
    """ Decrypt the supplied string using our private key.

    Arguments:
        text_to_decrypt         The encrypted text
        private_key_file        The private key to decrypt

    Return:
        decrypted_text          The decrypted text
    """
    cipher = PKCS1_OAEP.new(Priv_Key)
    decrypted_text = cipher.decrypt(text_to_decrypt)
    return decrypted_text


def run(source, destination, secret):
    """ Decrypts the source folder and outputs to the destination folder.

        Arguments:
            source          The folder to be decrypted
            destination     The folder where the decrypted files will end up
            secret          The (encrypted) secret used for the encryption
            public_key      The private key to be used for the decryption
    """
    try:     
            if source[-1] != os.sep:
                source += os.sep
            if destination[-1] != os.sep:
                destination += os.sep

            # Decrypt the AES secret
            # Set default path if None provided
            if not secret:
                secret = source + "secret"
            # Check to see if there is actually an AES secret file
            if not os.path.isfile(secret):
                print("Media is not Encrypted or missing secret key " + secret)
                sys.exit(1)
            # Check to see if there is actually a private key file
            IdRet = open("/home/pi/FingerCrypt/Session.idk", 'r')
            KeyId = IdRet.read()
            IdRet.close()
            conn = sqlite3.connect("/home/pi/FingerCrypt/finger.db")
            c = conn.cursor()
            c.execute("SELECT prvkey FROM codes WHERE idk == ?", str(KeyId))
            conn.commit()
            pvt_key = RSA.importKey(c.fetchone())
            KeyPrv = pvt_key.exportKey()
            conn.close   
            # Get the decrypted AES key
            with open(secret, "rb") as aes_secret_file:
                aes_secret = aes_secret_file.read()
            decrypted_aes_secret = decrypt_string(aes_secret, pvt_key)

            # We should restore the file structure, therefore we should parse the file
            # containing the encrypted structure and create the appropriate filepaths.
            # To do that we need to restore the mapping that contains the
            # real to obscured paths combinations. The keys are the obscured filenames
            # and the values are the real paths.
            json_encrypted_map = source + "filenames_map"
            # Dictionary to hold the mapping between encrypted and real paths
            filenames_map = dict()
            if not os.path.isfile(json_encrypted_map):
                print("Warning: Will not restore file structure.")
                warning_msg = "Map between encrypted filenames and paths not found: "
                print(warning_msg + json_encrypted_map)
            else:
                # Unencrypt the json containing the filenames map into a temporary file
                with tempfile.NamedTemporaryFile(mode="r+t") as tmp_json:
                    decrypt_file(decrypted_aes_secret, json_encrypted_map,
                                 tmp_json.name)
                    tmp_json.seek(0)  # Go to the beginning of the file to read again
                    filenames_map = json.load(tmp_json)

            # Recursively unencrypt files in the source folder
            for dirpath, dirnames, filenames in os.walk(source):
                for name in filenames:
                    filename = os.path.join(dirpath, name)
                    # Do not unencrypt files that we have generated ourselves
                    if filename != secret and filename != json_encrypted_map:
                        # If the filenames mapping is defined, then we should use it
                        # to restore the original file structure
                        if filenames_map:
                            # Get the real filename and its path
                            destination_file = destination + filenames_map[name]
                            # Create the necessary folder structure
                            #folder_structure = os.path.dirname(destination_file)
                            #os.makedirs(folder_structure)
                        else:
                            # If for some reason the filenames map is not defined then
                            # suffix the files to indicate that they are decrypted
                            destination_file = destination + name + ".clear"
                        print("Decrypting: " + filename)
                        decrypt_file(decrypted_aes_secret, filename, destination_file)
                    # If we are decrypting in the same folder as the encrypted files
                    # then remove the original encrypted files
                    if source == destination:
                        if os.path.exists(filename):
                            os.remove(filename)
    except:
            tkMessageBox.showinfo("", "INVALID LOGIN")
            sys.exit(1)

if __name__ == "__main__":
	WorkFolder, MySecret = initializer()
        run(WorkFolder, WorkFolder, MySecret)
	wrapup()
	tkMessageBox.showinfo("", "DECRYPTION DONE")
