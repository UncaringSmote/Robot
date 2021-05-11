

class Waypoint:
    LINE = 1
    END = 2
    TURNAROUND = 3

    def __init__(self,point,waypoint_type):
        self.point = point
        self.waypoint_type = waypoint_type

