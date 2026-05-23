import json
import streamlit as st
from utils.api_client import api_client
from utils.ui import apply_theme

st.set_page_config(page_title="Upload Meeting", page_icon="📹", layout="wide")
apply_theme()

st.markdown("# 📹 Upload Meeting")
st.markdown(
    "Use AI to extract meeting minutes, decisions, action items, risks, and open questions from transcript text or uploaded files."
)

with st.form(key="meeting_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        meeting_title = st.text_input("Meeting Title", placeholder="Enter meeting title")
        raw_text = st.text_area(
            "Paste meeting notes or transcript",
            placeholder="Paste the raw meeting transcript here...",
            height=260,
        )
    with col2:
        st.markdown("### Upload an optional file")
        uploaded_file = st.file_uploader(
            "Upload transcript or document",
            type=["txt", "pdf", "docx", "png", "jpg", "jpeg"],
            help="Supported formats: txt, pdf, docx, png, jpg, jpeg",
        )
        st.markdown(
            "Use textual uploads for full content extraction, or images/PDFs to let the AI extract text automatically."
        )

    submit = st.form_submit_button(label="Generate Meeting Minutes")

if submit:
    if not meeting_title:
        st.error("Please enter a meeting title.")
    elif not raw_text and not uploaded_file:
        st.error("Please paste transcript text or upload a supported file.")
    else:
        with st.spinner("Generating structured meeting minutes..."):
            if raw_text:
                result = api_client.extract_meeting_from_text(meeting_title, raw_text)
            else:
                result = api_client.extract_meeting_from_file(meeting_title, uploaded_file)

        if result.get("error") or result.get("detail"):
            st.error(f"Unable to extract meeting minutes: {result.get('error') or result.get('detail')}")
        else:
            st.success("✅ Meeting minutes extracted successfully!")
            summary = result.get("summary", "")
            decisions = result.get("decisions") or []
            action_items = result.get("action_items") or []
            risks = result.get("risks") or []
            questions = result.get("open_questions") or []

            st.markdown("---")
            st.markdown("## Executive Summary")
            editable_summary = st.text_area("Editable executive summary", summary, height=170)

            st.markdown("## Decisions")
            decision_text = "\n".join([item.get("decision_text", str(item)) for item in decisions])
            editable_decisions = st.text_area("Editable decisions", decision_text, height=140)

            st.markdown("## Results Overview")
            col1, col2, col3 = st.columns(3)
            col1.markdown(f"**Action items**\n\n{len(action_items)}")
            col2.markdown(f"**Risks / dependencies**\n\n{len(risks)}")
            col3.markdown(f"**Open questions**\n\n{len(questions)}")

            st.markdown("### Action Items")
            if action_items:
                for item in action_items:
                    st.markdown(
                        f"- **{item.get('task')}**  \n"
                        f"  Owner: **{item.get('owner') or 'Unassigned'}** | Due: **{item.get('due_date') or 'TBD'}** | Status: **{item.get('status') or 'pending'}**"
                    )
            else:
                st.info("No action items were found in this meeting.")

            st.markdown("### Risks & Dependencies")
            if risks:
                for risk in risks:
                    text = risk.get("risk_text") if isinstance(risk, dict) else str(risk)
                    st.write(f"• {text}")
            else:
                st.info("No risks or dependencies were detected.")

            st.markdown("### Open Questions")
            if questions:
                for question in questions:
                    st.write(f"• {question}")
            else:
                st.info("No open questions were extracted.")

            export_payload = {
                "title": meeting_title,
                "summary": editable_summary,
                "decisions": editable_decisions.splitlines(),
                "action_items": action_items,
                "risks": risks,
                "open_questions": questions,
            }

            st.download_button(
                "Download meeting minutes JSON",
                json.dumps(export_payload, default=str, indent=2),
                file_name="meetmind_meeting_minutes.json",
                mime="application/json",
            )
            st.download_button(
                "Download summary text",
                editable_summary,
                file_name="meetmind_minutes_summary.txt",
                mime="text/plain",
            )

st.markdown("---")
st.markdown("### Tips for better AI extraction")
st.markdown("- Use structured speaker notes where possible.")
st.markdown("- Add meeting title and agenda items for more precise outcomes.")
st.markdown("- Review and edit the generated summary before sharing.")
