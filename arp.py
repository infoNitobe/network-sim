from scapy.all import *

class Arp:

    def __init__(self):
        self.dst_ip = "192.168.10.106"  # destination ip address. Get the mac address corresponding to this ip address.
    
    def send_arp_request(self, additionalSize=0):
        #dst="ff~ff" indicates broadcast
        #op="who-has" indicates an arp request
        arp_pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op="who-has", pdst=self.dst_ip)
        # Add data of specified size to the end of arp
        arp_pkt = arp_pkt / ("\x01" * additionalSize)

        sendp(arp_pkt)  # ARPパケットの送信
        print("send arp packet")