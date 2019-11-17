#!/usr/bin/env python3

import subprocess as sp
import optparse, re #optparse to parse arguments and re to search in regular expressions


def get_current_mac(interface):
    ifconfig_result = sp.check_output(["ifconfig", interface]).decode("utf-8")

    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] Could not get MAC address.")


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    options, arguments = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify new MAC, use --help for more info.")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    sp.call(["ifconfig", interface, "down"])
    sp.call(["ifconfig", interface, "hw", "ether", new_mac])
    sp.call(["ifconfig", interface, "up"])


options = get_arguments()
current_mac = str(get_current_mac(options.interface))
print("Current MAC = " + current_mac)

change_mac(options.interface, options.new_mac)

current_mac = str(get_current_mac(options.interface))
if current_mac == options.new_mac:
    print("[+] Successfully changed MAC address to " + current_mac)
else:
    print("[-] Could not change MAC address.")