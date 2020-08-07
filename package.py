"""
Package Class that acts as a vertex for the graph class, DistanceTable
"""


class Package:
    """Package class holds all the information for a package"""

    def __init__(self, pkg_id: int, address: str, zip_code: str, dl: str, wt: int, notes: str):
        """
        :param pkg_id: unique id for each package
        :param address: address package is being delivered to
        :param zip_code: zip_code of each package
        :param dl: expected date & time to deliver the package
        :param wt: mass of the package in kg
        :param notes: describes problems with or instructions for a package's delivery
        """

        self.pkg_id = pkg_id
        self.address = Package.convert_delivery_address(address)
        self.city = "Salt Lake City"
        self.state = "UT"
        self.zip_code = zip_code
        self.deadline = Package.calculate_deadline(dl)
        self.weight = wt
        self.special_notes = notes
        self.delivery_status = "At Hub"

    @staticmethod
    def calculate_deadline(deadline: str) -> float:
        """
        Convert deadline from str into a float
        :param deadline: str containing hr:min and AM or PM
        :return: float representation of the dl time in 24 hr time
        """
        if deadline == "EOD":
            return 24.0
        time = deadline.split(":")
        am_pm = float(0.0)
        if time[1][3:-1] == "PM":
            am_pm = 12.0
        hour = float(time[0])
        minute = float(time[1][0:2]) / 60
        return hour + minute + am_pm

    @staticmethod
    def convert_delivery_address(address: str):
        """
        Makes the delivery address more consistent with Location labels
        :param address: containing North, South, East, West
        :return: address string with abbreviated cardinal directions
        """
        address.replace('North', 'N')
        address.replace('South', 'S')
        address.replace('East', 'E')
        address.replace('West', 'W')
        return address
