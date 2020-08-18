"""
C. Parker Barrett
#001392593
Main Class for controlling the GUI and running the hub_management system
"""
from hub_management import Hub


def main():
    """
    Runs the main demo of the WGU-PS Hub Management System with 2 Trucks
    :return: None
    """
    # sample_test()
    hub = Hub()
    # corrections for package 9
    pkg_9 = hub.database.look_up(9)
    pkg_9.correct_info("410 S State St", "84111", "corrected at 10:20 AM")
    hub.trucks[1].load_package(pkg_9.pkg_id, hub.destinations.get_location(pkg_9.address))
    pkg_9.delivery_status = "In Route"
    hub.trucks[1].depart_at = "10:20 AM"

    # load truck 2
    hub.load_truck_2(hub.trucks[1])

    # fill truck 3
    hub.load_forced_group(hub.trucks[2])
    hub.load_same_stop_truck(hub.trucks[2])
    hub.load_zip_code_truck(hub.trucks[2])

    # load truck 1
    hub.load_delayed_truck(hub.trucks[0])
    hub.load_early_truck(hub.trucks[0])
    hub.load_same_stop_truck(hub.trucks[0])
    hub.load_zip_code_truck(hub.trucks[0])

    # fill truck 2
    hub.load_delayed_truck(hub.trucks[1], False)
    hub.load_same_stop_truck(hub.trucks[1])
    hub.load_zip_code_truck(hub.trucks[1])
    hub.load_any_truck_(hub.trucks[1])

    # fill up last truck
    hub.load_any_truck_(hub.trucks[2])

    info, miles = hub.get_miles()
    # print_results(info, miles)
    # check_deliveries(hub)
    gui_menu(hub, info, miles)


def gui_menu(hub: Hub, info, miles):
    """
    Runs the Gui Control Menu for the Given Hub
    :param hub: the depot
    :param info: list of truck travel info
    :param miles: list of truck mileages
    :return: None
    """
    command = 0
    while command != 4:
        print_menu()
        try:
            command = int(input("Command: "))
            if command == 1:
                pkg_id = int(input("Enter a pkg id to lookup: "))
                print(hub.database.look_up(pkg_id).__str__())
                continue
            if command == 2:
                given_time = input("Enter a time ie. 00:00 AM or press enter to continue: ")
                if given_time == "":
                    check_deliveries(hub)
                    continue
                check_deliveries(hub, given_time)
                continue
            if command == 3:
                print_results(info, miles)
                continue
            if command == 4:
                break
            raise TypeError
        except TypeError:
            print("Error please enter a number from 1-4.")


def print_menu():
    """
    Prints the command menu for WGU-PS GUI
    :return: None
    """
    print()
    print("\tEnter a command: ")
    print("\t1 - Lookup Package")
    print("\t2 - Check Deliveries")
    print("\t3 - Print Results")
    print("\t4 - Exit program")
    print()


def print_results(info, miles):
    """
    Prints the mileage, departure time, and return time for all hub trucks.
    :param info: list of truck travel info
    :param miles: list of truck mileages
    :return: None
    """
    print()
    for _, j in enumerate(info):
        print(j[0])
        print(j[1])
        print(j[2])
        print()
    print('\n'f'The total distance traveled by all trucks is {sum(miles).__round__(2)}')
    print()


def check_deliveries(hub: Hub, given_time="EOD"):
    """
    Returns a list of all delivered packages.
    :param hub: the depot
    :param given_time: specified time to check delivery status
    :return: None
    """
    deliveries = hub.get_deliveries(given_time)
    for pkg in deliveries:
        print(pkg.__str__())
    print()
    print(f'Total Deliveries: {len(deliveries)}')


def sample_test():
    """
    Runs a test hub with 1 truck that delivers all packages according to Dijkstra's Shortest Paths
    :return: None
    """
    test_hub = Hub(1)
    # # corrections for package 9
    test_hub.database.look_up(9).correct_info("410 S State St", "84111", "corrected at 10:20 am")
    test_hub.load_all(test_hub.trucks[0])
    test_hub.route_truck(test_hub.trucks[0])
    test_hub.truck_mileage(test_hub.trucks[0])
    info, miles = test_hub.get_miles()
    print_results(info, miles)
    check_deliveries(test_hub)


if __name__ == "__main__":
    main()
