"""
HashTable to manage storage of all packages and their information
"""
from package import Package


# noinspection PyMethodMayBeStatic
class HashTable:
    """
    The Hashtable class has Big-O is as follows:
    Init: O(N)
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

    def look_up(self, pkg_id: int):
        """
        Gets package with matching pkg_id. Returns None if there is no matching package.
        :param pkg_id: int
        :return: Package
        """
        index = int(pkg_id)
        if self.table[index] is None:
            return None
        return self.table[index]

    def insert(self, pkg_id: int, address: str, zip_code: str, deadline: str, weight: int, special_notes: str):
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
        index = int(pkg_id)
        new_pkg = Package(pkg_id, address, zip_code, deadline, weight, special_notes)
        self.table[index] = new_pkg

    def update(self, package):
        """
        Update a package if it exists in the table
        :param package: Package
        :return: None
        """
        if self.look_up(package.pkg_id) == package.pkg_id:
            index = int(package.pkg_id)
            self.table[index] = package

    def remove(self, pkg_id):
        """
        Removes an item with matching pkg_id.
        :param pkg_id: int
        :return: None
        """
        index = int(pkg_id)
        self.table[index] = self.dummy_pkg
