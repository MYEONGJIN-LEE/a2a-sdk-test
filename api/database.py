from datetime import datetime
from typing import Dict, Optional
import hashlib
from api.schemas import UserInDB, UserCreate, UserUpdate


class InMemoryDatabase:
    """인메모리 데이터베이스 (개발/테스트용)"""
    
    def __init__(self):
        self.users: Dict[int, UserInDB] = {}
        self._next_id = 1
        self._email_index: Dict[str, int] = {}  # 이메일로 빠른 검색을 위한 인덱스
        self._username_index: Dict[str, int] = {}  # 사용자명으로 빠른 검색을 위한 인덱스
    
    def _hash_password(self, password: str) -> str:
        """비밀번호 해시화 (간단한 예제용)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, user: UserCreate) -> UserInDB:
        """사용자 생성"""
        # 이메일 중복 확인
        if user.email in self._email_index:
            raise ValueError("이미 존재하는 이메일입니다.")
        
        # 사용자명 중복 확인
        if user.username in self._username_index:
            raise ValueError("이미 존재하는 사용자명입니다.")
        
        user_id = self._next_id
        self._next_id += 1
        
        now = datetime.now()
        user_in_db = UserInDB(
            id=user_id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            password_hash=self._hash_password(user.password),
            created_at=now,
            updated_at=now
        )
        
        self.users[user_id] = user_in_db
        self._email_index[user.email] = user_id
        self._username_index[user.username] = user_id
        
        return user_in_db
    
    def get_user(self, user_id: int) -> Optional[UserInDB]:
        """ID로 사용자 조회"""
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """이메일로 사용자 조회"""
        user_id = self._email_index.get(email)
        if user_id:
            return self.users.get(user_id)
        return None
    
    def get_user_by_username(self, username: str) -> Optional[UserInDB]:
        """사용자명으로 사용자 조회"""
        user_id = self._username_index.get(username)
        if user_id:
            return self.users.get(user_id)
        return None
    
    def get_all_users(self) -> list[UserInDB]:
        """모든 사용자 조회"""
        return list(self.users.values())
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserInDB]:
        """사용자 정보 수정"""
        user = self.users.get(user_id)
        if not user:
            return None
        
        # 이메일 변경 시 중복 확인
        if user_update.email and user_update.email != user.email:
            if user_update.email in self._email_index:
                raise ValueError("이미 존재하는 이메일입니다.")
            # 기존 인덱스 제거
            del self._email_index[user.email]
            # 새 인덱스 추가
            self._email_index[user_update.email] = user_id
            user.email = user_update.email
        
        # 사용자명 변경 시 중복 확인
        if user_update.username and user_update.username != user.username:
            if user_update.username in self._username_index:
                raise ValueError("이미 존재하는 사용자명입니다.")
            # 기존 인덱스 제거
            del self._username_index[user.username]
            # 새 인덱스 추가
            self._username_index[user_update.username] = user_id
            user.username = user_update.username
        
        # 다른 필드 업데이트
        if user_update.full_name is not None:
            user.full_name = user_update.full_name
        
        if user_update.password:
            user.password_hash = self._hash_password(user_update.password)
        
        user.updated_at = datetime.now()
        
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """사용자 삭제"""
        user = self.users.get(user_id)
        if not user:
            return False
        
        # 인덱스에서 제거
        del self._email_index[user.email]
        del self._username_index[user.username]
        del self.users[user_id]
        
        return True


# 전역 데이터베이스 인스턴스
db = InMemoryDatabase()

