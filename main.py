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
    hub.database.look_up(9).correct_info("410 S State St", "84111", "corrected at 10:20 am")
    hub.load_truck_2(hub.trucks[1])
    info, miles = hub.get_miles()
    print_results(info, miles)
    # gui_menu(hub)


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
                break
            if command == 2:
                given_time = input("Enter a time ie. 00:00 AM or press enter to continue: ")
                if given_time == "":
                    check_deliveries(hub)
                else:
                    check_deliveries(hub, given_time)
            if command == 3:
                print_results(info, miles)
            else:
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
    for i in range(len(info)):
        print(info[i][0])
        print(info[i][1])
        print(info[i][2])
    print('\n'f'The total distance traveled by all trucks is {sum(miles).__round__(2)}')


def check_deliveries(hub: Hub, given_time="11:59 PM"):
    """
    Returns a list of all delivered packages.
    :param hub: the depot
    :param given_time: specified time to check delivery status
    :return: None
    """
    count = 0
    deliveries = hub.get_deliveries(given_time)
    for pkg in deliveries:
        count += 1
        print(pkg.__str__())
    print(f'Total Deliveries: {count}')


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
