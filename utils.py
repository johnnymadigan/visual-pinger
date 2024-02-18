import socket
from scapy.all import *
from scapy.layers.inet import IP, UDP
from state import TracerouteState

def traceroute(destination: str, state: TracerouteState, ip_list: list[str], max_hops=30, timeout=2) -> list[str]:
    """
    Simple clone of traceroute, modifies the given IP list as the route is traced
    """

    dst_ip = destination

    if not is_valid_ipv4(destination):
        dst_ip = dns_resolve_host(destination)
    
    if not dst_ip:
        print("✘ Invalid destination")
        return None
    
    print(f"Tracing route to {dst_ip}")
    ICMP_dst_reached_type = 0
    ttl = 1
        
    while state.kill_flag == False and ttl <= max_hops:
        # Create the packet matching traceroute's packets (UDP on port 33434)
        udp_segment = UDP(dport=33434)
        ip_packet = IP(dst=dst_ip, ttl=ttl)
        packet = ip_packet / udp_segment # combine, not division
 
        # SR1 = send and recieve 1 (packet)
        reply = sr1(packet, timeout=timeout, verbose=0)
 
        if reply is None:
            ip_list.append("Unknown")
            print(f"✔ Hop #{ttl}:\tUnknown")
        elif reply.type == ICMP_dst_reached_type or reply.src == dst_ip:
            ip_list.append(str(reply.src))
            print(f"✔ Hop #{ttl}:\t{reply.src}")
            print("✔ Destination reached, stopping trace")
            break
        else:
            # Intermediate hop
            ip_list.append(str(reply.src))
            print(f"✔ Hop #{ttl}:\t{reply.src}")
 
        ttl += 1

    if state.kill_flag == True:
        print("✘ Killing trace")
    else:
        print(f"✘ Destination unreachable within max hops of {max_hops}")

def dns_resolve_host(target: str):
    """
    Attempt to DNS resolve the IP, returning the IP or None
    """
    try:
        return socket.gethostbyname(target)
    except:
        return None
    
def is_valid_ipv4(ip: str | None):
    """
    Checks if an IP is in a valid format
    """
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False

def convert_ip_to_geoloc():
    print("todo")