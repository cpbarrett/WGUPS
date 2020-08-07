"""
The location class represents a vertex point in the distance_table (graph).
"""


class Location:
    """
    Each location object has a name, address, zip_code, and label
    """
    def __init__(self, name: str, address: str, zip_code: str, label: str):
        self.name = name
        self.address = address + " Salt Lake City, UT"
        self.zip_code = zip_code
        self.label = Location.convert_delivery_label(label)
        self.distance = 140
        self.prev_point = None

    @staticmethod
    def convert_delivery_label(label):
        """
        Makes the label data more consistent with packages
        :param label: the label to be shortened
        :return: label with abbreviated cardinal directions
        """
        label.replace('North', 'N')
        label.replace('South', 'S')
        label.replace('East', 'E')
        label.replace('West', 'W')
        return label
