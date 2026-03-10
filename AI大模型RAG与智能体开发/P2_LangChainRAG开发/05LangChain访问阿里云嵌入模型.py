#langchain_community
from langchain_community.embeddings import DashScopeEmbeddings

#创建模型对象，不传model则默认使用的是 text-embeddings-v1
model = DashScopeEmbeddings()

#不用invoke，stream
#embed_query（单个转化）,embed_documents（批量转换）
print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你","我稀饭你","晚上吃啥"]))
