import streamlit as st
from graph import app, app_without_reflection
from langchain_core.messages import HumanMessage



st.set_page_config(page_title="AI Research Agent", layout="centered")

st.title("🧠 AI Research Agent")
st.markdown("Ask about latest current affairs and compare baseline vs reflection.")

query = st.text_input("Enter your query:")

mode = st.radio(
    "Select Mode:",
    ["Baseline", "With Reflection"]
)

if st.button("Run Agent"):

    if not query.strip():
        st.warning("Please enter a query.")
        st.stop()

    state = {
        "messages": [HumanMessage(content=query)],
        "human_feedback": None,
        "plan": [],
        "research": {},
        "revision_score": 0
    }

    with st.spinner("Running agent..."):

        if mode == "Baseline":
            result = app_without_reflection.invoke(state)
            st.subheader("📄 Final Report")
            report = result["final_report"]
            st.markdown(f"{report['title']}")
            st.write(report["summary"])
            st.markdown(f"[Source]({report['source']})")

        else:
            result = app.invoke(state)

            st.subheader("📄 Final Report")
            report = result["final_report"]
            st.markdown(f"{report['title']}")
            st.write(report["summary"])
            st.markdown(f"[Source]({report['source']})")
            st.subheader("🔎 Accuracy Score")
            st.write(result["accuracy_report"]["score"])

            st.subheader("💬 Feedback")
            st.write(result["accuracy_report"]["feedback"])

            st.subheader("🔁 Total Revisions")
            st.write(result["revision_score"])
