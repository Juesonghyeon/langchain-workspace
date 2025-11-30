# 데코레이터(Decorator)
def my_decorator(func):
    def wrapper():
        print("함수 실행 전입니다.")
        result = func()
        print("함수 실행 후입니다.")
        return result
    return wrapper

@my_decorator
def say_hello():
    return "안녕하세요!"

print(say_hello())
