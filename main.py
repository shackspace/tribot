#!/usr/bin/env python3

from start import mc
import triweb
from kinematic import Kinematic


print("Initializing motor framework")




print("Initializing kinematics")
print("Initializing Websocket Framework")

def callback(data):
    kin.setSpeeds(data)
    kin.getMotorSpeeds()
    print("fr{} fl{} b{}".format(kin.w1,kin.w2,kin.w3))
    data["response"] = True

triweb.startup(callback)





