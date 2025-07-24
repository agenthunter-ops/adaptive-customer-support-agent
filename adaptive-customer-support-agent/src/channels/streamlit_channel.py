"""
Minimal Streamlit front-end for demos.
Run via:  `streamlit run src/channels/streamlit_channel.py`
"""
import streamlit as st
import uuid
from src.routing.workflow_router import get_conversation_agent

st.set_page_config(page_title="Banking Support AI", page_icon="💬")
st.title("💬 Adaptive Customer Support Agent")

if "session_id" not in st.session_state:
    st.session_state["session_id"] = uuid.uuid4().hex
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

agent = get_conversation_agent()

with st.chat_message("assistant"):
    st.markdown(
        "Hey there! I'm your virtual banking assistant. "
        "Ask me anything about your account, cards, or loans. "
        "_Note: demo only – **don't** share private information._"
    )

user_msg = st.chat_input("Type your question...")
if user_msg:
    st.session_state.chat_history.append(("user", user_msg))
    with st.chat_message("user"):
        st.markdown(user_msg)

    with st.spinner("Thinking..."):
        reply = agent(
            session_id=st.session_state.session_id,
            user_text=user_msg,
        )
        reply = reply if isinstance(reply, str) else reply  # sync / async adapt
    st.session_state.chat_history.append(("assistant", reply))
    with st.chat_message("assistant"):
        st.markdown(reply)
