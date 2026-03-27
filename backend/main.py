"""
만성코프레이션 홈페이지 백엔드 메인 애플리케이션
FastAPI 기반 REST API 서버 + 정적 파일 서빙
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from database import Base, engine
from routers import notices, products, contact

# .env 로드
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# 데이터베이스 테이블 자동 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="만성코프레이션 API",
    description="만성코프레이션 홈페이지 리뉴얼 백엔드 API",
    version="1.0.0"
)

# CORS 설정 — 프론트엔드 도메인 허용
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(notices.router)
app.include_router(products.router)
app.include_router(contact.router)

# 프론트엔드 정적 파일 서빙
frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app.mount("/static", StaticFiles(directory=os.path.join(frontend_dir, 'assets')), name="static")

# 모든 HTML 페이지 라우팅 (프론트엔드 SPA 방식)
@app.get("/")
def serve_index():
    """메인 페이지 제공"""
    return FileResponse(os.path.join(frontend_dir, 'index.html'))


@app.get("/company/{page}")
def serve_company(page: str):
    """회사소개 서브페이지 제공"""
    file_path = os.path.join(frontend_dir, 'company', f'{page}.html')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_dir, 'index.html'))


@app.get("/products/{page}")
def serve_products(page: str):
    """제품소개 서브페이지 제공"""
    file_path = os.path.join(frontend_dir, 'products', f'{page}.html')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_dir, 'index.html'))


@app.get("/support/{page}")
def serve_support(page: str):
    """고객지원 서브페이지 제공"""
    file_path = os.path.join(frontend_dir, 'support', f'{page}.html')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_dir, 'index.html'))


@app.get("/api/health")
def health_check():
    """서버 상태 확인 엔드포인트"""
    return {"status": "ok", "service": "만성코프레이션 API"}
