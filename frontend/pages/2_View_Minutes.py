import streamlit as st
from utils.api_client import api_client

st.set_page_config(page_title="View Minutes", page_icon="📋")

st.title("📋 View Meeting Minutes")
st.markdown("Review extracted meeting minutes and transcripts")

st.subheader("Recent Meetings")

# Get meetings from API
meetings_response = api_client.get_meetings()

if "error" not in meetings_response:
    if meetings_response:
        for meeting in meetings_response:
            with st.expander(f"📌 {meeting.get('title', 'Untitled Meeting')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**ID:** {meeting.get('id')}")
                    st.markdown(f"**Created:** {meeting.get('created_at', 'N/A')}")
                    st.markdown(f"**Duration:** {meeting.get('duration_minutes', 0)} minutes")
                
                with col2:
                    if meeting.get('participants'):
                        st.markdown(f"**Participants:** {len(meeting['participants'])}")
                        for participant in meeting['participants'][:3]:
                            st.caption(f"• {participant}")
                
                if meeting.get('minutes'):
                    st.markdown("**Minutes:**")
                    st.write(meeting['minutes'])
                else:
                    st.info("No minutes available yet")
    else:
        st.info("No meetings found")
else:
    st.error(f"Error loading meetings: {meetings_response.get('error')}")

st.markdown("---")

# Search/Filter
search_term = st.text_input("🔍 Search meetings", placeholder="Enter meeting title or description")
