#!/usr/bin/python
from gpiozero import Button,Buzzer
from signal import pause
from robot import Robot
import syslog

class RPi:
    def __init__(self):
        self.load_waypoints_button = Button(27)
        self.start_mission_button = Button(17)
        self.load_waypoints_button.when_pressed = self.load_waypoints
        self.start_mission_button.when_pressed = self.start_mission
        self.robot = Robot()
        self.bz = Buzzer(26)

    def start_mission(self):
        self.bz.beep(on_time=1,n=1)
        print('start mission')
        syslog.syslog('start mission')
        self.robot.start_mission()
        self.bz.beep(on_time=1,off_time=1,n=2)

    def load_waypoints(self):
        self.bz.beep(on_time=1,n=1)
        print('load waypoints')
        syslog.syslog('load waypoints')
        self.robot.load_waypoints()
        self.bz.beep(on_time=1,off_time=1,n=2)

def main():
    syslog.syslog('started')
    print('started')
    RPi()
    pause()

if __name__ == "__main__":
    main()


