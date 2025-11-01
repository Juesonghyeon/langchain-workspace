import sys

def make_even_nums_list(n):
    nums = []
    for i in range(n):
        if(i % 2 == 0):
            nums.append(i)
    return nums

def make_even_nums_generator(n):
    for i in range(n):
        if(i % 2 == 0):
            yield i

Number = 10000000

list_of_evens = make_even_nums_list(Number)
print(f"리스트 짝수 개수: {len(list_of_evens)}, {sys.getsizeof()} 바이트")

generator_of_evens = make_even_nums_generator(Number)

count = 0
for num in generator_of_evens:
    count += 1
print(f"제너레이터 짝수 개수: {count}, {sys.getsizeof()}바이트")