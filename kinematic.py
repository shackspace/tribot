#!/usr/bin/env python3


#Ansteuerung von omniwheels
import math

class Kinematic:
    def __init__(self):
        self.xSpeed = 0
        self.ySpeed = 0
        self.thetaSpeed = 0
        self.distanceToWheel = 0.88888888 #m
        self.sinPiThird = math.sin(math.pi / 3)
        self.cosPiThird = math.cos(math.pi/ 3)
        self.w1 = 0
        self.w2 = 0
        self.w3 = 0
    def setSpeeds(self, data):
        self.xSpeed = math.cos(data["direction"])*data["speed"]
        self.ySpeed = math.sin(data["direction"])*data["speed"]
        self.thetaSpeed = data["rotation"]
    def getMotorSpeeds(self):
        """
        Eigentliche Formel ist:
            w1 = sin(theta)*xSpeed + cos(theta) * ySpeed +  thetaSpeed * L
            w2 = -sin(Pi/3 -theta)*xSpeed - cos(Pi/3 - theta) * ySpeed +  thetaSpeed * L
            w3 = sin(Pi/3  + theta)*xSpeed - cos(Pi/3 + theta) * ySpeed +  thetaSpeed * L

        Da wir allerdings (vorerst) keinen Startwinkel brauchen können wir theta = 0 setzen
            w1 =                                   ySpeed +  thetaSpeed * L
            w2 = -sin(Pi/3) * xSpeed - cos(Pi/3) * ySpeed +  thetaSpeed * L
            w3 =  sin(Pi/3) * xSpeed - cos(Pi/3) * ySpeed +  thetaSpeed * L
        """
        self.w1 =  self.ySpeed + self.thetaSpeed * self.distanceToWheel
        self.w2 = -self.sinPiThird * self.xSpeed - self.cosPiThird * self.ySpeed + self.thetaSpeed * self.distanceToWheel 
        self.w3 =  self.sinPiThird * self.xSpeed - self.cosPiThird * self.ySpeed + self.thetaSpeed * self.distanceToWheel
def runTests():
    data = {}
    failedtests = 0
    data["speed"] = 0
    data["direction"] = 0
    data["rotation"] = 0
    kin = Kinematic()
    kin.setSpeeds(data)
    kin.getMotorSpeeds()
    if kin.w1 != 0 or kin.w2 != 0 or kin.w3 != 0:
        print("Inittest failed all motor speeds should be 0")
        failedtests += 1
    data["rotation"] = 1
    kin.setSpeeds(data)
    kin.getMotorSpeeds()
    lower = kin.distanceToWheel - 0.001
    higher = kin.distanceToWheel + 0.001
    if not (lower < kin.w1 - higher  or lower < kin.w2 < higher or lower < kin.w3 < higher):
        print("Rotatiiontest failed all motor speeds should be 0.8")
        print("\tgot values "+ str(kin.w1)+ ", "+ str(kin.w2)+ ", " + str(kin.w3))
        failedtests += 1
    data["rotation"] = 0
    data["direction"] = 0
    data["speed"] = 1
    kin.setSpeeds(data)
    kin.getMotorSpeeds()
    sollw1 = 0.0
    sollw2 = -0.866025
    sollw3 = 0.866025
    uw1 = sollw1 - 0.0001
    ow1 = sollw1 + 0.0001
    uw2 = sollw2 - 0.0001
    ow2 = sollw2 + 0.0001
    uw3 = sollw3 - 0.0001
    ow3 = sollw3 + 0.0001
    if not ((uw1 < kin.w1 < ow1) or ( uw2 < kin.w2 < ow2) or  ( uw3 <  kin.w3 < ow3 )):
        print("Rotationtest Failed expected values: {}, {}, {}".format(sollw1, sollw2, sollw3))
        print("\tgot values "+ str(kin.w1)+ ", "+ str(kin.w2)+ ", " + str(kin.w3))
        failedtests += 1
    data["rotation"] = 0
    data["direction"] = math.pi
    data["speed"] = 1
    kin.setSpeeds(data)
    kin.getMotorSpeeds()
    sollw1 = 0.0
    sollw2 = 0.866025
    sollw3 = -0.866025
    uw1 = sollw1 - 0.0001
    ow1 = sollw1 + 0.0001
    uw2 = sollw2 - 0.0001
    ow2 = sollw2 + 0.0001
    uw3 = sollw3 - 0.0001
    ow3 = sollw3 + 0.0001
    if not ((uw1 < kin.w1 < ow1) or ( uw2 < kin.w2 < ow2) or  ( uw3 <  kin.w3 < ow3 )):
        print("Rotationtest Failed expected values: {}, {}, {}".format(sollw1, sollw2, sollw3))
        print("\tgot values "+ str(kin.w1)+ ", "+ str(kin.w2)+ ", " + str(kin.w3))
        failedtests += 1
    

    if failedtests > 0:
        print("{} tests failed".format(failedtests))
    else:
        print("all tests passed ;-)")


if __name__ == '__main__':
    runTests()
