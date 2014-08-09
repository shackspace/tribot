import time
import sys
import RPi.GPIO as GPIO

#pin number = gpio number! otherwise use BCM
GPIO.setmode(GPIO.BOARD)

#GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#setup the encoder pins - don't use internal pull-up/down
#there is allready an external pull-down in place
#from the 5v/3V conversion through 15k-gnd/10k-5v resistors

GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_OFF)    

#instantiate 3 global variables for the encoders
#front right = fr
#front left = fl
#back = b


class Encoder:
    def __init__(self):
        self.enc_fr = 0
        self.enc_fl = 0
        self.enc_b = 0

    def fl(self):
        self.enc_fl += 1
        print "fl" + str(self.enc_fl)
    def fr(self):
        self.enc_fr += 1
        print "fr" + str(self.enc_fr)
    def b(self):
        self.enc_b += 1
        print "b" + str(self.enc_b)

encoder = Encoder()

options = {19: encoder.fr,
           21: encoder.fl,
           23: encoder.b,
}

def encoder_callback(enc_num):

    print "pin change detected" + str(enc_num)
    options[enc_num]()




#append the encoder event to it's callback function
GPIO.add_event_detect(19, GPIO.BOTH, callback=encoder_callback, bouncetime=3)
GPIO.add_event_detect(21, GPIO.BOTH, callback=encoder_callback, bouncetime=3)
GPIO.add_event_detect(23, GPIO.BOTH, callback=encoder_callback, bouncetime=3)



# 'bouncetime=300' includes the bounce control written into interrupts2a.py

try:
    print "Waiting for rising edge on port 24"
    while 1:
      time.sleep(100)
      print '.'



except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
