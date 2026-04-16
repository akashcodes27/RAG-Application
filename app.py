import streamlit as st
from dotenv import load_dotenv

from agents.pdf_agent import get_pdf_text, get_text_chunks, get_vectorstore, get_retriever, ask_pdf_question
from agents.sql_agent import ask_sql_question
from agents.router_agent import classify_intent
from htmlTemplate import css, bot_template, user_template

load_dotenv()


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Customer Support AI",
    page_icon="🤖",
    layout="wide",
)
st.write(css, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "retriever" not in st.session_state:
    st.session_state.retriever = None


# ── Header ────────────────────────────────────────────────────────────────────
st.title("🤖 Multi-Agent Customer Support AI")
st.caption(
    "Ask about **company policies** (from uploaded PDFs) "
    "or **customer data & support tickets** (from the database)."
)
st.divider()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📄 Policy Documents")
    st.write("Upload PDF policy documents to enable document Q&A.")

    pdf_docs = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if st.button("⚙️ Process Documents", use_container_width=True):
        if not pdf_docs:
            st.warning("Please upload at least one PDF first.")
        else:
            with st.spinner("Processing documents..."):
                raw_text = get_pdf_text(pdf_docs)
                chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(chunks)
                st.session_state.retriever = get_retriever(vectorstore)
            st.success(f"✅ {len(pdf_docs)} document(s) processed!")

    st.divider()

    # Status indicators
    st.subheader("Agent Status")
    pdf_status = "✅ Ready" if st.session_state.retriever else "⚠️ No docs uploaded"
    st.markdown(f"**📄 PDF Agent:** {pdf_status}")
    st.markdown("**🗃️ SQL Agent:** ✅ Always ready")

    st.divider()
    st.subheader("💡 Try asking:")
    st.markdown("""
**Policy questions:**
- *What is the refund policy?*
- *How many sick days do employees get?*
- *What is the remote work policy?*

**Customer questions:**
- *Give me an overview of Ema's profile*
- *What open tickets does James have?*
- *Show all suspended accounts*
- *List all high priority tickets*
    """)

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


# ── Chat display ──────────────────────────────────────────────────────────────
chat_container = st.container()

with chat_container:
    if not st.session_state.chat_history:
        st.info(
            "👋 Hello! I'm your Multi-Agent Support AI. "
            "Ask me anything about company policies or customer records."
        )
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.write(
                    user_template.replace("{{MSG}}", msg["content"]),
                    unsafe_allow_html=True,
                )
            else:
                badge_class = msg.get("agent", "pdf")
                badge_label = "📄 PDF Agent" if badge_class == "pdf" else "🗃️ SQL Agent"
                rendered = (
                    bot_template
                    .replace("{{MSG}}", msg["content"])
                    .replace("{{BADGE_CLASS}}", badge_class)
                    .replace("{{BADGE_LABEL}}", badge_label)
                )
                st.write(rendered, unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
st.divider()
user_question = st.chat_input("Ask about policies or a customer...")

if user_question:
    # Classify intent
    intent = classify_intent(user_question)

    # Route to correct agent
    if intent == "pdf":
        if st.session_state.retriever is None:
            answer = (
                "⚠️ No PDF documents have been uploaded yet. "
                "Please upload policy documents in the sidebar first."
            )
            intent = "pdf"
        else:
            with st.spinner("📄 Searching policy documents..."):
                answer = ask_pdf_question(user_question, st.session_state.retriever)
    else:
        with st.spinner("🗃️ Querying customer database..."):
            answer = ask_sql_question(user_question)

    # Save to history
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    st.session_state.chat_history.append({"role": "assistant", "content": answer, "agent": intent})

    st.rerun()
