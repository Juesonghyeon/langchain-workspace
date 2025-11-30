# I/O
# Input과 Output
# File I/O

# 파일 쓰기
file_write = open("sample.txt", "w", encoding="utf-8")
file_write.write("안녕하세요!\n")
file_write.write("두 번째 줄입니다.\n")
file_write.close()