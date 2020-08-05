class DistanceTable:
    def __init__(self):
        self.points = {}
        self.distances = {}

    def add_location(self, new_location):
        self.points[new_location] = []

    def add_distance(self, point_a, point_b, distance):
        self.distances[(point_a, point_b)] = distance
        self.points[point_a].append(point_b)
        self.distances[(point_b, point_a)] = distance
        self.points[point_b].append(point_a)

    def get_location(self, label):
        for x in self.points:
            if x.label == label:
                return x
        return None

    def get_distance(self, from_point, to_point):
        if from_point is None or to_point is None:
            return 0
        elif from_point is to_point:
            return 0
        else:
            distance = self.distances.get((from_point, to_point))
            return distance

    def print_table(self):
        for location in self.points:
            print(f'{location.label}')
