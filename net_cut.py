import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
	print(ip_packet.show())


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()