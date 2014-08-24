tribot
======
Controlling a robot with the raspberry Pi

Description
===========

This is a Framework that enables a omniwheel robot to be controlled with a Raspberry Pi. It was hacked to work with the omni oheel robot "tri-bot" from wowee.
There are serveral parts for this programm.

Files:
main.py start programm that calls all components that are needed to run this application
kinetics.py this library implements the foreward kinematics for a Omni-wheel robot
triweb.py provides a websocket interface
server.py will serve the html files for the web user interface
start.py the motorcontroller for the robot

TODO
====

The file start.py needs to be splitted into the files motor.py, enocoders.py and motorcontrol.py to enable the replacement of a motor controller
The inteface needs to be defined.
The the programm crashes after serveral minutes of usage
Lookup
======
http://www.uni-ulm.de/fileadmin/website_uni_ulm/iui.inst.130/Arbeitsgruppen/Robotics/Robotik/Robotik-Skript_07-08.pdf



