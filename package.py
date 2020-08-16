"""
Package class holds all the information for a package
"""


class Package:
    """
    Packages have id numbers, a delivery address and zip code, a deadline, weight,
    and special notes for delivery instructions
    """

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
        self.address = self.convert_delivery_address(address)
        self.city = "Salt Lake City"
        self.state = "UT"
        self.zip_code = zip_code
        self.deadline = dl
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
    def convert_delivery_address(address: str) -> str:
        """
        Makes the delivery address more consistent with Location labels
        :param address: containing North, South, East, West
        :return: address string with abbreviated cardinal directions
        """
        address = address.replace('North', 'N')
        address = address.replace('South', 'S')
        address = address.replace('East', 'E')
        address = address.replace('West', 'W')
        return address

    @staticmethod
    def calculate_delivery_time(miles: float, avg_speed: float, departure_time: str) -> str:
        """
        Calculate delivery time based on average speed and mileage.
        :param miles: current miles traveled from HUB
        :param avg_speed: avg_speed of the truck
        :param departure_time: the time the truck leaves the Hub
        :return: str representation of the dl time in 12 hr time
        """
        start_time = Package.calculate_deadline(departure_time)
        delivery_time = miles / avg_speed
        delivery_time += start_time
        hour = int(delivery_time)
        minute = int(60 * (delivery_time - hour))
        am_pm = " AM"
        if hour > 12:
            hour -= 12
            am_pm = " PM"
        if minute < 10:
            minute = "0" + str(minute)
        time = str(hour) + ":" + str(minute) + am_pm
        return time

    def correct_info(self, address: str = "", zip_code: str = "", notes: str = ""):
        """
        change the address, zip code, or special notes for this package
        :param address: corrected address
        :param zip_code: corrected zip code
        :param notes: updated special notes
        :return: None
        """
        if address != "":
            self.address = self.convert_delivery_address(address)
        if zip_code != "":
            self.zip_code = zip_code
        if notes != "":
            self.special_notes += "---" + notes

    def __str__(self) -> str:
        return str(f'PkgID={self.pkg_id} '
                   f' Delivery Address={self.address} '
                   f' Deadline={self.deadline} '
                   f' Weight={self.weight} '
                   f' {self.delivery_status}')
