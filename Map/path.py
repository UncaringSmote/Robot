from geopy import distance, Point


class Path:
    grid_size_meters = 5
    points_per_line = 2
    points = []

    def __init__(self, initial_lat_lon, brg):

        self.initial_point = Point(initial_lat_lon)
        self.initial_brn = brg
        self.AddFirstPass()
        self.addTurnAroundPoint()
        self.AddSecondPass()

        self.printPoints()
        self.savePoints()

    def get_points(self):
        return self.points

    def AddFirstPass(self):
        self.calculateFrontAndRight()
        self.line_spacing = self.spacingDistance(self.initial_point, self.side, self.grid_size_meters)
        self.point_spacing = self.spacingDistance(self.initial_point, self.front, self.points_per_line - 1)
        self.createPass()

    def AddSecondPass(self):
        self.initial_point = Point(self.end_point)
        self.initial_brn -= 90
        if self.grid_size_meters % 2 == 0:
            self.calculateFrontAndLeft()
        else:
            self.calculateFrontAndRight()
        self.line_spacing = self.spacingDistance(self.initial_point, self.side, self.grid_size_meters)
        self.point_spacing = self.spacingDistance(self.initial_point, self.front, self.points_per_line - 1)
        self.createPass()

    def calculateFrontAndRight(self):
        self.front = distance.distance(kilometers=self.grid_size_meters / 1000).destination(self.initial_point,
                                                                                            self.initial_brn)
        self.side = distance.distance(kilometers=self.grid_size_meters / 1000).destination(self.initial_point,
                                                                                           self.initial_brn + 90)

    def calculateFrontAndLeft(self):
        self.front = distance.distance(kilometers=self.grid_size_meters / 1000).destination(self.initial_point,
                                                                                            self.initial_brn)
        self.side = distance.distance(kilometers=(self.grid_size_meters) / 1000).destination(self.initial_point,
                                                                                             self.initial_brn - 90)

    def spacingDistance(self, start_point, end_point, divisions):
        lat = (end_point.latitude - start_point.latitude) / (divisions)
        lon = (end_point.longitude - start_point.longitude) / (divisions)
        return Point(lat, lon)

    def createPass(self):
        for i in range(self.grid_size_meters + 1):
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
                self.addTranstionPoints(self.initial_brn + 180 * (i % 2))

    def addTranstionPoints(self, brn):
        self.points.append(distance.distance(kilometers=1 / 1000).destination(self.points[-1], brn))

    def addTurnAroundPoint(self):
        self.end_point = self.points[-1]
        if self.grid_size_meters % 2 == 0:
            turn_brn = self.initial_brn + 45
        else:
            turn_brn = self.initial_brn + 135
        self.points.append(distance.distance(kilometers=1 / 1000).destination(self.points[-1], turn_brn))
        if self.grid_size_meters % 2 == 1:
            self.points.append(distance.distance(kilometers=2 / 1000).destination(self.points[-1], turn_brn - 45))
            self.points.append(distance.distance(kilometers=1 / 1000).destination(self.points[-1], turn_brn - 180))
        else:
            self.points.append(distance.distance(kilometers=2 / 1000).destination(self.points[-1], turn_brn + 45))
            self.points.append(distance.distance(kilometers=1 / 1000).destination(self.points[-1], turn_brn + 180))

    def printPoints(self):
        print("latitude,longitude,name")
        for p, k in enumerate(self.points):
            print(str(k[0]) + "," + str(k[1]) + "," + str(p))

    def savePoints(self):
        f = open("output.txt", "w")
        f.write("QGC WPL 110\n")
        f.write("0	1	0	16	0	0	0	0	" + str(self.points[0][0]) + "	" + str(self.points[0][1]) + "  0.000000	1\n")
        f.write("1	0	3	178	1.00000000	5.00000000	0.00000000	0.00000000	0.00000000	0.00000000	0.000000	1\n")
        for p, k in enumerate(self.points):
             f.write(str(p+2)+"	0	3	16	0.00000000	0.00000000	0.00000000	0.00000000	" +str(k[0]) + "    " + str(k[1]) + "   0.000000	1\n")
        f.close()