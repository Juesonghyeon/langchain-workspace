import sys

def make_even_nums_list(n):
    nums = []
    for i in range(n):
        if i % 2 == 0:
            nums.append(i)
    return nums

def make_even_nums_generator(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

NUMBER = 10_000_000

list_of_evens = make_even_nums_list(NUMBER)
print(f"리스트 짝수 개수: {len(list_of_evens)}, {sys.getsizeof(list_of_evens)}바이트")

generator_of_evens = make_even_nums_generator(NUMBER)

count = 0
for num in generator_of_evens:
    count += 1
print(f"제너레이터 짝수 개수: {count}, {sys.getsizeof(generator_of_evens)}바이트")