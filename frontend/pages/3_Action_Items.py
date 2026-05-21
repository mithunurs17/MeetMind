import streamlit as st
from utils.api_client import api_client

st.set_page_config(page_title="Action Items", page_icon="✅")

st.title("✅ Action Items")
st.markdown("Track and manage action items from your meetings")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Action Items", "0")

with col2:
    st.metric("Pending", "0")

with col3:
    st.metric("Completed", "0")

st.markdown("---")

st.subheader("Action Items by Status")

tabs = st.tabs(["All", "Pending", "In Progress", "Completed"])

with tabs[0]:
    st.info("No action items yet")

with tabs[1]:
    st.info("No pending action items")

with tabs[2]:
    st.info("No items in progress")

with tabs[3]:
    st.success("No completed action items to display")

st.markdown("---")

st.subheader("Add New Action Item")

col1, col2 = st.columns(2)

with col1:
    action_title = st.text_input("Action Item Title")
    assigned_to = st.selectbox("Assigned To", ["John Doe", "Jane Smith", "Mike Johnson"])

with col2:
    due_date = st.date_input("Due Date")
    priority = st.select_slider("Priority", ["Low", "Medium", "High"])

if st.button("➕ Add Action Item", type="primary", use_container_width=True):
    st.success("Action item added successfully!")
