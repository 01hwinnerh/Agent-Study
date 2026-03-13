from langchain_community.document_loaders import JSONLoader

# loader = JSONLoader(
#     file_path="./data/stu.json",
#     jq_schema=".",      #抽取的语法，或者说对象，在这里就决定了抽取的是什么
#     text_content=False   #如果抽取的是非字符串，告知JsonLoader抽取的不是text，默认是True
# )
#
# document = loader.load()
# print(document)

# loader = JSONLoader(
#     file_path="./data/stus.json",
#     jq_schema=".[].name",      #抽取的语法，或者说对象，在这里就决定了抽取的是什么
#     text_content=False   #告知JsonLoader抽取的不是text，默认是True
# )
#
# document = loader.load()
# print(document)


loader = JSONLoader(
    file_path="./data/stu_json_lines.json",
    jq_schema=".name",      #如果是jsonlines的话，不需要.[]了
    text_content=False,   #告知JsonLoader抽取的不是text，默认是True
    json_lines=True         #告知JsonLoader这是一个JsonLines文件，每一行都是一个独立的标准JSON
)

document = loader.load()
print(document)