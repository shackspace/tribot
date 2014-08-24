#!/usr/bin/env python3

import triweb



print("Initializing motor framework")
from start import mc

print("Initializing kinematics")
from kinematic import Kinematic
kin = Kinematic()

print("Initializing Websocket Framework")
import triweb

def callback(data):
    if data["enable"]==False:
        print("motors off")
        mc.setSpeeds(0, 0, 0)
    else:
        kin.setSpeeds(data)
        kin.getMotorSpeeds()
        print("fr{} fl{} b{}".format(kin.w1,kin.w2,kin.w3))
        mc.setSpeeds(kin.w1, kin.w2, kin.w3)
    data["response"] = True

triweb.startup(callback)





