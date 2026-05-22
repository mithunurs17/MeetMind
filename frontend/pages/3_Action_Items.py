import streamlit as st
from utils.api_client import api_client

st.set_page_config(page_title="Action Items", page_icon="✅")

st.title("✅ Action Items")
st.markdown("Track and manage action items extracted from meeting minutes.")

meetings_response = api_client.get_meetings()
all_items = []
if "error" not in meetings_response:
    meetings = meetings_response or []
    for meeting in meetings:
        for item in meeting.get("action_items", []):
            item_record = item.copy()
            item_record["meeting_title"] = meeting.get("title")
            item_record["meeting_id"] = meeting.get("id")
            all_items.append(item_record)
else:
    st.error(f"Error loading meetings: {meetings_response.get('error')}")

pending = sum(1 for i in all_items if i.get("status") == "pending")
completed = sum(1 for i in all_items if i.get("status") == "completed")
active = len(all_items) - pending - completed

col1, col2, col3 = st.columns(3)
col1.metric("Total Action Items", len(all_items))
col2.metric("Pending", pending)
col3.metric("Completed", completed)

st.markdown("---")

if all_items:
    status_tabs = st.tabs(["All", "Pending", "Completed"])
    status_map = {
        "All": all_items,
        "Pending": [item for item in all_items if item.get("status") == "pending"],
        "Completed": [item for item in all_items if item.get("status") == "completed"],
    }

    for idx, key in enumerate(status_map):
        with status_tabs[idx]:
            if status_map[key]:
                for item in status_map[key]:
                    st.markdown(
                        f"**{item.get('task')}** — {item.get('meeting_title', 'Meeting')} | "
                        f"Owner: {item.get('owner') or 'Unassigned'} | "
                        f"Due: {item.get('due_date') or 'TBD'} | Status: {item.get('status') or 'pending'}"
                    )
            else:
                st.info("No action items in this category.")

    st.markdown("---")
    st.subheader("Update Action Item Status")
    item_options = {f"{item['id']} — {item['task']}": item for item in all_items}
    selected_key = st.selectbox("Select an action item", list(item_options.keys()))
    if selected_key:
        selected_item = item_options[selected_key]
        new_status = st.selectbox(
            "New Status",
            ["pending", "in progress", "completed"],
            index=["pending", "in progress", "completed"].index(selected_item.get("status", "pending"))
        )
        if st.button("Update Status"):
            result = api_client.update_action_item_status(selected_item["id"], new_status)
            if result.get("error"):
                st.error(f"Error updating action item: {result['error']}")
            else:
                st.success("Action item updated successfully.")
                st.experimental_rerun()
else:
    st.info("No action items have been extracted yet.")
