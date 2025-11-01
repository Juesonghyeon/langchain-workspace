#제너레이터
def test_generator():
    yield 2
    yield 3
    yield 4
    yield 5

gen = test_generator()
print(gen)

print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
# print(next(gen))//
