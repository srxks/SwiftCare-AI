import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
from datetime import datetime

st.set_page_config(layout="wide")

def run_heart_rate_system():
    def render_monitor(bpm_value):
        monitor_html = f"""
        <style>
            .hr-monitor-box {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: #FF3366;
                font-family: 'Courier New', Courier, monospace;
                padding: 20px;
            }}
            .hr-label {{
                font-size: 2rem;
                font-weight: bold;
            }}
            .hr-value {{
                font-size: 10rem;
                font-weight: 900;
                line-height: 1;
                margin: 0;
            }}
        </style>
        <div class="hr-monitor-box">
            <div class="hr-label">BPM</div>
            <div class="hr-value">{bpm_value}</div>
        </div>
        """
        st.markdown(monitor_html, unsafe_allow_html=True)

    if 'heart_rate_df' not in st.session_state:
        st.session_state.heart_rate_df = pd.DataFrame(columns=["Time", "BPM"])

    if 'running' not in st.session_state:
        st.session_state.running = False

    st.title("Live Heart Rate Monitor")
    
    if st.button("Start/Stop Monitor"):
        st.session_state.running = not st.session_state.running

    col_chart, col_monitor = st.columns([4, 1.5])
    chart_placeholder = col_chart.empty()
    monitor_placeholder = col_monitor.empty()

    while st.session_state.running:
        curr_time = datetime.now().strftime("%I:%M:%S %p")
        curr_bpm = int(np.random.normal(75, 5))
        
        latest_row = pd.DataFrame({"Time": [curr_time], "BPM": [curr_bpm]})
        st.session_state.heart_rate_df = pd.concat([st.session_state.heart_rate_df, latest_row]).tail(30)
        
        with monitor_placeholder.container():
            render_monitor(curr_bpm)

        y_low = min(60, st.session_state.heart_rate_df["BPM"].min() - 5)
        y_high = max(90, st.session_state.heart_rate_df["BPM"].max() + 5)

        base = alt.Chart(st.session_state.heart_rate_df).encode(
            x=alt.X('Time:N', sort=None, axis=alt.Axis(labelAngle=-45)),
            y=alt.Y('BPM:Q', scale=alt.Scale(domain=[y_low, y_high])),
            tooltip=['Time', 'BPM']
        )

        line = base.mark_line(color='#FF3366', size=4, interpolate='monotone')
        points = base.mark_point(color='#FF3366', size=60, filled=True)
        
        hr_chart = (line + points).properties(height=500).interactive()

        chart_placeholder.altair_chart(hr_chart, use_container_width=True)
        
        time.sleep(1)

run_heart_rate_system()