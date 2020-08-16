"""
The Hub class loads all the data from the csv files, creates the package hash table,
 and creates the graph containing all the delivery locations.
"""
import csv

import distance_table
from location import Location
from hash_table import HashTable
from package import Package
from truck import Truck


class Hub:
    """
    Class constructor takes in the number of trucks and an optional opening time.
    The hub location is created manually for use elsewhere.
    """

    def __init__(self, truck_count=2, opening_time="08:00 AM"):
        print("Welcome to Hub Management Center")
        self.current_time = opening_time
        self.truck_count = truck_count
        self.trucks = []
        self.add_truck(truck_count)
        self.center = Location("Western Governors University", "4001 South 700 E", "84107", "HUB")
        self.destinations = distance_table.DistanceTable()
        self.database = HashTable()
        self.load_locations()
        self.load_packages()

    def truck_mileage(self, truck):
        """

        :param truck:Truck
        :return:int, List[Location]
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

    def add_truck(self, count):
        """
        Adds a number of new trucks to Hub according to the given count
        :param count:int
        :return:None
        """
        while count > 0:
            new_truck = Truck(count)
            self.trucks.append(new_truck)
            count -= 1
        self.trucks.reverse()

    def load_truck_2(self, truck):
        """
        loads packages onto truck 2
        :param truck:Truck
        :return:None
        """
        for pkg in self.database.table:
            if truck.not_full() is False:
                break
            if pkg.delivery_status != "At Hub":
                continue
            if pkg.special_notes.endswith('Must', 0, 4) or pkg.special_notes.endswith('truck 2'):
                if truck.load_package(pkg.pkg_id, self.destinations.get_location(pkg.address)):
                    pkg.delivery_status = "In Route"
                    continue
            if pkg.calculate_deadline(pkg.deadline) == 24:
                if truck.load_package(pkg.pkg_id, self.destinations.get_location(pkg.address)):
                    pkg.delivery_status = "In Route"

    def load_packages(self):
        """

        :return:None
        """
        with open('WGUPS_Package_File.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count > 2:
                    self.database.insert(row[0], row[1], row[4], row[5], row[6], row[7])
                line_count += 1

    def load_distances(self, distances: list):
        """
        populates the distances or edge weights for the graph class destinations
        :param distances:List[[str, str]]
        :return:None
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
        Reads in the string data from the csv file loads each location as a point on a graph class
        :return:None
        """
        with open('WGUPS_Distance_Table.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            distances = list()
            self.destinations.add_location(self.center)
            distances.append(
                ['0', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', '', '', '', ''])
            for row in csv_reader:
                line_count += 1
                if line_count < 4:
                    continue
                address = row[0].split("\n")
                label = row[1].split("\n")
                zip_code = label[1].strip("(").strip(")")
                location = Location(
                    address[0], address[1], zip_code, label[0].strip(" "))
                self.destinations.add_location(location)
                distances.append(row[2:-1])
            self.load_distances(distances)

    def find_a_way(self, truck):
        """
        finds the shortest route along the stops from truck in O(N) time
        :param truck: truck with stops to make
        :return: the list of locations and the total distance traveled by the truck
        """
        stops = []
        stops += list(truck.cargo.keys())
        current = self.center  # start at the Hub
        the_way = [current]
        distance = 0.0
        while stops:
            result = self.nearest_neighbor(stops, current)
            distance += result[1]
            the_way.append(result[0])
            current = stops.pop(0)
            packages = truck.unload_package(current)
            delivery_time = Package.calculate_delivery_time(distance, truck.speed, self.current_time)
            for ID in packages:
                pkg = self.database.look_up(ID)
                pkg.delivery_status = "Delivered at " + delivery_time
        distance += self.destinations.get_distance(the_way[-1], self.center)  # return to the Hub
        truck.depart_at = Package.calculate_delivery_time(distance, truck.speed, self.current_time)
        return the_way, distance

    def nearest_neighbor(self, stops: [Location], current: Location):
        """
        Loop through stops and hold onto min value to find shortest distance
        :param stops: list of points
        :param current: current stop
        :return: neighbor is the next closest stop and val is the distance to that stop
        """
        val = 140.0
        neighbor = current
        # loop through packages and hold onto min value to compare distances
        for stop in stops:
            dist = self.destinations.get_distance(current, stop)
            if dist < val:
                neighbor = stop
                val = dist
        return neighbor, val

    # the following functions are only for testing purposes and not used in the main program
    def load_all(self, truck):
        """
        test function that loads all of the packages onto 1 truck
        :param truck:Truck
        :return:None
        """
        truck.capacity = 41
        for num in range(0, truck.capacity):
            pkg = self.database.look_up(num)
            pkg.delivery_status = "In Route"
            truck.load_package(pkg.pkg_id, self.destinations.get_location(pkg.address))

    def route_truck(self, truck):
        """
        finds shortest route using Dijkstra's Shortest Paths
        :param truck:Truck
        :return:List[Location]
        """
        stops = [self.center]
        stops += list(truck.cargo.keys())
        self.dijkstra_shortest_path(self.center, stops)
        return stops

    def dijkstra_shortest_path(self, start_point, stops):
        """
        implementation of Dijkstra's Algorithm used only for testing purposes
        :param start_point:Location
        :param stops:List[Location]
        :return:None
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
