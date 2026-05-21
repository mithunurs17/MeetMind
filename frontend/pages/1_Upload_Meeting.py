import streamlit as st
from utils.api_client import api_client

st.set_page_config(page_title="Upload Meeting", page_icon="📹")

st.title("📹 Upload Meeting")
st.markdown("Upload and process your meeting recording")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Meeting Details")
    
    meeting_title = st.text_input(
        "Meeting Title",
        placeholder="Enter meeting title"
    )
    
    meeting_description = st.text_area(
        "Meeting Description",
        placeholder="Enter meeting description (optional)",
        height=100
    )
    
    participants = st.multiselect(
        "Participants",
        ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Williams"],
        help="Select or type participant names"
    )
    
    uploaded_file = st.file_uploader(
        "Upload Meeting Recording",
        type=["mp3", "mp4", "wav", "webm"],
        help="Supported formats: MP3, MP4, WAV, WebM"
    )

with col2:
    st.subheader("Preview")
    if uploaded_file:
        st.write(f"**File:** {uploaded_file.name}")
        st.write(f"**Size:** {uploaded_file.size / 1024 / 1024:.2f} MB")
    else:
        st.info("📁 No file selected")

st.markdown("---")

if st.button("📤 Process Meeting", type="primary", use_container_width=True):
    if not meeting_title:
        st.error("Please enter a meeting title")
    elif not uploaded_file:
        st.error("Please upload a meeting recording")
    else:
        with st.spinner("Processing meeting... This may take a few minutes"):
            result = api_client.create_meeting(
                title=meeting_title,
                description=meeting_description,
                participants=participants
            )
            
            if "error" not in result:
                st.success("✅ Meeting processed successfully!")
                st.json(result)
            else:
                st.error(f"Error processing meeting: {result.get('error')}")

st.markdown("---")
st.markdown("**Tips:**")
st.markdown("- Ensure clear audio for better transcription accuracy")
st.markdown("- Include all participants in the meeting details")
st.markdown("- Supported formats: MP3, MP4, WAV, WebM")
