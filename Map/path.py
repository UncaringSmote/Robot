from geopy import distance, Point


class Path:
    grid_size_meters = 5
    points_per_line = 2
    points = []

    def __init__(self, initial_lat_lon, brg):
        self.initial_point = Point(initial_lat_lon)
        self.initial_brn = brg
        self.add_first_pass()
        self.add_turn_around_point()
        self.add_second_pass()
        self.print_points()

    def get_points(self):
        return self.points

    def add_first_pass(self):
        self.calculate_front_and_right()
        self.line_spacing = self.spacing_distance(self.initial_point, self.side, self.grid_size_meters)
        self.point_spacing = self.spacing_distance(self.initial_point, self.front, self.points_per_line - 1)
        self.create_pass()

    def add_second_pass(self):
        self.initial_point = Point(self.end_point)
        self.initial_brn -= 90
        if self.grid_size_meters % 2 == 0:
            self.calculate_front_and_left()
        else:
            self.calculate_front_and_right()
        self.line_spacing = self.spacing_distance(self.initial_point, self.side, self.grid_size_meters)
        self.point_spacing = self.spacing_distance(self.initial_point, self.front, self.points_per_line - 1)
        self.create_pass()



    def calculate_front_and_right(self):
        self.front = distance.distance(kilometers=self.grid_size_meters / 1000).destination(self.initial_point,
                                                                                            self.initial_brn)
        self.side = distance.distance(kilometers=self.grid_size_meters / 1000).destination(self.initial_point,
                                                                                           self.initial_brn + 90)

    def calculate_front_and_left(self):
        self.front = distance.distance(kilometers=self.grid_size_meters / 1000).destination(self.initial_point,
                                                                                            self.initial_brn)
        self.side = distance.distance(kilometers=self.grid_size_meters / 1000).destination(self.initial_point,
                                                                                           self.initial_brn - 90)

    def spacing_distance(self, start_point, end_point, divisions):
        lat = (end_point.latitude - start_point.latitude) / (divisions)
        lon = (end_point.longitude - start_point.longitude) / (divisions)
        return Point(lat, lon)

    def create_pass(self):
        for i in range(self.grid_size_meters+1):
            for j in range(self.points_per_line):
                if i % 2 == 0:
                    self.points.append(
                        (self.initial_point.latitude + j * self.point_spacing.latitude + i * self.line_spacing.latitude,
                         self.initial_point.longitude + j * self.point_spacing.longitude + i * self.line_spacing.longitude))
                else:
                    self.points.append(
                        (self.front.latitude - j * self.point_spacing.latitude + i * self.line_spacing.latitude,
                         self.front.longitude - j * self.point_spacing.longitude + i * self.line_spacing.longitude))
            if i != self.grid_size_meters:
                self.add_transtion_points(self.initial_brn + 180 * (i % 2))

    def add_transtion_points(self, brn):
        self.points.append(distance.distance(kilometers=1 / 1000).destination(self.points[-1], brn))

    def add_turn_around_point(self):
        self.end_point = self.points[-1]
        if self.grid_size_meters%2==0:
            turn_brn = self.initial_brn+45
        else:
            turn_brn = self.initial_brn + 135
        self.points.append(distance.distance(kilometers=1 / 1000).destination(self.points[-1], turn_brn))
        self.points.append(distance.distance(kilometers=2 / 1000).destination(self.points[-1], turn_brn-45))
        self.points.append(distance.distance(kilometers=1 / 1000).destination(self.points[-1], turn_brn-180))

    def print_points(self):
        print("latitude,longitude,name")
        for p, k in enumerate(self.points):
            print(str(k[0]) + "," + str(k[1]) + "," + str(p))
