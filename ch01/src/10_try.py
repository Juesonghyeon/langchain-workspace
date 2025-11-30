try:
    result = 10 / 0
    print("결과는:", result)
# except ZeroDivisionError as e:
except Exception as e:
    print("에러가 발생했습니다:", e)