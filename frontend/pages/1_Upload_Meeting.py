import streamlit as st
from utils.api_client import api_client

st.set_page_config(page_title="Upload Meeting", page_icon="📹")

st.title("📹 Upload Meeting")
st.markdown("Upload a transcript or meeting document and extract minutes with AI.")

with st.form(key="meeting_form"):
    meeting_title = st.text_input("Meeting Title", placeholder="Enter meeting title")
    raw_text = st.text_area(
        "Meeting Transcript",
        placeholder="Paste the raw meeting transcript here...",
        height=200,
    )
    uploaded_file = st.file_uploader(
        "Or upload a transcript/document",
        type=["txt", "pdf", "docx", "png", "jpg", "jpeg"],
        help="Supported formats: txt, pdf, docx, png, jpg, jpeg",
    )
    submit = st.form_submit_button(label="📤 Extract Meeting Minutes")

if submit:
    if not meeting_title:
        st.error("Please enter a meeting title.")
    elif not raw_text and not uploaded_file:
        st.error("Please paste transcript text or upload a supported file.")
    else:
        with st.spinner("Processing meeting with AI..."):
            if raw_text:
                result = api_client.extract_meeting_from_text(meeting_title, raw_text)
            else:
                result = api_client.extract_meeting_from_file(meeting_title, uploaded_file)

        if result.get("error") or result.get("detail"):
            st.error(f"Error: {result.get('error') or result.get('detail')}" )
        else:
            st.success("✅ Meeting minutes extracted and saved successfully!")
            st.subheader("Summary")
            st.write(result.get("summary", "No summary returned."))

            st.subheader("Decisions")
            if result.get("decisions"):
                for decision in result["decisions"]:
                    st.write(f"• {decision}")
            else:
                st.info("No decisions extracted.")

            st.subheader("Action Items")
            if result.get("action_items"):
                for item in result["action_items"]:
                    st.markdown(
                        f"- **{item.get('task')}** | Owner: {item.get('owner') or 'Unassigned'} | "
                        f"Due: {item.get('due_date') or 'TBD'} | Status: {item.get('status') or 'pending'}"
                    )
            else:
                st.info("No action items extracted.")

            st.subheader("Risks")
            if result.get("risks"):
                for risk in result["risks"]:
                    st.write(f"• {risk}")
            else:
                st.info("No risks detected.")

            st.subheader("Open Questions")
            if result.get("open_questions"):
                for question in result["open_questions"]:
                    st.write(f"• {question}")
            else:
                st.info("No open questions found.")

st.markdown("---")
st.markdown("**Tips:**")
st.markdown("- Paste raw transcript text for the best AI output.")
st.markdown("- Upload meeting notes or scanned documents for extraction.")
st.markdown("- Use clear speaker text for better decision and action item capture.")
