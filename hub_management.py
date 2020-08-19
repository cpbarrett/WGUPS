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

    def __init__(self, truck_count=3, opening_time="08:00 AM"):
        print("Welcome to Hub Management Center")
        self.current_time = opening_time
        self.truck_count = truck_count
        self.trucks = []
        self.add_truck(truck_count)
        self.center = Location("Western Governors University", "4001 South 700 E", 84107, "HUB")
        self.destinations = distance_table.DistanceTable()
        self.database = HashTable()
        self.load_locations()
        self.load_packages()

    def add_truck(self, count):
        """
        Adds a number of new trucks to Hub according to the given count.
        :param count:int
        :return:None
        """
        while count > 0:
            new_truck = Truck(count)
            self.trucks.append(new_truck)
            count -= 1
        self.trucks.reverse()

    def load_any_truck_(self, truck: Truck):
        """
        Loads the next available package from hash table onto the truck.
        :param truck:Truck
        :return:None
        """
        for pkg in self.database.table:
            if truck.not_full() is False:
                break
            if pkg.delivery_status != "At Hub":
                continue
            if truck.load_package(pkg.pkg_id, self.destinations.get_location(pkg.address)):
                pkg.delivery_status = "In Route"

    def load_forced_group(self, truck: Truck):
        """
        Loads packages that must be delivered together.
        :param truck:Truck
        :return:None
        """
        for pkg in self.database.table:
            if truck.not_full() is False:
                break
            if pkg.delivery_status != "At Hub":
                continue
            if pkg.special_notes.endswith('Must', 0, 4):
                if truck.load_package(pkg.pkg_id, self.destinations.get_location(pkg.address)):
                    pkg.delivery_status = "In Route"
                    group = pkg.special_notes.strip('Must be delivered with ').split(',')
                    for pair in group:
                        pkg_match = self.database.look_up(int(pair))
                        destination = self.destinations.get_location(pkg_match.address)
                        truck.load_package(int(pair), destination)
                        pkg_match.delivery_status = "In Route"

    def load_truck_2(self, truck: Truck):
        """
        Loads all packages that must be on truck 2.
        :param truck:Truck
        :return:None
        """
        for pkg in self.database.table:
            if truck.not_full() is False:
                break
            if pkg.delivery_status != "At Hub":
                continue
            if pkg.special_notes.endswith('truck 2'):
                if truck.load_package(pkg.pkg_id, self.destinations.get_location(pkg.address)):
                    pkg.delivery_status = "In Route"

    def load_same_stop_truck(self, truck: Truck):
        """
        Loads packages with delivery addresses that the truck is already going to.
        :param truck:Truck
        :return:None
        """
        for pkg in self.database.table:
            if truck.not_full() is False:
                break
            if pkg.delivery_status != "At Hub":
                continue
            pkg_location = self.destinations.get_location(pkg.address)
            if pkg_location in truck.cargo.keys():
                if truck.load_package(pkg.pkg_id, pkg_location):
                    pkg.delivery_status = "In Route"

    def load_zip_code_truck(self, truck: Truck):
        """
        Loads packages with similar zip_codes onto the given truck.
        :param truck:Truck
        :return:None
        """
        zip_code_locations = self.destinations.get_zip_code_matches(truck.cargo.keys())
        for pkg in self.database.table:
            if truck.not_full() is False:
                break
            if pkg.delivery_status != "At Hub":
                continue
            pkg_location = self.destinations.get_location(pkg.address)
            if pkg_location in zip_code_locations:
                if truck.load_package(pkg.pkg_id, pkg_location):
                    pkg.delivery_status = "In Route"

    def load_delayed_truck(self, truck: Truck, has_deadline=True):
        """
        Loads a truck with delayed packages
        :param truck:
        :param has_deadline:
        :return:
        """
        for pkg in self.database.table:
            if truck.not_full() is False:
                break
            if pkg.delivery_status != "At Hub":
                continue
            if has_deadline:
                if pkg.deadline == "EOD":
                    continue
            if pkg.special_notes.__contains__("Delayed"):
                delay = pkg.special_notes[-8:]
                later_time = pkg.calculate_deadline(delay)
                depart_time = Package.calculate_deadline(truck.depart_at)
                if later_time > depart_time:
                    truck.depart_at = delay
                if truck.load_package(pkg.pkg_id, self.destinations.get_location(pkg.address)):
                    pkg.delivery_status = "In Route"

    def load_early_truck(self, truck: Truck):
        """
        Load truck with packages that have deadlines before 10:30 AM.
        :param truck:
        :return:
        """
        for pkg in self.database.table:
            if truck.not_full() is False:
                break
            if pkg.delivery_status != "At Hub":
                continue
            if len(pkg.special_notes) > 1:
                continue
            if pkg.calculate_deadline(pkg.deadline) <= 10.5:
                if truck.load_package(pkg.pkg_id, self.destinations.get_location(pkg.address)):
                    pkg.delivery_status = "In Route"

    def load_packages(self):
        """
        Loads all the packages into the database (hash table) from the csv file.
        :return:None
        """
        with open('WGUPS_Package_File.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count > 2:
                    self.database.insert(int(row[0]), row[1], int(row[4]), row[5], int(row[6]), row[7])
                line_count += 1

    def load_distances(self, distances: list):
        """
        Populates the distances or edge weights for the graph class, destinations.
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
        Reads in the string data from the csv file. Loads each location as a point in the graph class.
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
                zip_code = int(label[1].strip("(").strip(")"))
                location = Location(
                    address[0], address[1], zip_code, label[0].strip(" "))
                self.destinations.add_location(location)
                distances.append(row[2:-1])
            self.load_distances(distances)

    def find_a_way(self, truck: Truck):
        """
        finds the shortest route along the stops from truck in O(N^2) time
        :param truck: truck with stops to make
        :return: the list of locations and the total distance traveled by the truck
        """
        stops = list(truck.cargo.keys())
        current = self.center  # start at the Hub
        the_way = [current]
        distance = 0.0
        while stops:
            result = self.nearest_neighbor(stops, current)
            distance += result[1]
            the_way.append(result[0])
            current = stops.pop(0)
            packages = truck.unload_package(current)
            delivery_time = Package.get_delivery_time(distance, truck.speed, truck.depart_at)
            for pkg_id in packages:
                pkg = self.database.look_up(pkg_id)
                pkg.delivery_status = "Delivered"
                pkg.delivery_time = delivery_time
        distance += self.destinations.get_distance(the_way[-1], self.center)  # return to the Hub
        truck.depart_at = Package.get_delivery_time(distance, truck.speed, truck.depart_at)
        return the_way, distance

    def nearest_neighbor(self, stops: [Location], current: Location):
        """
        Loop through stops and hold onto min value to find shortest distance.
        :param stops: list of points
        :param current: current stop
        :return: Neighbor is the next closest stop and val is the distance to that stop.
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

    def get_deliveries(self, current_time="EOD"):
        """
        Returns a list of all delivered packages.
        :param current_time: What time is it?
        :return: None
        """
        deliveries = []
        for pkg in self.database.table:
            if pkg.delivery_status.__contains__("Delivered"):
                if pkg.calculate_deadline(pkg.delivery_time) < pkg.calculate_deadline(current_time):
                    deliveries.append(pkg)
        return deliveries

    def get_miles(self):
        """
        Returns the mileage, departure time, and return time for all hub trucks.
        :return: info, miles
        """
        miles = []
        info = []
        for truck in self.trucks:
            departure_time = f'Truck {truck.truck_id}:\n'
            departure_time += f'Departs from {self.center.label} at {truck.depart_at}.'
            result = self.find_a_way(truck)
            mileage = f'Travels {result[1].__round__(2)} miles.'
            return_time = f'Returns to {self.center.label} by {truck.depart_at}.'
            miles.append(result[1])
            info.append([departure_time, mileage, return_time])
        return info, miles

    # the following functions are only for testing purposes and not used in the main program
    def truck_mileage(self, truck: Truck):
        """
        Calculates the total round trip mileage driven by the truck.
        :param truck:Truck
        :return:int, List[Location]
        """
        stops = self.route_truck(truck)
        miles = 0.0
        route = []
        for packages in truck.cargo.values():
            for pkg_id in packages:
                pkg = self.database.look_up(pkg_id)
                pkg.delivery_status = "Delivered"
        for stop in stops:
            miles += stop.distance
            route.append(stop.label)
        return miles, route

    def load_all(self, truck):
        """
        Test function that loads all of the packages onto 1 truck.
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
        Finds shortest route using Dijkstra's Shortest Paths.
        :param truck:Truck
        :return:List[Location]
        """
        stops = [self.center]
        stops += list(truck.cargo.keys())
        self.dijkstra_shortest_path(self.center, stops)
        return stops

    def dijkstra_shortest_path(self, start_point, stops):
        """
        Implementation of Dijkstra's Algorithm used only for testing purposes.
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
