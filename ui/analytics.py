import matplotlib.pyplot as plt
import streamlit as st

class AnalyticsRenderer:
    @staticmethod
    def render_chart(df):
        if df.empty:
            st.info("No sessions recorded yet. Complete a session to see analytics.")
            return

        # Filter for Work sessions
        work_df = df[df['session_type'] == 'Work'].copy()
        
        if work_df.empty:
            st.info("No 'Work' sessions recorded yet.")
            return

        # Logic
        work_df['date'] = work_df['timestamp'].dt.date
        daily_counts = work_df.groupby('date').size()

        # Visualization Settings
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 3))
        fig.patch.set_facecolor('#1e1e1e') 
        ax.set_facecolor('#1e1e1e')
        
        # Plotting
        daily_counts.plot(kind='bar', ax=ax, color='#64b5f6')
        
        # Styling
        ax.set_title("Daily Productivity", color='#e0e0e0')
        ax.set_ylabel("Pomodoros", color='#e0e0e0')
        ax.tick_params(colors='#e0e0e0')
        ax.spines['bottom'].set_color('#444444')
        ax.spines['left'].set_color('#444444')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        st.pyplot(fig)