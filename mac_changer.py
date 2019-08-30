#!/usr/bin/env python

# subprocess module contains functions related to OS commands
import subprocess
# optparse module allows us to get CLI arguments from the user, parse them and use them
import optparse
# re module allows us to use Regex commands
import re

# functions for resuable and readable code
# define get_arguments function
def get_arguments():
    # Indented code is function block in change_mac function
    # create parsing object instance - parser that can handle user inputs for us
    # OptionParser starts with a capital letter and is thus a class - determines what we can do with OptionParser
    parser = optparse.OptionParser()
    # Giving user CLI arguments to change mac address on interface and type both mac and interface
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Interface to change its MAC address")
    # parse_args() is a method on parser object that returns 2 variables (options, arguments)
    (options, arguments) = parser.parse_args()
    if not options.interface:   #if user did not input an interface
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:   #if user did not input a new_mac
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return options

# define change_mac function which takes in arguments (interface and new_mac variables)
def change_mac(interface, new_mac):
    # Indented code is function block in change_mac function
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    # Module.function(arguments) | We can run shell commands from ifconfig function
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

# define get_current_mac function which takes in interface argument
def get_current_mac(interface):
    # execute and read ifconfig
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # use search method for regex library and use regex rules in python with (r"...")
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_search_result:
        return mac_search_result.group(0)  # group(0) is for first occurence of regex search match
    else:
        print("[-] Could not read MAC address.")

# call get_arguments function after users have specified options.interface & options.new_mac
options = get_arguments()
#call get_current_mac function with user input from options.interface
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))
# call change_mac function with user input from options.interface & options.new_mac
change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:  #We use == to compare values and we use = to assign or change variables
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")