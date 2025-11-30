# uv add langchain-community pypdf
# https://docs.langchain.com/oss/python/langchain/knowledge-base#loading-documents
from langchain_community.document_loaders import PyPDFLoader

file_path = r"data\KCI_FI003153549.pdf"
loader = PyPDFLoader(file_path)

pages = loader.load()

# print(len(docs))

# print(docs[0])

full_txt = ""

for page in pages:
    full_txt += page.page_content

with open("output/output_pypdf.txt", "w", encoding="utf-8") as f:
    f.write(full_txt)