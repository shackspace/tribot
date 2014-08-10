import time
import sys
import RPi.GPIO as GPIO

#pin number = gpio number! otherwise use BCM
GPIO.setmode(GPIO.BOARD)

#Encoder class
class Encoder:
    def __init__(self, encoderGPIO):
        #encoder GPIO
        self.encoderGPIO = encoderGPIO

        #setup the encoder pins - don't use internal pull-up/down
        #there is allready an external pull-down in place
        #from the 5v/3V conversion through 15k-gnd/10k-5v resistors

        GPIO.setup(self.encoderGPIO, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        #append the encoder event to it's callback function
        GPIO.add_event_detect(self.encoderGPIO, GPIO.BOTH, callback=self.encoder_callback, bouncetime=2)

        #counter variable
        self.encoder_count = 0

        #which direction (-1=cw/1=ccw)
        self.direction = 1

    #the callback function for the encoders
    def encoder_callback(self, GPIO):

        print "pin change detected: " + str(self.encoderGPIO)
        #python "switch case" (lookup) to change the right counter variable
        self.count()

    def count(self):
        self.encoder_count += self.direction
        print "pin: " + str(self.encoderGPIO) + " count: " + str(self.encoder_count)

    def set_direction(self, direction):
            self.direction = direction

#Motor class
class Motor:
    def __init__(self, motorEnableGPIO, motorSpeedGPIO, encoderGPIO):
        #Enable motor pin
        self.motorEnabledGPIO = motorEnableGPIO
        self.motorSpeedGPIO = motorSpeedGPIO
        self.encoderGPIO = encoderGPIO

        #self.encoder = Encoder(self.encoderGPIO)


        GPIO.setup(motorEnableGPIO, GPIO.OUT, initial=GPIO.LOW)

        #motor speed pins (PWM [full_cw ... off ... full_ccw] [0 ... 50 ... 100]
        GPIO.setup(motorSpeedGPIO, GPIO.OUT)

        #setup PWM 50Hz?
        self.motorSpeedPWM = GPIO.PWM(motorSpeedGPIO, 50)

        #counter variable
        self.enabled = False

        #which direction (1=cw/2=ccw)
        self.direction = 1

    def __exit__(self, type, value, traceback):
        self.motorSpeedPWM.stop()

    def set_speed(self, speed):
        #motor direction pins (PWM [full_cw ... off ... full_ccw] [0 ... [35-65] ... 100]
        if speed > -15 and speed < 15:
            self.set_enabled(False)
            self.motorSpeedPWM.stop()
            return
        else:
            self.set_enabled(True)

        #set encoder direction
       # if speed < 0:
       #     self.encoder.set_direction(-1)
       # else:
       #     self.encoder.set_direction(1)

        #adjust for [0-100] duty cycle
        self.motorSpeedPWM.start(speed + 50)



        print "Speed: " + str(speed)

    def set_enabled(self, enable):
        if enable == True:
            GPIO.output(self.motorEnabledGPIO, GPIO.HIGH)
        else:
            GPIO.output(self.motorEnabledGPIO, GPIO.LOW)


class MotionController():
    def __init__(self):
        self.motor_fl = Motor(7, 15, 19)
        self.motor_fr = Motor(11, 16, 21)
        self.motor_b = Motor(13, 18, 23)
        self.motor_fl.set_speed(0)
        self.motor_fr.set_speed(0)
        self.motor_b.set_speed(0)



    def move(self, direction, speed):
        self.direction = direction
        self.speed = speed

        if self.direction == 0:
            self.motor_fl.set_speed(-self.speed)
            self.motor_fr.set_speed(self.speed)
            self.motor_b.set_speed(0)
        elif self.direction == 60:
            self.motor_fl.set_speed(0)
            self.motor_fr.set_speed(self.speed)
            self.motor_b.set_speed(-self.speed)
        elif self.direction == 120:
            self.motor_fl.set_speed(self.speed)
            self.motor_fr.set_speed(0)
            self.motor_b.set_speed(-self.speed)
        elif self.direction == 180:
            self.motor_fl.set_speed(self.speed)
            self.motor_fr.set_speed(-self.speed)
            self.motor_b.set_speed(0)
        elif self.direction == 240:
            self.motor_fl.set_speed(0)
            self.motor_fr.set_speed(-self.speed)
            self.motor_b.set_speed(self.speed)
        elif self.direction == 300:
            self.motor_fl.set_speed(-self.speed)
            self.motor_fr.set_speed(0)
            self.motor_b.set_speed(self.speed)
 #       else:
  #          self.motor_fl.set_speed(0)
   #         self.motor_fr.set_speed(0)
    #        self.motor_b.set_speed(0)


mc = MotionController()

mc.move(0, 25)

time.sleep(3)

mc.move(60, 25)

time.sleep(3)

mc.move(120, 25)

time.sleep(3)

mc.move(180, 25)

time.sleep(3)

mc.move(240, 25)

time.sleep(3)

mc.move(300, 25)




# 'bouncetime=300' includes the bounce control written into interrupts2a.py

try:
    print "Waiting for rising edge on port 24"
    while 1:
      time.sleep(1)
      print '.'



except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit

GPIO.cleanup()           # clean up GPIO on normal exit
