"""
HashTable to manage storage of all packages and their information
"""
from package import Package


class HashTable:
    """
    Hashtable class definition using quadratic probing
    """

    def __init__(self, table_size=41):
        """
        table is initialized with empty values and small initial capacity
        """
        dummy_pkg = Package(0, "", "", "EOD", 0, "")
        self.table = [dummy_pkg] * table_size
        self.element_count = 0

    def hash(self, pkg_id):
        """
        calculate the table index for a specific pkg_id
        :param pkg_id:
        :return:
        """
        return hash(pkg_id) % 31

    def resize(self):
        """
        If the table is more than 70% full, expand the table size.
        :return:
        """
        size = len(self.table)
        load_factor = self.element_count / size
        if load_factor >= 0.7:
            dummy_pkg = Package(0, "", "", "EOD", 0, "")
            extension = [dummy_pkg] * size
            self.table.extend(extension)

    def look_up(self, pkg_id):
        """
        Gets package with matching pkg_id. Returns None if there is no matching package.
        :param pkg_id:
        :return:
        """
        index = self.hash(pkg_id)
        return self.table[index]

    def insert(self, pkg_id, address, zip_code, deadline, weight, special_notes):
        """
        Creates a pkg object based on given information and inserts it into the table using pkg_id.
        :param pkg_id:
        :param address:
        :param zip_code:
        :param deadline:
        :param weight:
        :param special_notes:
        :return:
        """
        # pkg_id, label, zip_code, deadline, weight, special_notes, delivery status
        new_pkg = Package(pkg_id, address, zip_code, deadline, weight, special_notes)
        index = self.hash(new_pkg.pkg_id)
        self.table.insert(index, new_pkg)
        self.element_count += 1
        self.resize()

    def update(self, package):
        """
        Update a package if it exists in the table
        :param package:
        :return:
        """
        if self.look_up(package.pkg_id) is not None:
            index = self.hash(package.pkg_id)
            self.table.insert(index, package)

    def remove(self, pkg_id):
        """
        Removes an item with matching key and returns the item if removed.
        :param pkg_id:
        :return:
        """
        if self.look_up(pkg_id) is not None:
            index = self.hash(pkg_id)
            return self.table.pop(index)
