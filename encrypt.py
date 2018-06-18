"""
author: platisd
modder: pdpablo
front-end: Josephine Rubio

This file was from the author's cryptopuck project.
https://github.com/platisd/cryptopuck

Script to decrypt the files.

User must login using the login.py to use this script.
"""

import sys, sqlite3
import os
import struct
from base64 import b64encode
import hashlib
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
	EncDir = hdd + ObjDir[0] + os.sep
	try:
                rmSVI = EncDir + "System Volume Information"
                shutil.rmtree(rmSVI)
        except:
                return EncDir

def wrapup():

		os.remove("/home/pi/FingerCrypt/Session.idk")
	
def encrypt_file(key, in_filename, out_filename=None, chunksize=64*64):
    """ Encrypts a file using AES (CBC mode) with the
        given key.


        Arguments:
            key             The encryption key - a string that must be
                            either 16, 24 or 32 bytes long. Longer keys
                            are more secure.
            in_filename     Path to the file to be encrypted.
            out_filename    The name (and path) for the encrypted file to be
                            generated.
                            If no filename is supplied, the encrypted file name
                            will be the original plus the `.enc` suffix.
            chunksize       Sets the size of the chunk which the function
                            uses to read and encrypt the file. Larger chunk
                            sizes can be faster for some files and machines.
                            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = os.path.basename(in_filename) + '.enc'

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' '.encode("UTF-8") * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def encrypt_string(text_to_encrypt):
    """ Encrypt the supplied string using our public key.

        Arguments:
            text_to_encrypt     The plain text to encrypt
            public_key_file     The public key to be used for encryption

        Return:
            encrypted_text      The encrypted text using the public key
    """
    try:
            IdRet = open("/home/pi/FingerCrypt/Session.idk", 'r')
            KeyId = IdRet.read()
            IdRet.close()
            conn = sqlite3.connect("/home/pi/FingerCrypt/finger.db")
            c = conn.cursor()
            c.execute("SELECT pbckey FROM codes WHERE idk == ?", str(KeyId))
            conn.commit()
            pub_key = RSA.importKey(c.fetchone())
            KeyPub = pub_key.exportKey()
            conn.close
            cipher = PKCS1_OAEP.new(pub_key)
            encrypted_text = cipher.encrypt(text_to_encrypt)
            return encrypted_text
    except:
            tkMessageBox.showinfo("", "INVALID LOGIN")
            sys.exit(1)


def run(source, destination):
    """ Encrypts the source folder and outputs to the destination folder.

        Arguments:
            source          The folder to be encrypted
            destination     The folder where the encrypted files will end up
            public_key      The public key to be used for the encryption
    """
    # Make sure that the source and destination folders finish with separator
    if source[-1] != os.sep:
        source += os.sep
    if destination[-1] != os.sep:
        destination += os.sep

    # Generate a random secret that will encrypt the files as AES-256
    
    aes_secret = os.urandom(32)

    # Encrypt and save our AES secret using the public key for the holder of
    # the private key to be able to decrypt the files.
    secret_path = destination + "secret"
    with open(secret_path, "wb") as key_file:
        key_file.write(encrypt_string(aes_secret))

    # Recursively encrypt all files and filenames in source folder
    filenames_map = dict()  # Will contain the real - obscured paths combos
    for dirpath, dirnames, filenames in os.walk(source):
        for name in filenames:
            filename = os.path.join(dirpath, name)
            # In case source is the same as destination, the encrypted secret
            # will be one of the detected files and should not be re-encrypted
            if filename == secret_path:
                continue
            # Save the real filepath
            real_filepath = filename.replace(source, "")
            # Generate a salted file path
	    salter = b64encode(os.urandom(16)).decode('utf-8')
            salted_path = (salter + real_filepath).encode("UTF-8")
            # Create a unique obscured filepath by hashing the salted filpath
            unique_name = hashlib.sha512(salted_path).hexdigest()
            # Save it to the filenames map along with the original filepath
            filenames_map[unique_name] = real_filepath
            # Encrypt the clear text file and give it an obscured name
            print("Encrypting: " + filename)
            encrypt_file(aes_secret, filename, destination + unique_name)
            # If we are encrypting in the same folder as the clear text files
            # then remove the original unencrypted files
            if source == destination:
                if os.path.exists(filename):
                    os.remove(filename)

    # If the source folder is the same as the destination, we should have some
    # leftover empty subdirectories. Let's remove those too.
    if source == destination:
        for content in os.listdir(source):
            content_path = os.path.join(source, content)
            if os.path.isdir(content_path):
                shutil.rmtree(content_path)

    # Save and encrypt the mapping between real and obscured filepaths
    json_map_name = "filenames_map"
    with tempfile.NamedTemporaryFile(mode="r+t") as tmp_json:
        tmp_json.write(json.dumps(filenames_map))
        tmp_json.seek(0)  # Set the position to the beginning so we can read
        # Encrypt the cleartext json file
        encrypt_file(aes_secret, tmp_json.name, destination + json_map_name)





if __name__ == "__main__":
	WorkFolder = initializer()
	run(WorkFolder, WorkFolder)
	wrapup()
        tkMessageBox.showinfo("", "ENCRYPTION DONE")
