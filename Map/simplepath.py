from geopy import distance, Point

class SimplePath:
    box_distance_meters = 20.0
    start_distance_meters = 10.0

    points = []

    def get_points(self):
        return self.points

    def __init__(self, initial_lat_lon, brg):

        self.current_point = Point(initial_lat_lon)
        self.initial_brn = brg
        self.calculate_next_point(self.start_distance_meters,0)
        self.calculate_next_point(self.box_distance_meters, 0)
        self.calculate_next_point(self.box_distance_meters,90)
        self.calculate_next_point(self.box_distance_meters, 180)
        self.calculate_next_point(self.box_distance_meters, 270)
        self.print_points()

    def calculate_next_point(self,offset,angle):
        self.current_point = distance.distance(kilometers=offset / 1000.).destination(self.current_point,
                                                                                         self.initial_brn+angle)
        self.points.append(self.current_point)


    def spacing_distance(self, start_point, end_point, divisions):
        lat = (end_point.latitude - start_point.latitude) / (divisions)
        lon = (end_point.longitude - start_point.longitude) / (divisions)
        return Point(lat, lon)

    def print_points(self):
        print("latitude,longitude,name")
        for p, k in enumerate(self.points):
            print(str(k[0]) + "," + str(k[1]) + "," + str(p))

if __name__ == '__main__':
    blah = SimplePath(Point(30.518341,-84.249066),45)

