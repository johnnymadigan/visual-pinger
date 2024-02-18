import json
import socket
import requests
from scapy.all import *
from scapy.layers.inet import IP, UDP
from app_types import TracerouteState, GeoLocation

def traceroute(destination: str, state: TracerouteState, ip_hop_list: list[str], max_hops=30, timeout=2) -> list[str]:
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
            ip_hop_list.append("*")
            print(f"✔ Hop #{ttl}:\tUnknown")
        elif reply.type == ICMP_dst_reached_type or reply.src == dst_ip:
            ip_hop_list.append(str(reply.src))
            print(f"✔ Hop #{ttl}:\t{reply.src}")
            print("✔ Destination reached, stopping trace")
            break
        else:
            # Intermediate hop
            ip_hop_list.append(str(reply.src))
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

def get_geoloc(ip: str) -> GeoLocation:
    """
    - Extracts the geo location (lon + lat) from an IP.
    - Uses public API: https://reallyfreegeoip.org/
    """
    if not is_valid_ipv4(ip):
        print(f"✘ IP '{ip}' is not in a valid IPv4 format")
        return None

    res = requests.get(f"https://reallyfreegeoip.org/json/{ip}")

    data = {}
    try:
        data = res.json()
    except json.JSONDecodeError as e:
        print(f"✘ Unable to decode JSON: {e}")
        return None

    lon = data.get("longitude")
    lat = data.get("latitude")
    name: list[str | None] = [data.get("country_name"), data.get("region_name"), data.get("city")]
    name = ', '.join([i for i in name if i is not None and not i.isspace()])

    if lon is None or lat is None:
        print(f"✘ No geo location information available for IP '{ip}'")
        return None
    
    print(f"✔ IP '{ip}' is located at longitude '{lon}', latitude '{lat}'")
    return GeoLocation(lon, lat, name)
