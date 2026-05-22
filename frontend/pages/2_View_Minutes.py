import streamlit as st
from utils.api_client import api_client

st.set_page_config(page_title="View Minutes", page_icon="📋")

st.title("📋 View Meeting Minutes")
st.markdown("Review AI-extracted meeting minutes and actionable items.")

st.subheader("Recent Meetings")
meetings_response = api_client.get_meetings()

if "error" in meetings_response:
    st.error(f"Error loading meetings: {meetings_response.get('error')}")
else:
    meetings = meetings_response or []
    if len(meetings) == 0:
        st.info("No meetings found yet. Upload a meeting to begin.")
    else:
        for meeting in meetings:
            with st.expander(f"📌 {meeting.get('title', 'Untitled Meeting')} (ID: {meeting.get('id')})"):
                st.markdown(f"**Created:** {meeting.get('created_at', 'N/A')}")
                st.markdown(f"**Summary:** {meeting.get('summary', '') or 'No summary available.'}")

                if meeting.get("action_items"):
                    st.markdown("**Action Items:**")
                    for item in meeting["action_items"]:
                        st.markdown(
                            f"- **{item.get('task')}** | Owner: {item.get('owner') or 'Unassigned'} | "
                            f"Due: {item.get('due_date') or 'TBD'} | Status: {item.get('status') or 'pending'}"
                        )
                else:
                    st.info("No action items extracted for this meeting.")

                if meeting.get("decisions"):
                    st.markdown("**Decisions:**")
                    for decision in meeting["decisions"]:
                        st.write(f"• {decision}")

                if meeting.get("risks"):
                    st.markdown("**Risks / Dependencies:**")
                    for risk in meeting["risks"]:
                        st.write(f"• {risk.get('risk_text', risk)}")

                open_questions = meeting.get("open_questions") or []
                if not open_questions:
                    open_questions = [
                        r["risk_text"].replace("OPEN QUESTION:", "").strip()
                        for r in meeting.get("risks", [])
                        if isinstance(r, dict) and r.get("risk_text", "").startswith("OPEN QUESTION:")
                    ]
                if open_questions:
                    st.markdown("**Open Questions:**")
                    for question in open_questions:
                        st.write(f"• {question}")

st.markdown("---")
search_term = st.text_input("🔍 Search meetings", placeholder="Enter meeting title or caption")
