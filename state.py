import streamlit as st
from app_types import TracerouteState

def get_traceroute_state() -> TracerouteState:
    """
    - Persists object in session state.
    - If object does not exist yet, it will be initialised.
    """
    
    key = 'traceroute_state'

    if key not in st.session_state:
        st.session_state[key] = TracerouteState()
    return st.session_state[key]
