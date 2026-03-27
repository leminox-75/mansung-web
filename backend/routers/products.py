"""
제품 API 라우터
제품 목록 및 상세 정보 조회 엔드포인트
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database import get_db
from models import Product
from schemas import ProductCreate, ProductResponse

router = APIRouter(prefix="/api/products", tags=["제품"])


@router.get("/", response_model=List[ProductResponse])
def get_products(
    category:     Optional[str] = Query(None, description="카테고리 필터 (비닐하우스자재/프레스제품/기타)"),
    sub_category: Optional[str] = Query(None, description="세부 카테고리 필터"),
    db:           Session = Depends(get_db)
):
    """
    제품 목록 조회.
    카테고리/세부 카테고리로 필터링 가능하며 sort_order 기준으로 정렬.
    """
    query = db.query(Product).filter(Product.is_active == True)
    if category:
        query = query.filter(Product.category == category)
    if sub_category:
        query = query.filter(Product.sub_category == sub_category)
    return query.order_by(Product.sort_order, Product.id).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    특정 제품 상세 조회.
    비활성화된 제품은 404 반환.
    """
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="제품을 찾을 수 없습니다.")
    return product


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    """
    제품 등록.
    관리자 전용 엔드포인트.
    """
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
