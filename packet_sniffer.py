import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
	scapy.sniff(iface=interface, store=False, prn=process_packet)

def process_packet(packet):
	print(packet.show())

sniff('enp0s31f6')