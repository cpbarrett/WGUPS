from location import Location


class DistanceTable:
    def __init__(self):
        self.points = {}
        self.distances = {}

    def add_location(self, new_location):
        self.points[new_location] = []

    def add_directed_edge(self, from_point, to_point, weight=1):
        self.distances[(from_point, to_point)] = weight
        if to_point not in self.points[from_point]:
            self.points[from_point].append(to_point)

    def add_distance(self, point_a, point_b, distance):
        self.add_directed_edge(point_a, point_b, distance)
        self.add_directed_edge(point_b, point_a, distance)

    def get_location(self, label):
        for x in self.points:
            if x.label == label:
                return x
        return None

    def print_table(self):
        for location in self.points:
            print(f'{location.label}')
