"""
基于Streamlit完成WEB网页上传服务
"""
import streamlit as st
from knowledge_base import KnowledgeBaseService


# 添加网页标题
st.title("知识库更新服务")

# 初始化service
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

# 创建标签页
tab1, tab2 = st.tabs(["上传文件", "删除文件"])

with tab1:
    uploader_file = st.file_uploader(
        "请上传TXT文件",
        type=['txt'],
        accept_multiple_files=False,
    )

    if uploader_file is not None:
        file_name = uploader_file.name
        file_type = uploader_file.type
        file_size = uploader_file.size / 1024

        st.subheader(f"文件名:{file_name}")
        st.write(f"格式{file_type} | 大小{file_size:.2f}KB")

        text = uploader_file.getvalue().decode("utf-8")

        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)

with tab2:
    st.subheader("删除已上传的文件")

    # 获取文件列表
    file_list = st.session_state["service"].get_file_list()

    if file_list:
        selected_file = st.selectbox(
            "选择要删除的文件",
            options=file_list,
            help="从列表中选择需要删除的文件"
        )

        st.info(f"准备删除: {selected_file}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("确认删除", type="primary"):
                result = st.session_state["service"].delete_by_filename(selected_file)
                st.success(result)
                import time
                time.sleep(1)
                st.rerun()

        with col2:
            if st.button("刷新列表", type="secondary"):
                st.rerun()
    else:
        st.info("暂无已上传的文件")