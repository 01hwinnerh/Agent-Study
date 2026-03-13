from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

# vector_store = InMemoryVectorStore(
#     embedding=DashScopeEmbeddings(),
# )

from langchain_chroma import Chroma
vector_store = Chroma(
    collection_name="test",     #数据库名称
    embedding_function=DashScopeEmbeddings(),       #传入嵌入模型
    persist_directory="./chroma_db",        #指定数据存放的文件夹层
)

# loader = CSVLoader(
#     file_path="./data/info.csv",
#     encoding="utf-8",
#     source_column="source",     #指定本条数据的来源是哪里
# )
#
# documents = loader.load()
#
# #id1 id2 id3 id4
# #向量存储的新增，删除，检索
# vector_store.add_documents(
#     documents=documents,
#     ids=["id"+str(i) for i in range(1,len(documents)+1)]       #给添加的文档提供id(字符串)
# )
#
# #删除 传入[id,id,id,.....]
# vector_store.delete(["id1","id2"])


#检索  返回类型lsit[Document]
result = vector_store.similarity_search(
    query="python是不是简单易学呀",
    k=3,
    filter={"source":"黑马程序员"},      #过滤，制指定只要黑马程序员的
)

print(result)
