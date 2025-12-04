from fastapi import APIRouter, HTTPException, status
from typing import List
from api import schemas, database

router = APIRouter()


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate):
    """
    사용자 회원가입
    
    - **email**: 사용자 이메일 (필수, 중복 불가)
    - **username**: 사용자명 (필수, 3-50자, 중복 불가)
    - **full_name**: 전체 이름 (선택)
    - **password**: 비밀번호 (필수, 최소 8자)
    """
    try:
        user_in_db = database.db.create_user(user)
        return schemas.UserResponse(
            id=user_in_db.id,
            email=user_in_db.email,
            username=user_in_db.username,
            full_name=user_in_db.full_name,
            created_at=user_in_db.created_at,
            updated_at=user_in_db.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[schemas.UserResponse])
async def get_all_users():
    """
    모든 사용자 조회
    """
    users = database.db.get_all_users()
    return [
        schemas.UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int):
    """
    특정 사용자 조회
    
    - **user_id**: 사용자 ID
    """
    user = database.db.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    
    return schemas.UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(user_id: int, user_update: schemas.UserUpdate):
    """
    사용자 정보 수정
    
    - **user_id**: 사용자 ID
    - 수정할 필드만 전달하면 됩니다 (부분 업데이트 지원)
    """
    try:
        user = database.db.update_user(user_id, user_update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        
        return schemas.UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """
    사용자 삭제
    
    - **user_id**: 사용자 ID
    """
    success = database.db.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    
    return None

