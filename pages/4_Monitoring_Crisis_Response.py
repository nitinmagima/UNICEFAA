import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# — App config —
st.set_page_config(
    page_title="Monitoring Crisis Response",
    page_icon="📊",
    layout="wide"
)

# Add UNICEF logo
col1, col2 = st.columns([0.85, 0.15])
with col2:
    st.image("assets/UNICEF_Logo.png", width=150)

st.title("Monitoring & Adaptation System")

# Generate dummy data
def generate_dummy_data():
    # Time range for the last 7 days
    dates = pd.date_range(end=datetime.now(), periods=168, freq='h')
    
    # Generate shelter data
    shelter_data = pd.DataFrame({
        'timestamp': dates,
        'shelter_id': np.random.choice(['Shelter A', 'Shelter B', 'Shelter C'], size=168),
        'occupancy': np.random.randint(50, 100, size=168),
        'capacity': 100,
        'status': np.random.choice(['Operational', 'At Capacity', 'Needs Support'], size=168, p=[0.7, 0.2, 0.1])
    })
    
    # Generate stock data
    stock_data = pd.DataFrame({
        'timestamp': dates,
        'hub_id': np.random.choice(['Hub North', 'Hub South', 'Hub East'], size=168),
        'kits_available': np.random.randint(100, 500, size=168),
        'kits_distributed': np.random.randint(50, 200, size=168),
        'status': np.random.choice(['Adequate', 'Low Stock', 'Critical'], size=168, p=[0.6, 0.3, 0.1])
    })
    
    # Generate facility data
    facility_data = pd.DataFrame({
        'timestamp': dates,
        'facility_id': np.random.choice(['Clinic A', 'School B', 'Hospital C'], size=168),
        'operational_status': np.random.randint(60, 100, size=168),
        'type': np.random.choice(['Medical', 'Education', 'Health'], size=168),
        'status': np.random.choice(['Fully Operational', 'Partially Operational', 'Non-Operational'], size=168, p=[0.6, 0.3, 0.1])
    })
    
    # Generate WASH data
    wash_data = pd.DataFrame({
        'timestamp': dates,
        'location': np.random.choice(['Zone 1', 'Zone 2', 'Zone 3'], size=168),
        'kits_deployed': np.random.randint(20, 100, size=168),
        'cases_reported': np.random.randint(0, 10, size=168),
        'status': np.random.choice(['Normal', 'Alert', 'Critical'], size=168, p=[0.7, 0.2, 0.1])
    })
    
    return shelter_data, stock_data, facility_data, wash_data

# Generate the dummy data
shelter_data, stock_data, facility_data, wash_data = generate_dummy_data()

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs([
    "Data Streams & Ingestion",
    "Monitoring Dashboards",
    "Anomaly Detection",
    "Adaptive Feedback"
])

with tab1:
    st.header("Data Streams & Ingestion")
    
    # Display data streams table
    streams_data = {
        "Stream": [
            "Shelter & Evacuation Status",
            "Stock & Kit Usage",
            "Facility Functionality",
            "Health & WASH Indicators",
            "Infrastructure Access",
            "Secondary Hazard Alerts",
            "Community Feedback"
        ],
        "Source": [
            "Mobile check-in app (ODK/KOBO)",
            "Warehouse management system (ERP)",
            "In-field assessments (tablet forms)",
            "Clinic reporting (DHIS2); WASH surveys",
            "Crowd-sourced road reports; drone feeds",
            "Flood gauges; landslide sensors",
            "Chatbot logs; social-listening bots"
        ],
        "Frequency": [
            "Hourly",
            "Near-real-time",
            "Daily",
            "Daily",
            "Daily",
            "Continuous",
            "Continuous"
        ]
    }
    
    st.dataframe(pd.DataFrame(streams_data), use_container_width=True)

with tab2:
    st.header("Key Monitoring Dashboards")
    
    # Create columns for different metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Shelter Occupancy")
        # Calculate current occupancy
        current_occupancy = shelter_data.groupby('shelter_id')['occupancy'].last()
        fig = px.bar(
            current_occupancy,
            title="Current Shelter Occupancy",
            labels={'value': 'Occupancy %', 'shelter_id': 'Shelter'},
            color=current_occupancy.values,
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Stock & Kit Distribution")
        # Calculate current stock levels
        current_stock = stock_data.groupby('hub_id')['kits_available'].last()
        fig = px.bar(
            current_stock,
            title="Current Stock Levels by Hub",
            labels={'value': 'Kits Available', 'hub_id': 'Hub'},
            color=current_stock.values,
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Facility Status")
        # Calculate facility operational status
        current_facility = facility_data.groupby('facility_id')['operational_status'].last()
        fig = px.bar(
            current_facility,
            title="Facility Operational Status",
            labels={'value': 'Operational %', 'facility_id': 'Facility'},
            color=current_facility.values,
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Health & WASH Indicators")
        # Calculate WASH metrics
        current_wash = wash_data.groupby('location')['kits_deployed'].last()
        fig = px.bar(
            current_wash,
            title="WASH Kits Deployed by Zone",
            labels={'value': 'Kits Deployed', 'location': 'Zone'},
            color=current_wash.values,
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Anomaly Detection & Alerts")
    
    # Generate dummy alerts
    alerts = [
        {
            "type": "Shelter Spike Alert",
            "location": "Shelter A",
            "message": "Occupancy at 95% - Above threshold",
            "severity": "High",
            "timestamp": datetime.now() - timedelta(hours=2)
        },
        {
            "type": "Stock-out Warning",
            "location": "Hub South",
            "message": "Kit usage rate 25% above forecast",
            "severity": "Medium",
            "timestamp": datetime.now() - timedelta(hours=4)
        },
        {
            "type": "Facility Drop-off",
            "location": "Clinic A",
            "message": "Operational status at 75%",
            "severity": "High",
            "timestamp": datetime.now() - timedelta(hours=1)
        },
        {
            "type": "WASH Outbreak Trigger",
            "location": "Zone 2",
            "message": "5 cholera cases reported in last 24h",
            "severity": "Critical",
            "timestamp": datetime.now() - timedelta(hours=3)
        }
    ]
    
    # Display alerts
    for alert in alerts:
        with st.container():
            col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
            with col1:
                st.write(f"**{alert['type']}**")
            with col2:
                st.write(f"{alert['message']} at {alert['location']}")
            with col3:
                st.write(f"Severity: {alert['severity']}")
            st.divider()

with tab4:
    st.header("Adaptive Feedback Loop")
    
    # Create columns for different feedback sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daily Ops Sync")
        st.write("""
        - Review all dashboard panels
        - Acknowledge and clear alerts
        - Assign action owners
        - Update resource allocations
        """)
        
        st.subheader("Mid-Event Checkpoint")
        st.write("""
        - Day +3 and Day +7 post-landfall
        - Calculate Plan vs. Actual KPIs
        - Adjust resource allocations
        - Update response strategies
        """)
    
    with col2:
        st.subheader("Community Pulse")
        st.write("""
        - Monitor chatbot logs
        - Track emerging needs
        - Identify misinformation
        - Update communications
        """)
        
        st.subheader("Recovery Metrics")
        st.write("""
        - Weekly recovery tracking
        - Facility restoration progress
        - Infrastructure repair status
        - Service restoration rates
        """)

# Add a footer with last update time
st.divider()
st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") 