from gpiozero import Button
from signal import pause
from robot import Robot

class RPi:
    def __init__(self):
        self.load_waypoints_button = Button(27,bounce_time=5)
        self.start_mission_button = Button(17,bounce_time=5)
        self.load_waypoints_button.when_pressed = self.load_waypoints
        self.start_mission_button.when_pressed = self.start_mission
        self.robot = Robot()

    def start_mission(self):
        print("start mission")
        self.robot.start_mission()

    def load_waypoints(self):
        print("load waypoints")
        self.robot.load_waypoints()

def main():
    RPi()
    pause()

if __name__ == "__main__":
    main()
