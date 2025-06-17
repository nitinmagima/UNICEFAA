import streamlit as st
import pandas as pd
import os
import pydeck as pdk
import altair as alt
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static
import json
from pathlib import Path

# Data loading functions
def load_admin_boundary(admin_level):
    # Map admin levels to file names
    admin_files = {
        "Admin Level 0": "adm0.geojson",
        "Admin Level 1": "adm1.geojson",
        "Admin Level 2": "adm2.geojson",
        "Admin Level 3": "adm3.geojson",
        "Admin Level 4": "adm4.geojson"
    }
    
    base_path = Path("/Users/majju/Downloads/UNTechWeek/data/boundaries/Bangladesh_Latest_-_Global_Administrative_Boundaries")
    file_name = admin_files.get(admin_level)
    
    if not file_name:
        st.error(f"Invalid admin level: {admin_level}")
        return None
        
    file_path = base_path / file_name
    
    try:
        if not file_path.exists():
            if admin_level in ["Admin Level 2", "Admin Level 3", "Admin Level 4"]:
                st.warning(f"Data for {admin_level} is not available in the current version.")
                return None
            else:
                st.error(f"File not found: {file_path}")
                return None
                
        # Read the GeoJSON file using json
        with open(file_path, 'r') as f:
            geojson_data = json.load(f)
            
        return geojson_data
        
    except Exception as e:
        st.error(f"Error loading {admin_level} boundary: {str(e)}")
        return None

def load_cyclone_track():
    track_path = Path("/Users/majju/Downloads/UNTechWeek/data/boundaries/CyclonePath/amphan_2020_track.geojson")
    if track_path.exists():
        with open(track_path, 'r') as f:
            track_data = json.load(f)
            
        # Extract coordinates from GeoJSON
        coordinates = []
        for feature in track_data['features']:
            coords = feature['geometry']['coordinates']
            coordinates.append({
                'longitude': coords[0],
                'latitude': coords[1]
            })
            
        return pd.DataFrame(coordinates)
    return None

# — App config —
st.set_page_config(page_title="UNICEF Cyclone Impact Explorer", layout="wide")

# Add UNICEF logo
col1, col2 = st.columns([0.85, 0.15])
with col2:
    st.image("assets/UNICEF_Logo.png", width=150)

st.title("Defining Cyclone Risk")

# Create tabs for the main sections
hazard_tab, exposure_tab = st.tabs([
    "Hazard",
    "Exposure"
])

# Hazard Tab
with hazard_tab:
    # Create sub-tabs for Hazard analysis
    historical_tab, forward_tab = st.tabs([
        "1. Historical Cyclone Analysis",
        "2. Forward-Looking Cyclone Scenario Analysis"
    ])
    
    # Historical Analysis Tab
    with historical_tab:
        st.header("Historical Cyclone Analysis")
        st.markdown(
            "Select which administrative boundary to use, "
            "and load the Cyclone Amphan track data."
        )

        # — 1. Cyclone selection —
        cyclone = st.selectbox(
            "Select Cyclone",
            ["Cyclone Amphan"]
        )

        # — 2. Admin level dropdown —
        admin_level = st.selectbox(
            "Select Admin level",
            ["Admin Level 0", "Admin Level 1", "Admin Level 2", "Admin Level 3", "Admin Level 4"]
        )

        # — 3. Load boundary data —
        boundary_data = load_admin_boundary(admin_level)
        if boundary_data is None:
            if admin_level in ["Admin Level 0", "Admin Level 1"]:
                st.error(f"Could not load {admin_level} boundary data. Please ensure the data file exists.")
            # For other levels, the warning is already shown in load_admin_boundary

        # — 4. Load cyclone track —
        track_df = load_cyclone_track()
        if track_df is None:
            st.error("Could not load cyclone track data. Please ensure the data file exists.")

        # — 5. Map display —
        st.subheader("Primary Hazard: Cyclone Track")
        if boundary_data is not None and track_df is not None:
            # Create layers for the map
            boundary_layer = pdk.Layer(
                "GeoJsonLayer",
                data=boundary_data,
                get_fill_color=[255, 0, 0, 50],  # Red with 50% opacity
                pickable=True,
                stroked=True,
                filled=True,
                extruded=False,
                line_width_min_pixels=1
            )
            
            track_layer = pdk.Layer(
                "ScatterplotLayer",
                data=track_df,
                get_position=['longitude', 'latitude'],
                get_color=[0, 0, 255],  # Blue
                get_radius=5000,  # Increased from 1000 to 5000
                pickable=True,
                stroked=True,
                filled=True,
                line_width_min_pixels=2
            )
            
            # Set the initial viewport
            view_state = pdk.ViewState(
                latitude=23.6850,  # Center of Bangladesh
                longitude=90.3563,
                zoom=6
            )
            
            # Create the deck.gl map
            deck = pdk.Deck(
                layers=[boundary_layer, track_layer],
                initial_view_state=view_state,
                map_style='mapbox://styles/mapbox/light-v9'
            )
            
            st.pydeck_chart(deck)
        else:
            st.warning("Please ensure both boundary and track data are available to display the map.")

# Add UNICEF footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    © 2025 UNICEF. All rights reserved. This application is part of UNICEF's efforts to improve disaster preparedness and response.
</div>
""", unsafe_allow_html=True) 