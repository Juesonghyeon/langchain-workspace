# 리스트 내포(List Comprehension) (향상된 for문ver.python)
nums = [1,2,3,4,5]
result = [num * num for num in nums]
print(result)
result = [num * num for num in nums if num % 2 == 0]
print(result)
