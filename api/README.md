# User Management API

FastAPI를 사용한 사용자 회원가입, 수정, 삭제, 읽기 API입니다.

## 설치

의존성 설치:
```bash
uv sync
```

## 실행

서버 실행:
```bash
python api/run.py
```

또는 uvicorn 직접 실행:
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

서버가 실행되면 다음 주소에서 접근할 수 있습니다:
- API: http://localhost:8000
- API 문서 (Swagger UI): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc

## API 엔드포인트

### 1. 사용자 회원가입 (Create)
```http
POST /api/users/
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "testuser",
  "full_name": "Test User",
  "password": "password123"
}
```

### 2. 모든 사용자 조회 (Read All)
```http
GET /api/users/
```

### 3. 특정 사용자 조회 (Read One)
```http
GET /api/users/{user_id}
```

### 4. 사용자 정보 수정 (Update)
```http
PUT /api/users/{user_id}
Content-Type: application/json

{
  "email": "newemail@example.com",
  "username": "newusername",
  "full_name": "New Name",
  "password": "newpassword123"
}
```

부분 업데이트도 가능합니다 (수정할 필드만 전달):
```http
PUT /api/users/{user_id}
Content-Type: application/json

{
  "full_name": "Updated Name"
}
```

### 5. 사용자 삭제 (Delete)
```http
DELETE /api/users/{user_id}
```

## 예제 요청

### cURL 예제

#### 회원가입
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "password123"
  }'
```

#### 사용자 조회
```bash
curl -X GET "http://localhost:8000/api/users/1"
```

#### 사용자 수정
```bash
curl -X PUT "http://localhost:8000/api/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Updated Name"
  }'
```

#### 사용자 삭제
```bash
curl -X DELETE "http://localhost:8000/api/users/1"
```

## 데이터베이스

현재는 인메모리 데이터베이스를 사용합니다. 서버를 재시작하면 모든 데이터가 초기화됩니다.

실제 프로덕션 환경에서는 `api/database.py`를 수정하여 PostgreSQL, MySQL 등의 실제 데이터베이스를 사용하도록 변경할 수 있습니다.

## 프로젝트 구조

```
api/
├── __init__.py
├── main.py              # FastAPI 앱 메인 파일
├── schemas.py           # Pydantic 스키마 정의
├── database.py          # 데이터베이스 로직
├── run.py               # 서버 실행 스크립트
├── routers/
│   ├── __init__.py
│   └── users.py         # 사용자 관련 라우터
└── README.md
```

