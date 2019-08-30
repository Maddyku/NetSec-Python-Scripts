#!/usr/bin/env python

import scapy.all as scapy
import optparse

def get_arguments():    #define get_arguments function
    parser = optparse.OptionParser() #OptionParser method from optparse module stored in parser variable
    #Add CLI Arguments for user using add_option method
    parser.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
    (options, arguments) = parser.parse_args()
    return options

def scan(ip): #define scan function with IP Parameter
    #Use ARP from scapy (to ask who has target IP) & store result in arp_request object
    arp_request = scapy.ARP(pdst=ip)
    #Set Destination MAC to Broadcast MAC and store it in broadcast variable
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request  #Append Ethernet Data to ARP Data
    #srp function in scapy used to send and receive packets with an ether   #verbose=False prints less "verbose" text
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #receive first element [0] of "answered_list" packet
    #Display appended "answered_list" data packet or response from target client
    #"answered_list" data packet is the MAC address of the device that has requested IP

    clients_list = []   #clients_list
    for element in answered_list:   # for loop to iterate over each element in answered_list (array)
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}  #clients_dictionary
        clients_list.append(client_dict) # Created List of Dictionaries by adding client_dictionary as an element to client_list
        #print (element[1].psrc + "\t\t" + element[1].hwsrc)  #print IP Address of target and print MAC Address of client IP
    return clients_list

def print_result(results_list): #define print_result function with results_list Parameter
    # \t used to tab  # \n used to go to new line # ------ used for styling
    print("IP\t\t\tMACAddress\n----------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

    scan_result = scan("10.0.2.1/24") #call scan function with IP Value
    print_result(scan_result)   #equate results_list to scan_result output

#call get_arguments function
options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)