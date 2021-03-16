from dronekit import connect, VehicleMode, Command
import time
from path import Path
from pymavlink import mavutil

class Robot:

    def __init__(self):
        pass

    def connect(self):
        self.vehicle = connect('replaceme', wait_ready=True)

    def start_mission(self, delay=3):
        self.connect()
        time.sleep(delay)
        if self.vehicle.mode.name == 'AUTO':
            self.vehicle.mode = VehicleMode("MANUAL")
            return

        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        print("Arming motors")
        self.vehicle.armed = True

        while not self.vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        self.vehicle.commands.next = 0
        # Set mode to AUTO to start mission
        self.vehicle.mode = VehicleMode("AUTO")
        self.close_connection()

    def close_connection(self):
        self.vehicle.close()

    def load_waypoints(self):
        self.connect()
        lat = self.vehicle.location.global_relative_frame.lat
        lon = self.vehicle.location.global_relative_frame.lon
        brn = self.vehicle.heading
        path = Path((lat,lon), brn)
        points = path.get_points()
        msg = self.vehicle.message_factory.command_long_encode(
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_CMD_DO_SET_HOME, #command
            0, #confirmation
            1,    # param 1, 1=use current
            0,          # param 2,
            0,          # param 3
            0,          # param 4,
            lat, lon, 100)    # param 5 ~ 7 lat,lon,alt
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()

        cmds = self.vehicle.commands

        print(" Clear any existing commands")
        cmds.clear()
        cmds.upload()

        for point in points:
            cmds.add(
                Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,0,
                        0, 0, 0, 0, point[0], point[1], 0))
        cmds.upload()

        self.close_connection()
