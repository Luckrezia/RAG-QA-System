import os
import json
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


def get_history(session_id):
    return FileChatMessagesHistory(session_id, storage_path = "./chat_history")

class FileChatMessagesHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id    #会话id
        self.storage_path = storage_path    #不同会话id的存储地址
        #完整文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)

        #确保文件夹是否存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok = True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)

        #将数据同步到本地文件中
        #类对象写入文件-》一堆二进制
        #为了方便，将BaseMessage转为字典存入json中
        #官方提供message_to_dict，实现单个对象转字典

        new_messages = [message_to_dict(messages) for messages in all_messages]
        #将数据写入文件
        with open(self.file_path, "w", encoding = "utf-8") as f:
            json.dump(new_messages, f)

    @property    #@property装饰器将messages方法变成成员属性使用
    def messages(self) -> list[BaseMessage]:
        # 当前文件内：list[字典]
        try:
            with open(self.file_path, "r", encoding = "utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding = "utf-8") as f:
            json.dump([], f)