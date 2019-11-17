#!usr/bin/env python3

import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='Target IP / IP range.')
    arguments = parser.parse_args()
    if not arguments:
        print('Please enter a target.')
    return arguments



def scan(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request = broadcast/arp_req
    answered = scapy.srp(arp_request, timeout=1, verbose=False)[0]
    result = []
    for element in answered:
        result.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
    return result



def print_scan(scan):
    print('IP\t\t\tMAC Address')
    for e in scan:
        print(e['ip'] + '\t\t' + e['mac'])


arguments = get_arguments()
print_scan(scan(arguments.target))