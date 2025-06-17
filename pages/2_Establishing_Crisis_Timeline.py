import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import geopandas as gpd
import pydeck as pdk

# — App config —
st.set_page_config(page_title="UNICEF Cyclone Impact Explorer", layout="wide")

# Add UNICEF logo
col1, col2 = st.columns([0.85, 0.15])
with col2:
    st.image("assets/UNICEF_Logo.png", width=150)

st.title("Establishing A Crisis Timeline")

# Add custom CSS for timeline
st.markdown("""
    <style>
    .timeline-section {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .timeline-item {
        margin-bottom: 15px;
    }
    .timeline-title {
        font-weight: bold;
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# Timeline Phases
PHASES = [
    "Preparedness",
    "Monitoring",
    "Recovery"
]

# Sample event data (replace with actual data loading)
events_data = {
    "Phase": [
        "Preparedness",
        "Preparedness",
        "Preparedness",
        "Preparedness",
        "Preparedness",
        "Preparedness",
        "Preparedness",
        "Preparedness",
        "Preparedness",
        "Preparedness",
        "Preparedness",
        "Preparedness",
        "Monitoring",
        "Monitoring",
        "Monitoring",
        "Monitoring",
        "Monitoring",
        "Monitoring",
        "Monitoring",
        "Recovery",
        "Recovery",
        "Recovery",
        "Recovery",
        "Recovery"
    ],
    "Event": [
        "ECMWF SEAS5 Seasonal Forecast Released",
        "SEAS5 Mid-season Update",
        "MJO Pulse Detected",
        "S2S Models Flag Elevated Risk",
        "Track Forecast Day 7",
        "Track Forecast Day 3",
        "90th-percentile Wind Speed Alert",
        "Community Evacuation Drills",
        "Relief Consignment Departs",
        "District-level Evacuation Orders",
        "72-hour Landfall Warning",
        "Landfall Occurs",
        "First Damage Assessment Report",
        "Floodwaters Begin Receding",
        "Satellite Flood Extent Update",
        "Cholera Risk Zones Identified",
        "Drone Survey of Road Blockages",
        "Mobile Lab Testing Results",
        "Vector-borne Disease Window Opens",
        "School Reconstruction Launch",
        "After-Action Review Workshop",
        "Three-month Recovery Check-in",
        "Major Infrastructure Restoration",
        "Transition to Resilience Programming"
    ],
    "Timestamp": [
        "2020-04-01 00:00 UTC",
        "2020-04-15 00:00 UTC",
        "2020-05-01 00:00 UTC",
        "2020-05-01 12:00 UTC",
        "2020-05-10 00:00 UTC",
        "2020-05-17 00:00 UTC",
        "2020-05-11 00:00 UTC",
        "2020-05-13 00:00 UTC",
        "2020-05-16 00:00 UTC",
        "2020-05-12 00:00 UTC",
        "2020-05-17 00:00 UTC",
        "2020-05-19 00:00 UTC",
        "2020-05-19 18:00 UTC",
        "2020-05-22 00:00 UTC",
        "2020-05-23 00:00 UTC",
        "2020-05-24 00:00 UTC",
        "2020-05-23 00:00 UTC",
        "2020-05-25 00:00 UTC",
        "2020-05-27 00:00 UTC",
        "2020-06-01 00:00 UTC",
        "2020-07-15 00:00 UTC",
        "2020-08-01 00:00 UTC",
        "2020-12-01 00:00 UTC",
        "2020-12-01 12:00 UTC"
    ],
    "Location": [
        "Bay of Bengal",
        "Bay of Bengal",
        "Indian Ocean",
        "Bay of Bengal",
        "Predicted Path",
        "Impact Zone",
        "Cox's Bazar",
        "Satkhira and Khulna",
        "Dhaka to Khulna",
        "Sundarbans Region",
        "Coastal Areas",
        "Landfall Zone",
        "Multiple Districts",
        "Low-lying Polders",
        "Flood-affected Areas",
        "Contaminated Areas",
        "Road Network",
        "Water and Soil Samples",
        "Risk Zones",
        "Affected Schools",
        "UNICEF HQ",
        "Affected Communities",
        "Major Infrastructure",
        "Program Areas"
    ],
    "Source": [
        "ECMWF SEAS5",
        "ECMWF SEAS5",
        "MJO Monitoring",
        "S2S Models",
        "ECMWF Track",
        "ECMWF Track",
        "Ensemble Model",
        "Field Teams",
        "UNICEF Logistics",
        "ECMWF Track",
        "Regional Model",
        "Weather Stations",
        "Rapid Assessment",
        "Field Reports",
        "Satellite Data",
        "Health Assessment",
        "Drone Survey",
        "Mobile Lab",
        "Health Teams",
        "Education Team",
        "Stakeholders",
        "Monitoring Team",
        "Infrastructure Team",
        "Program Team"
    ],
    "Alert_Level": [
        "Info",
        "Info",
        "Watch",
        "Warning",
        "Warning",
        "Alert",
        "Alert",
        "Warning",
        "Info",
        "Alert",
        "Critical",
        "Critical",
        "Critical",
        "Warning",
        "Warning",
        "Alert",
        "Warning",
        "Info",
        "Alert",
        "Info",
        "Info",
        "Info",
        "Info",
        "Info"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(events_data)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Create tabs for different views
timeline_tab = st.tabs(["Timeline View"])[0]

# Timeline View Tab
with timeline_tab:
    # Main Timeline Overview
    st.header("Timeline Overview")
    
    # Create Gantt chart data with category information
    gantt_data = pd.DataFrame([
        {"Phase": "Seasonal Outlook", "Start": 0, "End": 2, "Description": "Above-normal cyclone season forecast", "Category": "Preparation"},
        {"Phase": "Sub-Seasonal Alerts", "Start": 2, "End": 4, "Description": "Early warning systems activation", "Category": "Preparation"},
        {"Phase": "Forecast Updates", "Start": 4, "End": 6, "Description": "Daily track forecasts", "Category": "Preparation"},
        {"Phase": "Early Warning", "Start": 6, "End": 7, "Description": "Automated alerts", "Category": "Preparation"},
        {"Phase": "Community Engagement", "Start": 7, "End": 8, "Description": "Evacuation drills", "Category": "Preparation"},
        {"Phase": "Logistics Preparation", "Start": 8, "End": 9, "Description": "Relief supplies mobilization", "Category": "Preparation"},
        {"Phase": "Medium-Range Forecasts", "Start": 9, "End": 10, "Description": "Landfall predictions", "Category": "Preparation"},
        {"Phase": "Short-Range Nowcast", "Start": 10, "End": 11, "Description": "Final warnings", "Category": "Preparation"},
        {"Phase": "Impact Phase", "Start": 11, "End": 12, "Description": "Landfall and assessment", "Category": "Monitoring"},
        {"Phase": "Secondary Hazards", "Start": 12, "End": 13, "Description": "Flooding and disease risks", "Category": "Monitoring"},
        {"Phase": "Response & Monitoring", "Start": 13, "End": 14, "Description": "Resource deployment", "Category": "Monitoring"},
        {"Phase": "Recovery & Restoration", "Start": 14, "End": 16, "Description": "Long-term rebuilding", "Category": "Recovery"}
    ])

    # Create the Gantt chart
    gantt_chart = alt.Chart(gantt_data).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        cornerRadiusBottomLeft=3,
        cornerRadiusBottomRight=3
    ).encode(
        y=alt.Y('Phase:N', sort='-x', title=''),
        x=alt.X('Start:Q', title='Timeline'),
        x2='End:Q',
        color=alt.Color('Category:N', scale=alt.Scale(
            domain=['Preparation', 'Monitoring', 'Recovery'],
            range=['#2E86C1', '#E67E22', '#27AE60']
        )),
        tooltip=['Phase', 'Description', 'Category']
    ).properties(
        height=400,
        width=800,
        title='Crisis Timeline'
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).configure_legend(
        orient='top',
        title=None
    )

    # Display the Gantt chart
    st.altair_chart(gantt_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Sections
    st.header("Detailed Timeline")
    
    # Preparedness Section
    with st.expander("Preparedness Phase", expanded=False):
        st.markdown("""
        ### Forecast Horizons:
        
        1. **Seasonal Outlook (Months in Advance)**
        * **When?** At the start of the Bay of Bengal cyclone season (roughly April and again in October).
        * **What?** ECMWF's seasonal forecasting system (SEAS5) gives you a heads-up 3–6 months out.
        """)
        
        # Filter for seasonal events
        seasonal_events = df[(df['Phase'] == 'Preparedness') & (df['Event'].str.contains('Seasonal'))]
        if not seasonal_events.empty:
            st.info(f"🔔 **Current Alert**: {seasonal_events.iloc[-1]['Event']}")
            st.map()
        
        st.markdown("""
        2. **Sub-Seasonal to Seasonal (2–6 Weeks)**
        * **When?** As large-scale patterns (e.g. MJO, monsoon breaks) evolve.
        * **What?** Dynamical S2S forecasts signal periods of elevated cyclone risk.
        """)
        
        # Filter for sub-seasonal events
        subseasonal_events = df[(df['Phase'] == 'Preparedness') & (df['Event'].str.contains('MJO|Risk Period'))]
        if not subseasonal_events.empty:
            st.warning(f"⚠️ **Current Alert**: {subseasonal_events.iloc[-1]['Event']}")
            st.map()
        
        st.markdown("""
        3. **Medium-Range Track Forecasts (5–10 Days)**
        * **When?** Once a tropical disturbance organizes into a named system.
        * **What?** Track forecasts with decreasing uncertainty:
            * **Day 7:** broad "cone of uncertainty"
            * **Day 5:** errors shrink to ~200 km
            * **Day 3:** errors closer to ~100 km
        """)
        
        # Filter for medium-range events
        medium_range_events = df[(df['Phase'] == 'Preparedness') & (df['Event'].str.contains('Track Forecast'))]
        if not medium_range_events.empty:
            st.error(f"🚨 **Current Alert**: {medium_range_events.iloc[-1]['Event']}")
            st.map()
        
        st.markdown("""
        4. **Short-Range Nowcast (0–3 Days)**
        * **When?** 72 hours to landfall.
        * **What?** High-resolution regional models and satellite/radar updates.
        """)
        
        # Filter for short-range events
        short_range_events = df[(df['Phase'] == 'Preparedness') & (df['Event'].str.contains('Intensity|Surge'))]
        if not short_range_events.empty:
            st.error(f"🚨 **Current Alert**: {short_range_events.iloc[-1]['Event']}")
            st.map()
    
    # Monitoring Section
    with st.expander("Monitoring Phase", expanded=False):
        st.markdown("""
        * Real-time impact monitoring
        * Damage assessment
        * Critical infrastructure status
        """)
        
        # Filter for monitoring events
        monitoring_events = df[df['Phase'] == 'Monitoring']
        if not monitoring_events.empty:
            st.error("🚨 **Current Alert**: " + monitoring_events.iloc[-1]['Event'])
            st.map()
    
    # Recovery Section
    with st.expander("Recovery Phase", expanded=False):
        st.markdown("""
        * Emergency response operations
        * Infrastructure restoration
        * Community recovery
        """)
        
        # Filter for recovery events
        recovery_events = df[df['Phase'] == 'Recovery']
        if not recovery_events.empty:
            st.warning("⚠️ **Current Alert**: " + recovery_events.iloc[-1]['Event'])
            st.map()

# Add UNICEF footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    © 2025 UNICEF. All rights reserved. This application is part of UNICEF's efforts to improve disaster preparedness and response.
</div>
""", unsafe_allow_html=True) 