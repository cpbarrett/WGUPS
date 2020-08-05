"""
The Hub class loads all the data from the csv files, creates the package hash table,
 and creates the graph containing all the delivery locations.
"""
import csv

import distance_table
from location import Location
from hash_table import HashTable
from truck import Truck


class Hub:
    """
    Class constructor takes in the number of trucks and an optional opening time.
    The hub location is also created for use elsewhere.
    """

    def __init__(self, truck_count=1, opening_time="08:00 AM"):
        print("Welcome to Hub Management Center")
        self.opening_time = opening_time
        self.truck_count = truck_count
        self.trucks = []
        self.add_truck(truck_count)
        self.center = Location("Western Governors University", "4001 South 700 East",
                               "Salt Lake City", "UT", "84107", "HUB")
        self.destinations = distance_table.DistanceTable()
        self.database = HashTable()
        self.load_locations()
        self.load_packages()

    def truck_mileage(self, truck):
        """

        :param truck:
        :return:
        """
        stops = self.route_truck(truck)
        miles = 0.0
        route = []
        for i in truck.cargo.values():
            if isinstance(i, Location) is False:
                continue
            pkg = self.database.look_up(i)
            pkg.delivery_status = "Delivered"
        for stop in stops:
            if isinstance(stop, Location) is False:
                continue
            miles += stop.distance
            route.append(stop.label)
        return miles, route

    def add_truck(self, count=1):
        """

        :param count:
        :return:
        """
        while count > 0:
            new_truck = Truck(count)
            self.trucks.append(new_truck)
            count -= 1

    def load_all(self, truck):
        """

        :param truck:
        :return:
        """
        truck.capacity = len(self.database.table)
        for pkg in self.database.table:
            if truck.not_full() is False:
                break
            if pkg.delivery_status != "At Hub":
                continue
            pkg.delivery_status = "In Route"
            truck.load_package(pkg.pkg_id, self.destinations.get_location(pkg.address))

    def load_up_truck(self, truck):
        """

        :param truck:
        :return:
        """
        for pkg in self.database.table:
            if truck.not_full() is False:
                break
            if pkg.delivery_status != "At Hub":
                continue
            pkg.delivery_status = "In Route"
            truck.load_package(pkg.pkg_id, self.destinations.get_location(pkg.address))

    def load_truck_2(self, truck):
        """

        :param truck:
        :return:
        """
        for pkg in self.database.table:
            if truck.not_full() is False:
                break
            if pkg.delivery_status != "At Hub":
                continue
            if pkg.special_notes.endswith('Must', 0, 4) or pkg.special_notes.endswith('truck 2'):
                pkg.delivery_status = "In Route"
                truck.load_package(pkg.pkg_id, self.destinations.get_location(pkg.address))
                continue
            if pkg.deadline == 24:
                pkg.delivery_status = "In Route"
                truck.load_package(pkg.pkg_id, self.destinations.get_location(pkg.address))

    def load_packages(self):
        """

        :return:
        """
        with open('WGUPS_Package_File.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count > 2:
                    self.database.insert(row[0], row[1], row[4], row[5], row[6], row[7])
                line_count += 1

    def load_distances(self, distances):
        """

        :param distances:
        :return:
        """
        points = list(self.destinations.points.keys())
        for i in distances:
            for j in range(0, len(points) - 1):
                distance = float(i[j])
                if distance == 0:
                    break
                point_a = points[j]
                point_b = points[distances.index(i)]
                self.destinations.add_distance(point_a, point_b, distance)

    def load_locations(self):
        """

        :return:
        """
        with open('WGUPS_Distance_Table.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            distances = []
            self.destinations.add_location(self.center)
            distances.append(
                ['0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', ''])
            for row in csv_reader:
                line_count += 1
                if line_count < 4:
                    continue
                address = row[0].split("\n")
                label = row[1].split("\n")
                zip_code = label[1].strip("(").strip(")")
                location = Location(
                    address[0], address[1], "Salt Lake City", "UT", zip_code, label[0].strip(" "))
                self.destinations.add_location(location)
                distances.append(row[2:-1])
            self.load_distances(distances)

    def route_truck(self, truck):
        """

        :param truck:
        :return:
        """
        stops = [self.center]
        stops += list(truck.cargo.keys())
        self.dijkstra_shortest_path(self.center, stops)
        return stops

    def dijkstra_shortest_path(self, start_point, stops):
        """

        :param start_point:
        :param stops:
        :return:
        """
        # Put all points in an unvisited queue.
        unvisited_queue = []
        for current_point in stops:
            if isinstance(current_point, Location):
                unvisited_queue.append(current_point)

        # start_point has a distance of 0 from itself
        start_point.distance = 0

        # A point is removed each iteration and repeats until the list is empty.
        while len(unvisited_queue) > 0:

            # Visit point with minimum distance from start_point
            smallest_index = 0
            for i in range(1, len(unvisited_queue)):
                if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                    smallest_index = i
            current_point = unvisited_queue.pop(smallest_index)

            # Check potential path lengths from the current_point to all neighbors.
            for neighbor in self.destinations.points[current_point]:
                route_distance = self.destinations.distances[(current_point, neighbor)]
                alternative_path_distance = current_point.distance + route_distance

                # If shorter path from start_point to neighbor is found,
                # update neighbor's distance and predecessor
                if alternative_path_distance < neighbor.distance:
                    neighbor.distance = alternative_path_distance
                    neighbor.prev_point = current_point
