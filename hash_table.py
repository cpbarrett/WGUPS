"""
HashTable to manage storage of all packages and their information
"""
from package import Package


# noinspection PyMethodMayBeStatic
class HashTable:
    """
    The Hashtable class has Big-O is as follows:
    Init: O(N)
    Resize: O(n)
    Lookup: O(1)
    Insert: O(1)
    Update: O(1)
    Remove: O(1)
    """

    def __init__(self, table_size=41):
        """
        table is initialized with empty values and small initial capacity
        """
        self.dummy_pkg = Package(0, "", "", "EOD", 0, "")
        self.table = [self.dummy_pkg] * table_size
        self.element_count = 0

    def hash(self, pkg_id):
        """
        calculate the table index for a specific pkg_id
        :param pkg_id: int
        :return: int
        """
        return hash(pkg_id) % 31

    def resize(self):
        """
        If the table is more than 70% full, expand the table size.
        :return: None
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
        :param pkg_id: int
        :return: Package
        """
        index = self.hash(pkg_id)
        return self.table[index]

    def insert(self, pkg_id, address, zip_code, deadline, weight, special_notes):
        """
        Creates a pkg object based on given information and inserts it into the table using pkg_id.
        :param pkg_id: int
        :param address: str
        :param zip_code: int
        :param deadline: str
        :param weight: int
        :param special_notes: str
        :return: None
        """
        # pkg_id, label, zip_code, dl, wt, notes, delivery status
        new_pkg = Package(pkg_id, address, zip_code, deadline, weight, special_notes)
        index = self.hash(new_pkg.pkg_id)
        self.table[index] = new_pkg
        self.element_count += 1
        self.resize()

    def update(self, package):
        """
        Update a package if it exists in the table
        :param package: Package
        :return: None
        """
        if self.look_up(package.pkg_id) == package.pkg_id:
            index = self.hash(package.pkg_id)
            self.table[index] = package

    def remove(self, pkg_id):
        """
        Removes an item with matching pkg_id.
        :param pkg_id: int
        :return: None
        """
        index = self.hash(pkg_id)
        self.table[index] = self.dummy_pkg
