"""
知识库
"""
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def check_md5(md5_str: str):
    # 检查传入md5字符串是否被处理过了

    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False


def save_md5(md5_str: str):
    # 将传入的md5字符串，记录到文件中保存
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str, encoding='utf-8'):
    # 将传入的字符串转化为md5字符串
    str_bytes = input_str.encode(encoding=encoding)
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    md5_hex = md5_obj.hexdigest()
    return md5_hex


class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory,
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,
        )

    def upload_by_str(self, data: str, filename):
        # 将传入的字符串，进行向量化，存入向量数据库中
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"

        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.splitter.split_text(data)
        else:
            knowledge_chunks: list[str] = [data]

        metadata = {
            "source": filename,
            "md5": md5_hex,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "gua",
        }
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )

        save_md5(md5_hex)

        return "[成功]内容已经成功载入向量库"

    def get_file_list(self):
        # 获取所有已上传文件的列表
        try:
            all_docs = self.chroma.get()
            file_set = set()

            for metadata in all_docs['metadatas']:
                if metadata and 'source' in metadata:
                    file_set.add(metadata['source'])

            return sorted(list(file_set))
        except Exception as e:
            print(f"获取文件列表失败: {e}")
            return []

    def delete_by_filename(self, filename: str):
        # 根据文件名删除向量库中的文档，并删除对应的MD5记录
        try:
            all_docs = self.chroma.get()

            # 找出需要删除的文档ID和对应的MD5值
            ids_to_delete = []
            md5s_to_delete = set()

            for idx, metadata in enumerate(all_docs['metadatas']):
                if metadata and metadata.get('source') == filename:
                    ids_to_delete.append(all_docs['ids'][idx])
                    if 'md5' in metadata:
                        md5s_to_delete.add(metadata['md5'])

            if not ids_to_delete:
                return f"[提示] 未找到文件 '{filename}' 的相关记录"

            # 删除向量库中的文档
            self.chroma.delete(ids=ids_to_delete)

            # 删除MD5记录
            if md5s_to_delete:
                self._remove_md5_records(md5s_to_delete)
                return f"[成功] 已删除文件 '{filename}'（{len(ids_to_delete)}个文档块，{len(md5s_to_delete)}个MD5记录）"
            else:
                return f"[成功] 已删除文件 '{filename}'（{len(ids_to_delete)}个文档块），但未找到MD5记录"

        except Exception as e:
            return f"[错误] 删除失败: {str(e)}"

    def _remove_md5_records(self, md5s_to_delete: set):
        # 从md5文件中删除指定的MD5记录
        if not md5s_to_delete:
            return

        try:
            # 读取现有的所有MD5记录
            existing_md5s = []
            if os.path.exists(config.md5_path):
                with open(config.md5_path, 'r', encoding='utf-8') as f:
                    existing_md5s = [line.strip() for line in f.readlines()]

            # 过滤掉需要删除的MD5
            remaining_md5s = [md5 for md5 in existing_md5s if md5 not in md5s_to_delete]

            # 重新写入文件
            with open(config.md5_path, 'w', encoding='utf-8') as f:
                for md5 in remaining_md5s:
                    f.write(md5 + '\n')

        except Exception as e:
            print(f"删除MD5记录失败: {e}")


if __name__ == '__main__':
    service = KnowledgeBaseService()
    print(service.get_file_list())