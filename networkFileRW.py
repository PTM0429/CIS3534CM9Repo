#!/usr/bin/env python3
# networkFileRW.py
# Pamela Brauda
# Thursday, March 3, 2022
# Updated by completing the JSON file reading and writing,
# and adding checks for valid IP addresses.

# import the JSON module
try:
    import json
except ImportError:
    print("Could not import the JSON module.")
    raise SystemExit

# file constants
ROUTER_FILE = "equip_r.txt"
SWITCH_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
ERROR_FILE = "errors.txt"

# prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"


# function to get valid device
def getValidDevice(routers, switches):
    validDevice = False

    while not validDevice:
        device = input(UPDATE + QUIT).lower()

        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == "x":
            return device
        else:
            print("That device is not in the network inventory.")


# function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False

    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split(".")

        # check that there are four numbers in the IP address
        if len(octets) == 4:
            validIP = True

            for byte in octets:
                if not byte.isdigit() or int(byte) < 0 or int(byte) > 255:
                    validIP = False
                    break
        else:
            validIP = False

        if validIP:
            return ipAddress, invalidIPCount
        else:
            invalidIPCount += 1
            invalidIPAddresses.append(ipAddress)
            print(SORRY)


def main():

    # open the router and switch files and read the JSON data
    try:
        with open(ROUTER_FILE, "r") as routerFile:
            routers = json.load(routerFile)

        with open(SWITCH_FILE, "r") as switchFile:
            switches = json.load(switchFile)

    except FileNotFoundError:
        print("Could not find one of the equipment files.")
        return

    # dictionaries
    # the updated dictionary holds the device name and new IP address
    updated = {}

    # list of bad addresses entered by the user
    invalidIPAddresses = []

    # accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    # flags and sentinels
    quitNow = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")

    for router, ipa in routers.items():
        print("\t" + router + "\t\t" + ipa)

    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:

        # function call to get valid device
        device = getValidDevice(routers, switches)

        if device == "x":
            quitNow = True
            break

        # function call to get valid IP address
        ipAddress, invalidIPCount = getValidIP(
            invalidIPCount, invalidIPAddresses
        )

        # update device
        if device in routers.keys():
            routers[device] = ipAddress
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1

        # add the device and IP address to the updated dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)

    # user finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    # write the updated equipment dictionary to a file
    with open(UPDATED_FILE, "w") as updatedFile:
        json.dump(updated, updatedFile)

    print("Updated equipment written to file 'updated.txt'")
    print()
    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    # write the list of invalid addresses to a file
    with open(ERROR_FILE, "w") as errorFile:
        json.dump(invalidIPAddresses, errorFile)

    print("List of invalid addresses written to a file 'errors.txt'")


# top-level scope check
if __name__ == "__main__":
    main()
