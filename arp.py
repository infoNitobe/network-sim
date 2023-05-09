from scapy.all import *

class Arp:

    def __init__(self):
        self.recipient_ip = "192.168.10.106"  # destination ip address. Get the mac address corresponding to this ip address.
        self.sender_ip = "127.0.0.1"  # destination ip address. Get the mac address corresponding to this ip address.
    
    def send_arp_request(self, additionalSize=0):
        #dst="ff~ff" indicates broadcast
        #op="who-has" indicates an arp request
        arp_pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op="who-has", pdst=self.recipient_ip)
        # Add data of specified size to the end of arp
        arp_pkt = arp_pkt / ("\x01" * additionalSize)

        sendp(arp_pkt)  # send ARP request.
        print("send arp packet")

    def arp_reply(self, pkt):
        # Handle ARP requests
        arp = pkt[ARP]
        if arp.op == 1:
            ether = pkt[Ether]
            if arp.pdst == self.recipient_ip:
                # todo: Correct the subsequent processing.
                print("Received ARP request from " + ether.src + " for " + arp.pdst)
                ether.dst, ether.src = ether.src, ether.dst
                arp.op = 2 # ARP reply
                arp.hwdst, arp.pdst = arp.hwsrc, arp.psrc
                arp.hwsrc = get_if_hwaddr(conf.iface)
                arp.psrc = '192.168.0.1'
                del pkt[ICMP] # remove ICMP layer if present
                pkt[Ether] = ether
                pkt[ARP] = arp
                sendp(pkt, iface=conf.iface)
                print("Sent ARP reply to " + ether.src + " for " + arp.pdst)
            else:
                print("IP is not correct.")
        else:
            print("not ARP request.")