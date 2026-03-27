"""
데이터베이스 ORM 모델 정의
만성코프레이션 홈페이지 관련 테이블 구조
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Notice(Base):
    """
    공지사항 테이블.
    관리자가 등록한 공지/뉴스 게시글을 저장.
    """
    __tablename__ = "notices"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False, comment="공지 제목")
    content     = Column(Text, nullable=False, comment="공지 내용 (HTML 허용)")
    category    = Column(String(50), default="공지", comment="카테고리: 공지/뉴스/이벤트")
    is_pinned   = Column(Boolean, default=False, comment="상단 고정 여부")
    view_count  = Column(Integer, default=0, comment="조회수")
    created_at  = Column(DateTime, default=datetime.utcnow, comment="등록일시")
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")


class Product(Base):
    """
    제품 정보 테이블.
    만성코프레이션의 비닐하우스 자재 및 프레스 제품 정보.
    """
    __tablename__ = "products"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(200), nullable=False, comment="제품명")
    category     = Column(String(100), nullable=False, comment="카테고리: 비닐하우스자재/프레스제품/기타")
    sub_category = Column(String(100), comment="세부 카테고리")
    description  = Column(Text, comment="제품 설명")
    spec         = Column(Text, comment="규격/사양 (JSON 형태 텍스트)")
    image_url    = Column(String(500), comment="대표 이미지 경로")
    is_active    = Column(Boolean, default=True, comment="노출 여부")
    sort_order   = Column(Integer, default=0, comment="정렬 순서")
    created_at   = Column(DateTime, default=datetime.utcnow, comment="등록일시")


class Contact(Base):
    """
    문의하기(Q&A) 테이블.
    고객이 제출한 문의 내용 저장.
    """
    __tablename__ = "contacts"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False, comment="문의자 이름")
    company     = Column(String(200), comment="회사명/기관명")
    phone       = Column(String(30), nullable=False, comment="연락처")
    email       = Column(String(200), nullable=False, comment="이메일")
    product     = Column(String(200), comment="문의 제품/서비스")
    message     = Column(Text, nullable=False, comment="문의 내용")
    status      = Column(String(20), default="접수", comment="처리상태: 접수/처리중/완료")
    reply       = Column(Text, comment="답변 내용")
    created_at  = Column(DateTime, default=datetime.utcnow, comment="접수일시")
    replied_at  = Column(DateTime, comment="답변일시")
