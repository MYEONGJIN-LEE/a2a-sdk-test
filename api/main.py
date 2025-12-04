from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import users

app = FastAPI(
    title="User Management API",
    description="사용자 회원가입, 수정, 삭제, 읽기 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(users.router, prefix="/api/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "User Management API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

