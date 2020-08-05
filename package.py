"""Package Class"""


class Package:
    """Package class holds all the information for a package"""

    def __init__(self, pkg_id, address, zip_code, deadline, weight, special_notes):
        self.pkg_id = int(pkg_id)
        self.address = Package.convert_delivery_address(address)
        self.city = "Salt Lake City"
        self.state = "UT"
        self.zip_code = zip_code
        self.deadline = Package.calculate_deadline(deadline)
        self.weight = int(weight)
        self.special_notes = special_notes
        self.delivery_status = "At Hub"

    @staticmethod
    def calculate_deadline(deadline):
        """
        Convert deadline from string into a float
        :param deadline:
        :return:
        """
        if deadline == "EOD":
            return 24
        time = deadline.split(":")
        am_pm = 0
        if time[1][3:-1] == "PM":
            am_pm = 12
        hour = float(time[0])
        minute = float(time[1][0:2]) / 60
        return hour + minute + am_pm

    @staticmethod
    def convert_delivery_address(address):
        """
        Makes the delivery address more consistent with Location labels
        :param address: address containing North, South, East, West
        :return: address string with abbreviated directions
        """
        address.replace('North', 'N')
        address.replace('South', 'S')
        address.replace('East', 'E')
        address.replace('West', 'W')
        return address
