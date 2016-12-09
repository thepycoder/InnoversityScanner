#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import datetime
import time
from websocket import create_connection

continue_reading = True
try:
    ws = create_connection("ws://192.168.0.173:5000")
except:
    "Unable to connect to remote server"

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    try:
        ws.close()
    except:
        pass
    GPIO.cleanup()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 11
GPIO.setup(led, GPIO.OUT)

print "Searching for an ID card now..."

# Holds the last scanned card
last = ['', datetime.datetime.now()]

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Enable LED
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(led, GPIO.LOW)

        UID = format(uid[0], '02x') + format(uid[1], '02x') + format(uid[2], '02x') + format(uid[3], '02x')

        # Calculate timedifference since last scan
        td = datetime.datetime.now() - last[1]

        # Check if scanned already or was scanned in the last 10 seconds
        if UID not in last or (UID in last and td.seconds > 10):
            print "Card read UID: " + UID
            last = [UID, datetime.datetime.now()]
            try:
                ws.send(UID)
            except:
                pass