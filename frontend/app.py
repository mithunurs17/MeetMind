import streamlit as st
from utils.api_client import api_client

st.set_page_config(
    page_title="MeetMind AI",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 MeetMind AI")
st.subheader("AI-powered Meeting Minutes & Action Item Extractor")

health_status = api_client.health_check()
meetings_response = api_client.get_meetings()
meetings = []
action_items = []

if isinstance(meetings_response, list):
    meetings = meetings_response
    for meeting in meetings:
        for item in meeting.get("action_items", []):
            action_items.append(item)

participant_names = {
    item.get("owner") for item in action_items if item.get("owner")
}

# Sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### Navigation")
    st.markdown("Use the pages menu to navigate between features:")
    st.markdown("- 📹 **Upload Meeting**: Upload and process meeting transcripts")
    st.markdown("- 📋 **View Minutes**: Review extracted meeting minutes")
    st.markdown("- ✅ **Action Items**: Manage action items and follow-ups")
    st.markdown("---")
    st.markdown("### API Status")
    if health_status.get("status") == "healthy":
        st.success("✅ Backend Connected")
    else:
        st.error("❌ Backend Disconnected")

    if health_status.get("database"):
        st.info(f"Database: {health_status.get('database')}")

# Main content
col1, col2, col3 = st.columns(3)
col1.metric("Total Meetings", len(meetings))
col2.metric("Action Items", len(action_items))
col3.metric("Participants", len([name for name in participant_names if name]))

st.markdown("---")

st.info(
    "👋 Welcome to MeetMind AI! Extract minutes, decisions, and action items from meeting transcripts "
    "using AI-enhanced NLP. Start by uploading a transcript or using the navigation menu."
)
