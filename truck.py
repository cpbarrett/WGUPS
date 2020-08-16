"""Truck Class"""
from location import Location


class Truck:
    """Trucks have id numbers, travel at 18mph, and carry 16 packages."""
    def __init__(self, truck_id: int, capacity=16):
        """
        Constructor sets the id number.
        :param truck_id: id number of the truck
        """
        self.truck_id = truck_id
        self.speed = 18.0
        self.capacity = capacity
        self.cargo = {}
        self.depart_at = "08:00 AM"

    def load_package(self, pkg_id: int, delivery_location: Location) -> bool:
        """
        If truck is not full, add a package and set it as 'In Route'.
        :param pkg_id: package's ID number
        :param delivery_location: the delivery location of the package
        :return:True if loaded
        """
        if self.not_full() is False or delivery_location is None:
            return False
        if delivery_location not in self.cargo:
            self.cargo[delivery_location] = list()
        self.cargo[delivery_location].append(pkg_id)
        return True

    def unload_package(self, delivery_location: Location):
        """
        If truck is not empty, remove the packages being delivered to this location from cargo.
        :param delivery_location: destination of the package
        :return: Packages being delivered
        """
        if len(self.cargo) > 0:
            return self.cargo.pop(delivery_location)
        return None

    def not_full(self):
        """
        Return False if the truck cannot carry anymore packages.
        :return:bool
        """
        if len(self.cargo.items()) < self.capacity:
            return True
        return False

    def get_all_stops(self):
        """
        Return a list of all the stops the truck needs to make.
        :return:List[str]
        """
        stops = []
        for stop in self.cargo:
            stops.append(stop.address)
        return stops
