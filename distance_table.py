"""
This graph class represents the data from the WGUPS_Distance_Table.csv
"""
from location import Location


class DistanceTable:
    """
    DistanceTable uses 2 dictionaries to represent adjacency list and edge weights.
    Big-O is as follows:
    add_location: O(1)
    add_distance: O(1)
    get_location: O(N)
    get_distance: O(1)
    print_table: O(N)
    """
    def __init__(self):
        """
        Adjacency List: points
        Edge Weights: distances
        """
        self.points = {}
        self.distances = {}

    def add_location(self, new_location: Location):
        """
        add a new location to the graph that points to an empty list for future adjacent locations
        :param new_location: the Location to be added
        :return: None
        """
        self.points[new_location] = []

    def add_distance(self, point_a: Location, point_b: Location, distance: float):
        """
        set point a and b as adjacent locations in the graph
        add the distance as a new item in the distances dictionary
        :param point_a: Location
        :param point_b: Location
        :param distance: int
        :return: None
        """
        self.distances[(point_a, point_b)] = distance
        self.points[point_a].append(point_b)
        self.distances[(point_b, point_a)] = distance
        self.points[point_b].append(point_a)

    def get_location(self, label: str):
        """
        iterate over the locations in points and return the location with a matching label if found
        :param label: str
        :return: Location with matching label or None if not found
        """
        for location in self.points:
            if location.label == label:
                return location
        return None

    def get_distance(self, from_point: Location, to_point: Location):
        """

        :param from_point: Location
        :param to_point: Location
        :return: int
        """
        if from_point is None or to_point is None:
            return 0
        if from_point is to_point:
            return 0
        distance = self.distances.get((from_point, to_point))
        return distance

    def print_table(self):
        """
        prints out a list of all the labels contained in the graph
        :return: None
        """
        for location in self.points:
            print(f'{location.label}')
