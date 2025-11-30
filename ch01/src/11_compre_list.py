# 리스트 내포(List Comprehension)
nums = [1, 2, 3, 4, 5]
result = [num * num for num in nums]
print(result) # [1, 4, 9, 16, 25]
result = [num * num for num in nums if num % 2 == 0]
print(result) # [4, 16]
