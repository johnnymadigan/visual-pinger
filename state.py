import threading
import streamlit as st
from threading import Thread

class TracerouteState:
    def __init__(self):
        self._curr_thread: Thread = None
        self._kill_flag: bool = False
        self._lock = threading.Lock()

    @property
    def kill_flag(self):
        with self._lock:
            return self._kill_flag
    
    @property
    def curr_thread(self):
        with self._lock:
            return self._curr_thread
        
    @property
    def is_curr_thread_alive(self):
        return True if self._curr_thread and self._curr_thread.is_alive() else False

    @kill_flag.setter
    def set_kill_flag(self, val: bool):
        with self._lock:
            self._kill_flag = val

    @curr_thread.setter
    def set_curr_thread(self, val: Thread | None):
        with self._lock:
            self._curr_thread = val


def get_traceroute_state() -> TracerouteState:
    """
    - Persists object in session state.
    - If object does not exist yet, it will be initialised.
    """
    
    key = 'traceroute_state'

    if key not in st.session_state:
        st.session_state[key] = TracerouteState()
    return st.session_state[key]
