# UNICEF Cyclone Impact Explorer

A Streamlit application for analyzing and visualizing cyclone impacts, risk assessment, and anticipatory actions.

## Features

- Cyclone Risk Analysis
- Hazard and Exposure Analysis
- Anticipatory Action Planning
- Real-time Monitoring and Adaptation
- Interactive Maps and Visualizations

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run Home.py
   ```

## Project Structure

- `Home.py`: Main application entry point
- `pages/`: Contains individual pages for different features
  - `1_Defining_Risk.py`: Risk analysis and visualization
  - `2_Anticipatory_Actions.py`: Anticipatory action planning
  - `3_Anticipatory_Action_Chatbot.py`: Interactive chatbot for action planning
  - `4_Monitoring_Adaptation.py`: Real-time monitoring and adaptation

## Data

The application uses various data sources including:
- Administrative boundaries
- Cyclone track data
- Population data
- Infrastructure data

## Deployment

This application is deployed on Streamlit Cloud. Visit [streamlit.io](https://streamlit.io) to deploy your own version. 