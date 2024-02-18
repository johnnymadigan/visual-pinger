#!venv/bin/python3

import threading
import streamlit as st
import folium # port of Leaflet (JS)
from app_types import GeoLocation 
from state import get_traceroute_state
from utils import traceroute, get_geoloc
from streamlit_folium import folium_static

def get_ip_hop_list(destination):
    # As streamlit constantly re-renders page to reflect changes, we lose all global state
    # Solution to persist state? store and retrieve from Session Storage
    # Make sure to fetch the state obj to get the latest values
    
    # IMPORTANT: ensure state is initialised before accessing
    get_traceroute_state()

    while get_traceroute_state().is_curr_thread_alive:
        if get_traceroute_state().kill_flag == False:
            get_traceroute_state().set_kill_flag = True

    ip_hop_list: list[str] = [] # pass as ref so thread func can update 
    thread = threading.Thread(target=traceroute, args=(destination, get_traceroute_state(), ip_hop_list,), daemon=True)

    get_traceroute_state().set_kill_flag = False
    get_traceroute_state().set_curr_thread = thread

    thread.start()
    thread.join()

    return ip_hop_list

def main():
    print(r"""
        a speedrun project...
        ░▒▓███████▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░▒▓███████▓▒░  
        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓███████▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░  
        ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                                                            ...by Johnny Madigan                                                                         
    """)

    st.text('''
        a speedrun project...
        ░▒▓███████▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░▒▓███████▓▒░  
        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓███████▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░  
        ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                                                            ...by Johnny Madigan    
    ''')

    st.text("Try: www.hackthissite.org (137.74.187.102)")
    st.text("This app uses Scapy which requires elevated priviledges, please run app with sudo")

    # Create a Folium Map with Mapbox tiles
    map = folium.Map(
        location=[40.7128, -74.0060],  # New York City coordinates
        zoom_start=1.5,
        tiles='OpenStreetMap',
    )

    dst = st.text_input("IP or web address here")

    if dst and not dst.isspace():
        ip_hop_list: list[str] = get_ip_hop_list(dst)
        geo_loc_list: list[GeoLocation] = [] # TODO: need to add src ip (of user running as 127.0.0.1 loopback has no address) and maybe the destination if not included

        for ip in ip_hop_list:
            geo_loc = get_geoloc(ip)
            if geo_loc:
                geo_loc_list.append(geo_loc)
        
        st.text(geo_loc_list)

        for idx, geo_loc in enumerate(geo_loc_list):
          folium.Marker([geo_loc.lat, geo_loc.lon], popup=geo_loc.name).add_to(map)
          if idx != 0:
              folium.PolyLine(locations=[[geo_loc.lat, geo_loc.lon], [geo_loc_list[idx - 1].lat, geo_loc_list[idx - 1].lon]], color='blue').add_to(map) # TODO: randomise colors by rand index of a list of colours

        folium_static(map) # render

if __name__ == "__main__":
    main()
