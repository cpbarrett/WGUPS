from hub_management import Hub


def print_menu():
    print()
    print("\tEnter a command: ")
    print("\t1 - Advance Time")
    print("\t2 - Check Packages")
    print("\t3 - Check Trucks")
    print("\t4 - Exit program")
    print()


if __name__ == "__main__":
    hub = Hub()
    hub.load_up_truck(hub.trucks[0])
    hub.route_truck(hub.trucks[0])
    # print_menu()
    # while True:
    #     try:
    #         command = int(input("Command: "))
    #         if 1 <= command <= 4:
    #             break
    #     except TypeError:
    #         print("Error please enter a number from 1-4.")
    #         print_menu()
    # hub.destinations.print_table()
