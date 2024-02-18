#!venv/bin/python3

import threading
import streamlit as st
import folium # port of Leaflet (JS)
from utils import traceroute
from state import get_traceroute_state
from streamlit_folium import folium_static


def get_hop_coordinates(destination):
    # As streamlit constantly re-renders page to reflect changes, we lose all global state
    # Solution to persist state? store and retrieve from Session Storage
    # Make sure to fetch the state obj to get the latest values
    
    # IMPORTANT: ensure state is initialised before accessing
    get_traceroute_state()

    while get_traceroute_state().is_curr_thread_alive:
        if get_traceroute_state().kill_flag == False:
            get_traceroute_state().set_kill_flag = True

    ip_list: list[str] = [] # pass as ref so thread func can update 
    thread = threading.Thread(target=traceroute, args=(destination, get_traceroute_state(), ip_list,), daemon=True)

    get_traceroute_state().set_kill_flag = False
    get_traceroute_state().set_curr_thread = thread

    thread.start()
    thread.join()

    return ip_list

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

    st.text("www.hackthissite.org")
    st.text("this app uses Scapy which requires elevated priviledges, please run app with sudo")

    # -27.57543631422662, 153.09408200000001
    # -27.46871248213641, 153.02122023782255
    # coordinates = [
    #     {'lat': 40.7128, 'lon': -74.0060},  # New York City
    #     {'lat': 34.0522, 'lon': -118.2437}  # Los Angeles
    # ]

    # st.map(coordinates)

    # map = folium.Map(location=[coordinates[0]['lat'], coordinates[0]['lon']], zoom_start=4)

    # for coord in coordinates:
    #     folium.Marker(location=[coord['lat'], coord['lon']]).add_to(map)

    # folium.PolyLine(locations=[[coord['lat'], coord['lon']] for coord in coordinates], color='blue').add_to(map)



    # Create a Folium Map with Mapbox tiles
    m = folium.Map(
        location=[40.7128, -74.0060],  # New York City coordinates
        zoom_start=1.5,
        tiles='OpenStreetMap',
    )

    # Add markers for the two points
    folium.Marker([40.7128, -74.0060], popup='New York City').add_to(m)
    folium.Marker([34.0522, -118.2437], popup='Los Angeles').add_to(m)
    folium.Marker([-27.5754, 153.0940], popup='Eight Mile Plains').add_to(m)

    # Connect the two points with a line
    folium.PolyLine(locations=[[40.7128, -74.0060], [34.0522, -118.2437]], color='blue').add_to(m)
    folium.PolyLine(locations=[[-27.5754, 153.0940], [34.0522, -118.2437]], color='blue').add_to(m)

    dst = st.text_input("IP or web address here")
    if dst and not dst.isspace():
        st.text(get_hop_coordinates(dst))

    # Render the map
    folium_static(m)

if __name__ == "__main__":
    main()