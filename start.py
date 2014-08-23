#!/usr/bin/env python3

import time
import sys
import RPi.GPIO as GPIO
import RPIO

import http.server
from http.server import SimpleHTTPRequestHandler

class LightsHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print("ola: " + self.path)
        if ("ledon" in self.path):
            self.statusled_on()
        elif ("ledoff" in self.path):
            self.statusled_off()
        elif ("move" in self.path):
            if("move0" in self.path):
                mc.move(0, 25)
                time.sleep(1)
                mc.move(0, 0)

            elif("move1" in self.path):
                mc.move(60, 25)
                time.sleep(1)
                mc.move(60, 0)

            elif("move2" in self.path):
                mc.move(120, 25)
                time.sleep(1)
                mc.move(120, 0)

            elif("move3" in self.path):
                mc.move(180, 25)
                time.sleep(1)
                mc.move(180, 0)

            elif("move4" in self.path):
                mc.move(240, 25)
                time.sleep(1)
                mc.move(240, 0)

            elif("move5" in self.path):
                mc.move(300, 25)
                time.sleep(1)
                mc.move(300, 0)

            elif("movel" in self.path):
                mc.rotate(-1, 25)
                time.sleep(1)
                mc.rotate(-1, 0)

            elif("mover" in self.path):
                mc.rotate(1, 25)
                time.sleep(1)
                mc.rotate(1, 0)


        self.wfile.write(b"""<!DOCTYPE html><body>Hello</br>
                      <a href="move0">0</a></br>
                      <a href="move1">1</a></br>
                      <a href="move2">2</a></br>
                      <a href="move3">3</a></br>
                      <a href="move4">4</a></br>
                      <a href="move5">5</a></br>
                      <a href="movel">l</a></br>
                      <a href="mover">r</a></br>
                      World !</body></html>""")
        return

    def statusled_on(self):
        GPIO.output(22, True)
        print("becoming active")
    def statusled_off(self):
        print("going offline")
        GPIO.output(22, False)

#Encoder class
class Encoder:
    def __init__(self, encoderGPIO):
        #encoder GPIO
        self.encoderGPIO = encoderGPIO

        #setup the encoder pins - don't use internal pull-up/down
        #there is allready an external pull-down in place
        #from the 5v/3V conversion through 15k-gnd/10k-5v resistors

       # RPIO.setup(self.encoderGPIO, RPIO.IN)

        #append the encoder event to it's callback function
        
        # workaround 
        new_gpio= RPIO.channel_to_gpio(self.encoderGPIO)
        RPIO.setmode(RPIO.BCM)
        RPIO.setup(new_gpio, RPIO.IN)
        RPIO.add_interrupt_callback(new_gpio, callback=self.encoder_callback, edge='both',pull_up_down=RPIO.PUD_OFF, debounce_timeout_ms=2,threaded_callback=True)
        RPIO.setmode(RPIO.BOARD)

        #counter variable
        self.encoder_count = 0

        #which direction (-1=cw/1=ccw)
        self.direction = 1

 #   def __exit__(self, type, value, traceback):
#        GPIO.remove_event_detect(self.encoderGPIO)

    #the callback function for the encoders
    def encoder_callback(self, GPIO,value):

        print("pin change detected: " + str(self.encoderGPIO))
        #python "switch case" (lookup) to change the right counter variable
        self.count()

    def count(self):
        self.encoder_count += self.direction
        print("pin: " + str(self.encoderGPIO) + " count: " + str(self.encoder_count))

    def set_direction(self, direction):
            self.direction = direction

#Motor class
class Motor:
    def __init__(self, motorEnableGPIO, motorSpeedGPIO, encoderGPIO):
        #Enable motor pin
        self.motorEnabledGPIO = motorEnableGPIO
        self.motorSpeedGPIO = motorSpeedGPIO
        self.encoderGPIO = encoderGPIO

        self.encoder = Encoder(self.encoderGPIO)


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

        #print "Speed: " + str(speed)

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
        self.sin120 = 0.866025
        self.sinm120 = -0.866025
        self.cos120 =  -0.5
        self.cosm120 = -0.5


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
        else:
            self.motor_fl.set_speed(0)
            self.motor_fr.set_speed(0)
            self.motor_b.set_speed(0)

    def go(self, vx, vy, angle):
        self.vb = round(vx + angle)
        self.motor_b.set_speed(self.vb)
        self.vfr = round(vx * self.cos120 - vy * self.sin120 + angle)
        self.motor_fr.set_speed(self.vfr)
        self.vfl = round(vx * self.cosm120 - vy * self.sinm120 + angle)
        self.motor_fl.set_speed(self.vfl)

        print("%d %s %d %s %d %s" %(self.vb, "vb", self.vfr, "vfr", self.vfl, "vfr"))

        time.sleep(2)
        self.motor_b.set_speed(0)
        self.motor_fr.set_speed(0)
        self.motor_fl.set_speed(0)
        print("stopped")

    def rotate(self, direction, speed):
        if direction == 1 or direction == "ccw":
            self.motor_fr.set_speed(speed)
            self.motor_fl.set_speed(speed)
            self.motor_b.set_speed(speed)
        elif direction == -1 or direction == "cw":
            self.motor_fr.set_speed(-speed)
            self.motor_fl.set_speed(-speed)
            self.motor_b.set_speed(-speed)
        else:
            self.motor_fr.set_speed(0)
            self.motor_fr.set_speed(0)
            self.motor_b.set_speed(0)

    def setSpeeds(fr, fl, b):
        self.motor_fr.set_speed(fr)
        self.motor_fl.set_speed(fl)
        self.motor_b.set_speed(b)
#pin number = gpio number! otherwise use BCM
GPIO.setmode(GPIO.BOARD)
RPIO.setmode(RPIO.BOARD)
mc = MotionController()

def main():


    HandlerClass = LightsHandler
    ServerClass=http.server.HTTPServer
    Protocol="HTTP/1.0"

    server_address= ("", 8080)

    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print("serving")

    GPIO.setup(22, GPIO.OUT)
    RPIO.wait_for_interrupts(threaded=True, epoll_timeout=1)
    httpd.serve_forever()

    

    # 'bouncetime=300' includes the bounce control written into interrupts2a.py

    try:
        while 1:
            print('.')

    #        for i in range (-1, 2, 2):
    #           mc.rotate(i,25)
    #          time.sleep(3)

    #     for i in range(0,301,60):
        #        mc.move(i, 25)
        #       time.sleep(3)
            time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit


    GPIO.cleanup()           # clean up GPIO on normal exit

if __name__ == '__main__':
    main()

