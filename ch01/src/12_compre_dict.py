keys = ["name", "age", "city"]
values = ["김일남", 99, "부산"]

result = zip(keys, values)
# print(list(result)) # [('name', '김일남'), ('age', 99), ('city', '부산')]

# key, value = ('name', '김일남') # unpacking, destructuring(구조분해할당)
# print(key)
# print(value)

# 딕셔너리 내포(Dictionary Comprehension)
# result_dict = {k: v for k, v in zip(keys, values)}
# print(result_dict)
result_dict = {k: v for k, v in result} # {'name': '김일남', 'age': 99, 'city': '부산'}
print(result_dict)