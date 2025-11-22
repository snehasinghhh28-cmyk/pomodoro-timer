import streamlit as st
import time
from config.settings import *
from database.db_handler import DatabaseHandler
from ui.styles import get_custom_css
from ui.analytics import AnalyticsRenderer
from core.timer_logic import TimerManager

# 1. Setup & Config
st.set_page_config(page_title="FocusFlow Pro", page_icon="🍅", layout="centered")
st.markdown(get_custom_css(), unsafe_allow_html=True)

# 2. Initialize Modules
db = DatabaseHandler()
timer_logic = TimerManager()
timer_logic.initialize_state()

# 3. Header & Metrics
st.title("🍅 FocusFlow Pro")
col1, col2, col3 = st.columns(3)
col1.metric("Phase", st.session_state.current_phase)
col2.metric("Cycle Progress", f"{st.session_state.sessions_completed % 4}/4")
col3.metric("Total Focus", st.session_state.sessions_completed)

# 4. Timer UI
timer_container = st.empty()
timer_container.markdown(
    f"<div class='big-font'>{timer_logic.format_time(st.session_state.time_left)}</div>", 
    unsafe_allow_html=True
)

# 5. Controls
b1, b2, b3, b4 = st.columns(4)
start_btn = b1.button("Start/Pause")
reset_btn = b2.button("Reset")
skip_btn = b3.button("Skip Phase")
undo_btn = b4.button("Undo Last")

if start_btn:
    st.session_state.timer_running = not st.session_state.timer_running

if reset_btn:
    timer_logic.reset()
    st.rerun()

if undo_btn:
    # CRUD Operation: Delete
    db.delete_latest_session()
    st.session_state.sessions_completed = max(0, st.session_state.sessions_completed - 1)
    st.success("Last session removed.")
    time.sleep(1)
    st.rerun()

# 6. Main Loop
if st.session_state.timer_running:
    while st.session_state.time_left > 0 and st.session_state.timer_running:
        time.sleep(1)
        st.session_state.time_left -= 1
        timer_container.markdown(
            f"<div class='big-font'>{timer_logic.format_time(st.session_state.time_left)}</div>", 
            unsafe_allow_html=True
        )

    # Phase Complete Logic
    if st.session_state.time_left == 0:
        st.session_state.timer_running = False
        
        if st.session_state.current_phase == "Work":
            db.save_session("Work", WORK_TIME_MIN * 60)
            st.session_state.sessions_completed += 1
            
            # Determine next break type
            next_phase, duration = timer_logic.get_next_duration(st.session_state.sessions_completed)
            st.session_state.current_phase = next_phase
            st.session_state.time_left = duration
            st.balloons()
            
        else:
            # Break is over, back to work
            st.session_state.current_phase = "Work"
            st.session_state.time_left = WORK_TIME_MIN * 60
            
        st.rerun()

if skip_btn:
    st.session_state.time_left = 0
    st.session_state.timer_running = True # Force loop to catch 0
    st.rerun()

# 7. Analytics Section
st.markdown("---")
st.subheader("📊 Productivity Analytics")
df = db.fetch_all_sessions()
AnalyticsRenderer.render_chart(df)