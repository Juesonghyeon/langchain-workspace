# 비동기 코드
import asyncio

async def fetch_data_async(delay):
    print(f"비동기 데이터 가져오기 시작 (딜레이: {delay}초)")
    await asyncio.sleep(delay)
    print(f"비동기 데이터 가져오기 완료 (딜레이: {delay}초)")
    return f"비동기 데이터 (딜레이 {delay})"

async def main():
    task1 = asyncio.create_task(fetch_data_async(2))
    task2 = asyncio.create_task(fetch_data_async(1))
    result = await asyncio.gather(task1, task2)
    print(result)

asyncio.run(main())