'''
Created on 08/04/2014

@author: jeanmachuca

SAMPLE CODE:

This script is a test for device connected to GPIO port in raspberry pi

For test purpose:

Step 1:
Connect the TX pin of the fingerprint GT511C3 to RX in the GPIO

Step 2:
Connect the RX pin of the fingerprint GT511C3 to TX in the GPIO

Step 3:
Connect the VCC pin of the fingerprint GTC511C3 to VCC 3,3 in GPIO

Step 4:
Connect the Ground pin of fingerprint GT511C3 to ground pin in GPIO


This may be works fine, if don't, try to change the fingerprint baud rate with baud_to_115200.py sample code


'''
from socketIO_client import SocketIO
import FPS, sys
DEVICE_GPIO = '/dev/ttyAMA0'
# DEVICE_LINUX = '/dev/cu.usbserial-A601EQ14'
# DEVICE_MAC = '/dev/cu.usbserial-A601EQ14'
# DEVICE_WINDOWS = 'COM3'
FPS.BAUD = 9600
FPS.DEVICE_NAME = DEVICE_GPIO

def on_connect():
    print('connect')

def on_disconnect():
    print('disconnect')

def on_fps_com_response(*args):
    print('on_fps_com_response', args)
    # print(type(args))
    # print(args['msg'])
    # x = args[0]

    # if x['hello'] == "Hey there!":
    #     print ('yo')

def waitUntilPress(fps):
    while fps.IsPressFinger() == False:
        FPS.delay(FPS.INTERVAL+0.03)

def waitUntilRelease(fps):
    while fps.IsPressFinger() == True:
        FPS.delay(FPS.INTERVAL+0.03)

def identifyprotocol(fps):
    waitUntilPress(fps)
    if fps.CaptureFinger(True):
        return fps.Identify1_N()
    else:
        return 'fail'

def printEnroll():
    enrollid=0
    okid=True
    #search for a free enrollid, you have max 200
    while enrollid < 200:
        okid = fps.CheckEnrolled(enrollid)
        print okid
        enrollid+=1

def LegacyEnroll(fps):
    '''
    Enroll test
    '''
    fps.SetLED(False) # Turns OFF the CMOS LED
    enrollid=0
    okid=True
    msg='string'
    #search for a free enrollid, you have max 200
    while okid == True and enrollid < 200:
        okid = fps.CheckEnrolled(enrollid)
        print okid
        if okid == True:
            enrollid+=1
    fps.SetLED(True) # Turns ON the CMOS LED
    if enrollid <200:
        #press finger to Enroll enrollid
        print 'Press finger to Enroll %s' % str(enrollid)
        # msg = 'Press finger to Enroll ID: %s' % str(enrollid)
        # socketIO.emit('fps_com', msg)
        fps.EnrollStart(enrollid)
        waitUntilPress(fps)
        iret = 0
        if fps.CaptureFinger(True):
            #remove finger
            print 'remove finger'
            # msg = 'remove finger'
            # socketIO.emit('fps_com', msg)
            fps.Enroll1()
            waitUntilRelease(fps)
            #Press same finger again
            print 'Press same finger again'
            # msg = 'Press finger for the second time'
            # socketIO.emit('fps_com', msg)
            waitUntilPress(fps)
            if fps.CaptureFinger(True):
                #remove finger
                print 'remove finger'
                # msg = 'remove finger'
                # socketIO.emit('fps_com', msg)
                fps.Enroll2()
                waitUntilRelease(fps)
                #Press same finger again
                print 'press same finger yet again'
                # msg = 'final press'
                # socketIO.emit('fps_com', msg)
                waitUntilPress(fps)
                if fps.CaptureFinger(True):
                    #remove finger
                    iret = fps.Enroll3()
                    if iret == 0:
                        print 'Enrolling Successfull'
                        # msg = {msg:'Enrolling Successfull',data:enrollid}
                        # socketIO.emit('fps_com', msg)
                    else:
                        print 'Enrolling Failed with error code: %s' % str(iret)
                        # if(iret == 3):
                            # msg = 'Failed : Found duplicate finger'
                            # socketIO.emit('fps_com', msg)
                        # else:
                            # msg = 'Failed with error code: %s' % str(iret)
                            # socketIO.emit('fps_com', msg)
                else:
                    print 'Failed to capture third finger'
                    # msg = 'Failed to capture third finger'
                    # socketIO.emit('fps_com', msg)
            else:
                print 'Failed to capture second finger'
                # msg = 'Failed to capture second finger'
                # socketIO.emit('fps_com', msg)
        else:
            print 'Failed to capture first finger'
            # msg = 'Failed to capture first finger'
            # socketIO.emit('fps_com', msg)
    else:
        print 'Failed: enroll storage is full'
        # msg = 'Failed: enroll storage is full'
        # socketIO.emit('fps_com', msg)


if __name__ == '__main__':
    fps =  FPS.FPS_GT511C3(device_name=DEVICE_GPIO,baud=9600,timeout=2,is_com=False)
    fps.UseSerialDebug = False
    # fps.UseSerialDebug = True

    fps.SetLED(False) # Turns ON the CMOS LED
    FPS.delay(5) # wait 1 second for initialize finish

    # socketIO = SocketIO('http://192.168.1.37', 8080, verify=False)
    # socketIO.on('connect', on_connect)
    # socketIO.on('fps_com', on_fps_com_response)
    # socketIO.emit('fps_com', 'FPS >>> standby')
    # socketIO.wait(0.5)
    # while True:
    #     waitUntilPress(fps)
    #     idenid = identifyprotocol(fps)
    #     print 'lift the finger'
    #     socketIO.on('fps_com', on_fps_com_response)
    #     socketIO.emit('fps_com', idenid)
    #     socketIO.wait(0.5)
    #     fps.SetLED(False) # Turns OFF the CMOS LED
    #     FPS.delay(0.1) # wait 1 second for initialize finish
    #     fps.SetLED(True) # Turns ON the CMOS LED
    #     waitUntilRelease(fps)


    # LegacyEnroll(fps)
    # print 'Identify'
    # FPS.delay(1)
    # print identifyprotocol(fps)
    # printEnroll()


    printEnroll()
    deleteID = int(raw_input("ID : "))
    fps.DeleteID(deleteID)

    # fps.DeleteAll()
    #fps.SetLED(False) # Turns CLOSE the CMOS LED

    # fps.Close() # Closes serial connection
    pass
