import csv

from distance_table import DistanceTable, Location
from hash_table import HashTable
from truck import Truck


class Hub:
    def __init__(self, opening_time="08:00 AM", truck_count=1):
        print("Welcome to Hub Management Center")
        self.opening_time = opening_time
        self.truck_count = truck_count
        self.trucks = []
        self.add_truck(truck_count)
        self.center = Location(
                    "Western Governors University",
                    "4001 South 700 East", "Salt Lake City",
                    "UT", "84107", "HUB")
        self.destinations = DistanceTable()
        self.database = HashTable()
        self.load_locations()
        self.load_packages()

    def route_truck(self, truck):
        delivery_addresses = [self.center]
        for x in truck.cargo:
            delivery_addresses.append(self.destinations.get_location(x.address))

    def add_truck(self, count=1):
        while count > 0:
            new_truck = Truck(count)
            self.trucks.append(new_truck)
            count -= 1

    def load_up_truck(self, truck):
        while truck.not_full():
            truck.load_package(self.database.nearest_deadline())

    def load_packages(self):
        with open('WGUPS_Package_File.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count > 2:
                    self.database.insert(row[0], row[1], row[4], row[5], row[6], row[7])
                line_count += 1

    def load_distances(self, distances):
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
