"""
Pydantic 스키마 정의
API 요청/응답 데이터 유효성 검사 및 직렬화
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# ─── 공지사항 스키마 ───────────────────────────────────────────────
class NoticeBase(BaseModel):
    title:    str
    content:  str
    category: str = "공지"
    is_pinned: bool = False


class NoticeCreate(NoticeBase):
    """공지사항 생성 요청 스키마"""
    pass


class NoticeResponse(NoticeBase):
    """공지사항 응답 스키마"""
    id:         int
    view_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ─── 제품 스키마 ──────────────────────────────────────────────────
class ProductBase(BaseModel):
    name:         str
    category:     str
    sub_category: Optional[str] = None
    description:  Optional[str] = None
    spec:         Optional[str] = None
    image_url:    Optional[str] = None
    is_active:    bool = True
    sort_order:   int  = 0


class ProductCreate(ProductBase):
    """제품 생성 요청 스키마"""
    pass


class ProductResponse(ProductBase):
    """제품 응답 스키마"""
    id:         int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── 문의하기 스키마 ──────────────────────────────────────────────
class ContactCreate(BaseModel):
    """문의 등록 요청 스키마"""
    name:    str
    company: Optional[str] = None
    phone:   str
    email:   str
    product: Optional[str] = None
    message: str


class ContactResponse(BaseModel):
    """문의 응답 스키마"""
    id:         int
    name:       str
    status:     str
    created_at: datetime

    class Config:
        from_attributes = True
