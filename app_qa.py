import time
import streamlit as st
from rag import RagService
import config_data as config

#title
st.title("智能客服")
st.divider()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好,有什么能帮你"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入框
prompt = st.chat_input()
if prompt:

    # 在页面输出用户提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    with st.spinner("AI思考中..."):
        history_text = ""
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)
        res = st.chat_message("assistant").write_stream(res_stream)
        st.session_state["message"].append({"role": "assistant", "content": res})