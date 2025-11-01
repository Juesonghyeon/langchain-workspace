# 파일 읽기
file_read = open("sample.txt", "r", encoding="utf-8")
content = file_read.read()
print(content)
file_read.close()