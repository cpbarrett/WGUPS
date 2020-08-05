"""Truck Class"""


class Truck:
    """Trucks have id numbers, travel at 18mph, and carry 16 packages."""
    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.speed = 18.0
        self.capacity = 16
        self.cargo = {}

    def load_package(self, pkg_id, delivery_location):
        """If truck is not full, add a package and set it as 'In Route'."""
        if self.not_full():
            self.cargo[delivery_location] = pkg_id

    def not_full(self):
        """Return False if the truck cannot carry anymore packages."""
        if len(self.cargo) < self.capacity:
            return True
        return False

    def get_all_stops(self):
        """Return a list of all the stops the truck needs to make."""
        stops = []
        for x in self.cargo:
            stops.append(x.address)
        return stops
