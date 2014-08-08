import time
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

#GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

print "test"

def encoder_callback(enc_num):
    print "falling edge detected on" + str(enc_num)

GPIO.add_event_detect(19, GPIO.RISING, callback=encoder_callback, bouncetime=300)
GPIO.add_event_detect(21, GPIO.RISING, callback=encoder_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.RISING, callback=encoder_callback, bouncetime=300)


# 'bouncetime=300' includes the bounce control written into interrupts2a.py

try:
    print "Waiting for rising edge on port 24"
    while 1:
      time.sleep(100)
      print '.'



except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
