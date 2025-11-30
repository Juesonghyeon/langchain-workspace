def greet(name="아무개"): # 기본 매개변수(default parameter)
    """이 함수는 이름을 입력 받아서 환영하는 메시지를 출력합니다."""
    return f"안녕하세요, {name}님!"

print(greet("김일남"))
print(greet())