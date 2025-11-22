import streamlit as st
from config.settings import *

class TimerManager:
    @staticmethod
    def initialize_state():
        if 'timer_running' not in st.session_state:
            st.session_state.timer_running = False
        if 'time_left' not in st.session_state:
            st.session_state.time_left = WORK_TIME_MIN * 60
        if 'current_phase' not in st.session_state:
            st.session_state.current_phase = "Work"
        if 'sessions_completed' not in st.session_state:
            st.session_state.sessions_completed = 0

    @staticmethod
    def format_time(seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    @staticmethod
    def get_next_duration(current_sessions):
        """Determines duration based on cycle logic."""
        # If we just finished 4 sessions, take long break
        if current_sessions > 0 and current_sessions % SESSIONS_BEFORE_LONG_BREAK == 0:
            return "Long Break", LONG_BREAK_MIN * 60
        else:
            return "Short Break", SHORT_BREAK_MIN * 60

    @staticmethod
    def reset():
        st.session_state.timer_running = False
        st.session_state.current_phase = "Work"
        st.session_state.sessions_completed = 0
        st.session_state.time_left = WORK_TIME_MIN * 60