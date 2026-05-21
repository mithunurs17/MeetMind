import streamlit as st
from utils.api_client import api_client

st.set_page_config(
    page_title="MeetMind AI",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 MeetMind AI")
st.subheader("AI-powered Meeting Minutes & Action Item Extractor")

# Sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### Navigation")
    st.markdown("Use the pages menu to navigate between features:")
    st.markdown("- 📹 **Upload Meeting**: Upload and process meeting recordings")
    st.markdown("- 📋 **View Minutes**: Review extracted meeting minutes")
    st.markdown("- ✅ **Action Items**: Manage action items and follow-ups")
    
    st.markdown("---")
    st.markdown("### API Status")
    health_status = api_client.health_check()
    if health_status.get("status") == "healthy":
        st.success("✅ Backend Connected")
    else:
        st.error("❌ Backend Disconnected")
    
    if health_status.get("database"):
        st.info(f"Database: {health_status.get('database')}")


# Main content
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Meetings",
        "0",
        help="Total number of meetings processed"
    )

with col2:
    st.metric(
        "Action Items",
        "0",
        help="Total pending action items"
    )

with col3:
    st.metric(
        "Participants",
        "0",
        help="Total unique participants"
    )

st.markdown("---")

st.info(
    "👋 Welcome to MeetMind AI! This application helps you extract meeting minutes "
    "and action items from your meetings automatically using AI. "
    "Get started by uploading a meeting recording or selecting a page from the menu."
)
