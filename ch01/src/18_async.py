# --- async/await를 사용한 비동기 코드 ---
import asyncio

async def fetch_data(delay):
    print(f"데이터 가져오기 시작 (딜레이: {delay}초)")
    await asyncio.sleep(delay) # I/O 작업 시뮬레이션
    print(f"데이터 가져오기 완료 (딜레이: {delay}초)")
    return f"데이터 (딜레이 {delay})"

async def main():
    task1 = asyncio.create_task(fetch_data(2))
    task2 = asyncio.create_task(fetch_data(1))

    results = await asyncio.gather(task1, task2)  #  이 await 문 덕분에 main() 함수는 fetch_data 코루틴들이 asyncio.sleep()을 완료하고 "데이터 가져오기 완료" 메시지를 출력할 때까지 기다림, 프로그램이 태스크가 끝나기 전에 종료되는 것을 방지!
    print(f"모든 결과: {results}")

# main() 함수 실행 (Jupyter/IPython 환경에서는 run_until_complete 사용)
asyncio.run(main())