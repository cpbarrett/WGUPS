"""HashTable to manage storage of all packages and their information"""
from package import Package


class HashTable:
    """Hashtable class definition using quadratic probing"""

    def __init__(self):
        """table is initialized with empty values and small initial capacity"""
        self.size = 11
        dummy_pkg = Package(0, "", "", "EOD", 0, "")
        self.table = [dummy_pkg] * self.size

    def hash(self, pkg_id):
        """calculate the table index for a specific pkg_id"""
        return hash(pkg_id) % self.size

    def resize(self):
        pass

    def look_up(self, pkg_id):
        """Gets package with matching pkg_id. Returns None if there is no matching package."""
        index = self.hash(pkg_id)
        return self.table[index]

    def insert(self, pkg_id, address, zip_code, deadline, weight, special_notes, city="Salt Lake City", state="UT"):
        """Creates a pkg object based on given information and inserts it into the table using pkg_id."""
        # pkg_id, address, zip_code, deadline, weight, special_notes, delivery status
        new_pkg = Package(pkg_id, address, zip_code, deadline, weight, special_notes)
        index = self.hash(pkg_id)
        self.table.insert(index, new_pkg)

    def remove(self, pkg_id):
        """Removes an item with matching key and returns the item if removed."""
        index = self.hash(pkg_id)
        return self.table.pop(index)

    def nearest_deadline(self):
        if self.size == 0:
            return None
        nearest = self.table[0]
        for pkg in self.table:
            if nearest.deadline > pkg.deadline:
                nearest = pkg
        return nearest

