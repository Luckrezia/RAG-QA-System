from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from vector_stores import VectorStoreService
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.documents import Document
from file_history_store import get_history

class RagService(object):
    def __init__(self):
        self.vector_store = VectorStoreService(
            embedding = DashScopeEmbeddings(model = config.embedding_model_name),
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的参考资料为主,"),
                ("system", "简介回答用户问题,参考资料{context}."),
                ("system", "用户对话历史记录如下如下:"),
                MessagesPlaceholder("history"),
                ("user","请回答用户提问{input}")
            ]
        )
        self.chat_model = ChatTongyi(model = config.chat_model_name)
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_store.get_retriever()

        def format_document(docs: list[Document]):
            if not docs:
                return "无相关参考资料"

            formatted_str = ""
            for doc in docs:
                formatted_str += f"文段片段:{doc.page_content}\n文件元数据:{doc.metadata}\n\n"
            return formatted_str

        def format_for_retriever(value: dict) -> str:
            return value["input"]

        def format_for_template(value):
            # 提取并重组输入数据
            return {
                "input": value["input"]["input"],
                "context": value["context"],
                "history": value["input"]["history"]
            }

        chain = (
            {
                "input": RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriever) | retriever | format_document
            }
            | RunnableLambda(format_for_template)
            | self.prompt_template
            | self.chat_model
            | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain

if __name__ == '__main__':
    session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }
    res = RagService().chain.invoke({"input": "用户提问"})
    print(res)