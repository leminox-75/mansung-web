"""
공지사항 API 라우터
공지사항 CRUD 엔드포인트 제공
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database import get_db
from models import Notice
from schemas import NoticeCreate, NoticeResponse

router = APIRouter(prefix="/api/notices", tags=["공지사항"])


@router.get("/", response_model=List[NoticeResponse])
def get_notices(
    skip:     int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit:    int = Query(10, ge=1, le=100, description="페이지당 항목 수"),
    category: Optional[str] = Query(None, description="카테고리 필터"),
    db:       Session = Depends(get_db)
):
    """
    공지사항 목록 조회.
    고정 게시물이 상단에 오도록 정렬하고 최신순으로 반환.
    """
    query = db.query(Notice)
    if category:
        query = query.filter(Notice.category == category)
    notices = query.order_by(desc(Notice.is_pinned), desc(Notice.created_at)) \
                   .offset(skip).limit(limit).all()
    return notices


@router.get("/{notice_id}", response_model=NoticeResponse)
def get_notice(notice_id: int, db: Session = Depends(get_db)):
    """
    특정 공지사항 상세 조회.
    조회 시 view_count를 1 증가시킴.
    """
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")
    notice.view_count += 1
    db.commit()
    db.refresh(notice)
    return notice


@router.post("/", response_model=NoticeResponse, status_code=201)
def create_notice(data: NoticeCreate, db: Session = Depends(get_db)):
    """
    공지사항 등록.
    관리자만 사용하는 엔드포인트 (추후 인증 미들웨어 추가 예정).
    """
    notice = Notice(**data.model_dump())
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return notice
