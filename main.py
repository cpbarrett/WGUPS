"""
C. Parker Barrett
#001392593
Main Class for controlling the GUI and running the hub_management system
"""
from hub_management import Hub
from package import Package


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
    print_results(hub)
    # gui_menu(hub)


def gui_menu(hub: Hub):
    """
    Runs the Gui Control Menu for the Given Hub
    :param hub:
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
                check_deliveries(hub)
            if command == 3:
                print_results(hub)
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


def print_results(hub: Hub):
    """
    Prints the mileage, departure time, and return time for all hub trucks.
    :param hub: the depot
    :return: None
    """
    print()
    miles = []
    for truck in hub.trucks:
        print(f'Truck {truck.truck_id}:')
        print(f'Departs from {hub.center.label} at {truck.depart_at}.')
        result = hub.find_a_way(truck)
        print(f'Travels {result[1].__round__(2)} miles.')
        print(f'Returns to {hub.center.label} by {truck.depart_at}.')
        miles.append(result[1])
    print('\n'f'The total distance traveled by all trucks is {sum(miles).__round__(2)}')


def check_deliveries(hub: Hub):
    """
    Prints the status of all delivered packages.
    :param hub: the depot
    :return: None
    """
    count = 0
    for pkg in hub.database.table:
        if pkg.delivery_status.__contains__("Delivered"):
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
    print_results(test_hub)
    check_deliveries(test_hub)


if __name__ == "__main__":
    main()
