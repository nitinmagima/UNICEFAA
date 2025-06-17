import streamlit as st
import geopandas as gpd
import pandas as pd
import os
import pydeck as pdk
import altair as alt
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static
import json
from geojson import load

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
    
    base_path = "/Users/majju/Downloads/UNTechWeek/data/boundaries/Bangladesh_Latest_-_Global_Administrative_Boundaries"
    file_name = admin_files.get(admin_level)
    
    if not file_name:
        st.error(f"Invalid admin level: {admin_level}")
        return None
        
    file_path = os.path.join(base_path, file_name)
    
    try:
        if not os.path.exists(file_path):
            if admin_level in ["Admin Level 2", "Admin Level 3", "Admin Level 4"]:
                st.warning(f"Data for {admin_level} is not available in the current version.")
                return None
            else:
                st.error(f"File not found: {file_path}")
                return None
                
        # Read the GeoJSON file using geojson
        with open(file_path, 'r') as f:
            geojson_data = json.load(f)
            
        # Convert to GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
        
        return gdf
        
    except Exception as e:
        st.error(f"Error loading {admin_level} boundary: {str(e)}")
        return None

def load_cyclone_track():
    track_path = "/Users/majju/Downloads/UNTechWeek/data/boundaries/CyclonePath/amphan_2020_track.geojson"
    if os.path.exists(track_path):
        gdf = gpd.read_file(track_path)
        # Convert to DataFrame with lat/lon columns
        df = pd.DataFrame({
            'latitude': gdf.geometry.y,
            'longitude': gdf.geometry.x
        })
        return df
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
        boundary_gdf = load_admin_boundary(admin_level)
        if boundary_gdf is None:
            if admin_level in ["Admin Level 0", "Admin Level 1"]:
                st.error(f"Could not load {admin_level} boundary data. Please ensure the data file exists.")
            # For other levels, the warning is already shown in load_admin_boundary

        # — 4. Load cyclone track —
        track_df = load_cyclone_track()
        if track_df is None:
            st.error("Could not load cyclone track data. Please ensure the data file exists.")

        # — 5. Map display —
        st.subheader("Primary Hazard: Cyclone Track")
        if boundary_gdf is not None and track_df is not None:
            # Create layers for the map
            boundary_layer = pdk.Layer(
                "GeoJsonLayer",
                data=boundary_gdf,
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

        # Secondary Hazard Section
        st.subheader("Secondary Hazards")
        st.markdown("""
        Secondary hazards include:
        - Storm Surge
        - Heavy Rainfall
        - Flooding
        - Landslides
        
        _Note: Secondary hazard data visualization will be implemented in future updates._
        """)
    
    # Forward-Looking Analysis Tab
    with forward_tab:
        st.header("Forward-Looking Cyclone Scenario Analysis")
        
        # Create sections using expandable containers
        with st.expander("1. Rigorous Threshold Estimation", expanded=True):
            st.markdown("""
            ### Extreme Value Distribution Analysis
            - Fit a Generalized Extreme Value (GEV) distribution to historical maxima
            - Smooth sampling noise and enable interpolation to any return period
            - Calibrate forecast ensemble spread against past events
            - Match percentile thresholds with real-world return periods
            """)
            
            # Placeholder for GEV fitting controls
            st.info("GEV distribution fitting controls will be implemented here.")
        
        with st.expander("2. Quantify Uncertainty", expanded=True):
            st.markdown("""
            ### Uncertainty Analysis
            - Monte Carlo simulation of ensemble data
            - Bootstrap analysis of historical records
            - Confidence intervals for thresholds (w<sub>T</sub>)
            - Error bars and uncertainty bands for exposure metrics
            """)
            
            # Placeholder for uncertainty analysis controls
            st.info("Uncertainty analysis controls will be implemented here.")
        
        with st.expander("3. Multi-Hazard Coupling", expanded=True):
            st.markdown("""
            ### Combined Hazard Analysis
            - Weight combined footprints by joint exceedance probability
            - Distinguish between:
              - High-wind only zones
              - High-surge only zones
              - Combined hazard zones
            """)
            
            # Placeholder for multi-hazard controls
            st.info("Multi-hazard coupling controls will be implemented here.")
        
        with st.expander("4. Dynamic Scenario Definition", expanded=True):
            st.markdown("""
            ### Customizable Scenarios
            - User-defined return periods
            - Custom threshold curve upload
            - Adaptable risk-tolerance levels
            """)
            
            # Placeholder for scenario definition controls
            st.info("Dynamic scenario controls will be implemented here.")
        
        with st.expander("5. Vulnerability Curves & Impact Functions", expanded=True):
            st.markdown("""
            ### Impact Assessment
            - Apply fragility/vulnerability curves
            - Map wind speed and flood depth to damage probability
            - Calculate expected loss metrics
            - Aggregate probabilities over exposure layers
            """)
            
            # Placeholder for vulnerability analysis controls
            st.info("Vulnerability analysis controls will be implemented here.")
        
        with st.expander("6. Sensitivity Analysis", expanded=True):
            st.markdown("""
            ### Parameter Sensitivity
            - Vary surge thresholds
            - Test population growth assumptions
            - Evaluate building code changes
            - Identify key drivers of child-exposure numbers
            """)
            
            # Placeholder for sensitivity analysis controls
            st.info("Sensitivity analysis controls will be implemented here.")
        
        with st.expander("7. Narrative & Decision Dashboard", expanded=True):
            st.markdown("""
            ### Actionable Insights
            - Auto-generated action statements
            - Scenario-based exposure estimates
            - Pre-positioning recommendations
            - Anticipatory planning guidance
            """)
            
            # Placeholder for dashboard controls
            st.info("Decision dashboard controls will be implemented here.")
        
        with st.expander("8. Automated Reporting & Alerts", expanded=True):
            st.markdown("""
            ### Real-time Monitoring
            - Near-real-time forecast integration
            - Automated threshold monitoring
            - Email/text alerts for country offices
            - Scenario summary generation
            """)
            
            # Placeholder for alert system controls
            st.info("Automated reporting controls will be implemented here.")

# Exposure Tab
with exposure_tab:
    st.header("Exposure Analysis")
    
    # Create sub-tabs for Exposure analysis
    infrastructure_tab, population_tab, secondary_hazards_tab = st.tabs([
        "1. Child-Centric Impact on Critical Infrastructure & Services",
        "2. Population Exposure",
        "3. Secondary Hazard & Compounding Vulnerabilities Analysis"
    ])
    
    # Critical Infrastructure Tab
    with infrastructure_tab:
        st.subheader("Child-Centric Impact on Critical Infrastructure & Services")
        
        # Infrastructure Type Selection
        infrastructure_type = st.selectbox(
            "Select Infrastructure Type",
            ["Schools", "Hospitals/Clinics", "Water Points"]
        )
        
        # Load and display infrastructure data
        st.markdown("""
        ### Infrastructure Exposure Assessment
        - Loading building footprints from UNICEF GIGA dataset
        - Filtering by facility type
        - Assessing exposure to hazard zones
        """)
        
        # Placeholder for infrastructure map
        st.info("Infrastructure exposure visualization will be implemented here.")
        
        # Exposure Statistics
        st.markdown("""
        ### Exposure Statistics
        | Metric | Value |
        |--------|-------|
        | Total Facilities | 0 |
        | Exposed Facilities | 0 |
        | % Exposed | 0% |
        """)
    
    # Population Exposure Tab
    with population_tab:
        st.subheader("Child Population Exposure")
        
        # Population Layer Selection
        population_layer = st.selectbox(
            "Select Population Layer",
            ["Under-5 Population", "School-Age Population (5-14)", "Total Child Population"]
        )
        
        # Population Exposure Analysis
        st.markdown("""
        ### Population Exposure Assessment
        - Loading high-resolution population raster
        - Calculating exposure within hazard zones
        - Aggregating by administrative units
        """)
        
        # Placeholder for population exposure map
        st.info("Population exposure visualization will be implemented here.")
        
        # Population Statistics
        st.markdown("""
        ### Population Statistics
        | Metric | Value |
        |--------|-------|
        | Total Children | 0 |
        | Exposed Children | 0 |
        | % Exposed | 0% |
        """)
    
    # Secondary Hazards Tab
    with secondary_hazards_tab:
        st.subheader("Secondary Hazard & Compounding Vulnerabilities Analysis")
        
        # Secondary Hazard Selection
        hazard_type = st.selectbox(
            "Select Secondary Hazard Type",
            ["Flood-Stagnant Water", "Landslide Susceptibility", "Contaminated Water Sources"]
        )
        
        # Vulnerability Indicators
        st.markdown("""
        ### Child Vulnerability Indicators
        - Vaccination coverage
        - Acute malnutrition prevalence
        - Poverty/asset-ownership proxies
        """)
        
        # Vulnerability Index Parameters
        st.subheader("Vulnerability Index Parameters")
        col1, col2, col3 = st.columns(3)
        with col1:
            malnutrition_weight = st.slider("Malnutrition Weight", 0.0, 1.0, 0.4)
        with col2:
            vaccination_weight = st.slider("Vaccination Weight", 0.0, 1.0, 0.3)
        with col3:
            poverty_weight = st.slider("Poverty Weight", 0.0, 1.0, 0.3)
        
        # Risk Analysis
        st.subheader("Child-Centered Risk Analysis")
        
        # Risk Metrics
        st.markdown("""
        ### Risk Metrics by Secondary Hazard
        
        | Hazard Type | Risk Metric | Value |
        |-------------|-------------|-------|
        | Cholera Risk | Children in contaminated zones | 0 |
        | Vector-Borne Disease | Children in standing water zones | 0 |
        | Landslide Risk | Children in high susceptibility areas | 0 |
        """)
        
        # Actionable Insights
        st.subheader("Actionable Insights")
        st.markdown("""
        ### Recommended Actions
        - Pre-position water purification kits in high-risk areas
        - Mobilize mobile health teams to malnutrition hotspots
        - Deploy emergency response teams to landslide-prone areas
        """)
        
        # Interactive Map
        st.subheader("Risk Visualization")
        st.info("Interactive map showing secondary hazards and vulnerability index will be implemented here.")
        
        # Detailed Analysis
        with st.expander("Detailed Analysis Parameters", expanded=False):
            st.markdown("""
            ### Analysis Parameters
            - Standing water persistence threshold: 3 days
            - Landslide susceptibility classification:
              - High: > 0.7
              - Medium: 0.4-0.7
              - Low: < 0.4
            - Vulnerability index normalization: Min-Max scaling
            """)

# Add UNICEF footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    © 2025 UNICEF. All rights reserved. This application is part of UNICEF's efforts to improve disaster preparedness and response.
</div>
""", unsafe_allow_html=True) 