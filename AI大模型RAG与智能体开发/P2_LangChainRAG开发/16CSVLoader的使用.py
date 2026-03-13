from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path = "./data/stu.csv",
    csv_args={
        "delimiter":"|",    #指定分隔符
        "quotechar":'"',    #指定带有分隔符文本的引号包围是单引号还是双引号
        #如果数据原本有表头，就不要下面指定表头的代码,否则表头也会被当成数据处理
        "fieldnames":['name','age','gender','hobby']
    },
    encoding = "utf-8"
)

#批量加载 .laod

# documents = loader.load()
# for document in documents:
#     print(document)


#流式加载 .lazy_load
for document in loader.lazy_load():
    print(document)