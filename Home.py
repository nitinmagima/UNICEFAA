import streamlit as st

# — App config —
st.set_page_config(
    page_title="UNICEF Cyclone Impact Explorer",
    page_icon="🌪️",
    layout="wide"
)

# Welcome Page
st.title("Welcome to UNICEF Cyclone Impact Explorer 🌪️")

# Introduction
st.markdown("""
### About This Tool
This interactive platform helps analyze and understand cyclone impacts, with a focus on child-centric risk assessment and preparedness planning.

### Key Features
- **Historical Analysis**: Explore past cyclone events and their impacts
- **Forward-Looking Scenarios**: Model potential future impacts
- **Multi-Hazard Assessment**: Analyze combined effects of wind, surge, and rainfall
- **Child-Centric Focus**: Special attention to impacts on children and educational facilities

### Getting Started
1. Navigate to "Defining Risk and Establishing A Crisis Timeline" to begin your analysis
2. Choose between Hazard, Exposure, and Vulnerability assessments
3. Explore historical data or model future scenarios

### Data Sources
- Historical cyclone tracks
- Administrative boundaries
- Population data
- Infrastructure locations
- Vulnerability assessments

### Support
For technical support or questions, please contact the development team.
""")

# Add some visual elements
col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Historical Analysis**\n\nExplore past cyclone events and their impacts on communities.")

with col2:
    st.warning("**Risk Assessment**\n\nEvaluate current vulnerabilities and exposure levels.")

with col3:
    st.success("**Future Planning**\n\nModel potential scenarios and plan for resilience.") 