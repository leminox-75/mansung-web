"""
문의하기 API 라우터
고객 문의 접수 및 조회 엔드포인트
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database import get_db
from models import Contact
from schemas import ContactCreate, ContactResponse

router = APIRouter(prefix="/api/contact", tags=["문의하기"])


@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(data: ContactCreate, db: Session = Depends(get_db)):
    """
    고객 문의 접수.
    제출된 문의를 DB에 저장하고 접수 완료 응답 반환.
    """
    contact = Contact(**data.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.get("/", response_model=List[ContactResponse])
def get_contacts(
    skip:  int = 0,
    limit: int = 20,
    db:    Session = Depends(get_db)
):
    """
    문의 목록 조회 (관리자 전용).
    최신 접수 순으로 반환.
    """
    contacts = db.query(Contact) \
                 .order_by(desc(Contact.created_at)) \
                 .offset(skip).limit(limit).all()
    return contacts
