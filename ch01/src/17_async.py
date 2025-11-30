# 비동기 프로그래밍 (async / await)

# 동기 코드
import time

def fetch_data_sync(delay):
    print(f"동기 데이터 가져오기 시작 (딜레이: {delay}초)")
    time.sleep(delay)
    print(f"동기 데이터 가져오기 완료 (딜레이: {delay}초)")
    return f"동기 데이터 (딜레이 {delay})"

def main_sync():
    result1 = fetch_data_sync(2)
    result2 = fetch_data_sync(1)
    print(f"모든 동기 결과: [{result1}, {result2}]")

main_sync()