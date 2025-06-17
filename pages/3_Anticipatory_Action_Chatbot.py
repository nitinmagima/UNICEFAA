import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import io
from typing import List, Dict, Any, Union, cast
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam
)

# Set the page configuration
st.set_page_config(
    page_title="🤖 Anticipatory Action AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add UNICEF logo
col1, col2 = st.columns([0.85, 0.15])
with col2:
    st.image("assets/UNICEF_Logo.png", width=150)

# Sidebar for OpenAI API Key and options
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    # Add radio buttons for predefined sections
    st.markdown("### Select a Focus Area")
    context_option = st.radio("Choose a section:", [
        "Development of Anticipatory Actions Interventions",
        "Associating Anticipatory Actions with Predictive Models"
    ])

    # Add copyright notice
    st.markdown(
        "<div style='text-align: center; font-size: 12px; color: gray;'>"
        "© UNICEF. All rights reserved."
        "</div>",
        unsafe_allow_html=True
    )

def main():
    st.title("🤖 Anticipatory Action AI Assistant")
    st.caption("AI Co-Pilot for Anticipatory Actions and Stakeholder Engagement")
    
    st.markdown(""" 
    ### Welcome to the Anticipatory Action Assistant!
    
    This AI assistant helps you with:
    - **Anticipatory Actions Development**: Guidance on creating effective interventions
    - **Predictive Model Integration**: Help with linking actions to forecast models
    - **Stakeholder Engagement**: Support for governance and coordination
    - **SOP Management**: Assistance with standard operating procedures
    - **Role-Based Guidance**: Clear instructions for different stakeholders
    
    #### How to use:
    1. Enter your OpenAI API Key in the sidebar
    2. Select your focus area from the sidebar options
    3. Upload any relevant documents (optional)
    4. Start chatting with the AI assistant
    
    For support, please contact the development team.
    """)

if __name__ == "__main__":
    main()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": (
                "Hello! I'm your Anticipatory Action Assistant. I can help you with developing interventions, "
                "integrating predictive models, and managing stakeholder engagement. Select a focus area from the "
                "sidebar and let's get started!"
            ),
        }
    ]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# File upload for relevant documents
uploaded_file = st.file_uploader(
    "Upload relevant documents (PDF) for context (max 200MB):",
    type=["pdf"],
    help="Upload SOPs, meeting minutes, or other relevant documents"
)

document_text = ""
if uploaded_file:
    try:
        pdf_reader = PdfReader(uploaded_file)
        document_text = "".join(page.extract_text() for page in pdf_reader.pages)
        st.success("Document uploaded successfully. The assistant will use this for context.")
        
        st.session_state["messages"].append(
            {
                "role": "assistant",
                "content": (
                    f"I've processed your document. Based on the selected focus area '{context_option}', "
                    "I can provide specific guidance. What would you like to know?"
                ),
            }
        )
    except Exception as e:
        st.error(f"Error processing document: {str(e)}")

# System prompt based on selected context
def get_system_prompt(context_option):
    if context_option == "Development of Anticipatory Actions Interventions":
        return """You are an expert in developing anticipatory action interventions. Your role is to:
1. Guide the development of effective anticipatory action interventions
2. Help identify key components and best practices
3. Assist in designing intervention strategies
4. Provide insights on implementation approaches
5. Share knowledge about successful case studies

Focus on practical, actionable advice that can be implemented in real-world scenarios."""
    else:  # Associating Anticipatory Actions with Predictive Models
        return """You are an expert in linking anticipatory actions with predictive models. Your role is to:
1. Help connect predictive models with appropriate anticipatory actions
2. Guide the selection of triggers and thresholds
3. Assist in developing early warning systems
4. Provide insights on model validation and verification
5. Share knowledge about successful implementations

Focus on practical, actionable advice that can be implemented in real-world scenarios."""

# Chat input
if prompt := st.chat_input("Ask a question about anticipatory actions..."):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Prepare context
    system_prompt = get_system_prompt(context_option)
    context = f"{system_prompt}\n\nSelected Focus Area: {context_option}\n\nDocument Content:\n{document_text}\n\nUser Query: {prompt}"

    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "assistant", "content": f"Focus Area: {context_option}\n\nDocument Context:\n{document_text}"},
            ]
            + [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages],
            max_tokens=1000,
        )

        # Process and display response
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    except Exception as e:
        st.error(f"Error communicating with OpenAI: {str(e)}")

# Add copyright notice at the bottom
st.markdown(
    "<div style='text-align: center; margin-top: 50px; font-size: 12px; color: gray;'>"
    "© UNICEF. All rights reserved."
    "</div>",
    unsafe_allow_html=True
) 