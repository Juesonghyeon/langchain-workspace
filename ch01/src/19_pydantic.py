# uv add pydantic
from pydantic import BaseModel, Field

# 유효성 검사 적용
class User(BaseModel):
    name: str = Field(..., description="사용자의 이름")
    age: int = Field(..., gt=0, description="사용자의 나이 (0보다 커야 함)")
    # age: int
    email: str | None = None # 옵션(선택적 필드)

try:
    kim1 = User(name="김일남", age=99)
    print(kim1)
    kim2 = User(name="김이남", age=98, email="kim2@example.com")
    print(kim2)
    kim3 = User(name="김삼남", age=-97, email="kim3@example.com")
    print(kim3)
except Exception as e:
    print(e)