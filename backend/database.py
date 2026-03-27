"""
데이터베이스 연결 설정 모듈
PostgreSQL 연결을 시도하고, 실패 시 SQLite로 자동 폴백
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# .env 파일 로드 (backend 상위 디렉토리의 .env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# 데이터베이스 URL — 미설정 시 SQLite 사용
_DB_URL = os.getenv("DATABASE_URL", "sqlite:///./mansung.db")

# SQLite 경로 (폴백용)
_SQLITE_URL = "sqlite:///" + os.path.join(os.path.dirname(__file__), "mansung.db")


def _make_engine(url: str):
    """
    DB URL에 맞는 SQLAlchemy 엔진 생성.
    SQLite와 PostgreSQL 설정을 분기 처리.
    """
    if url.startswith("sqlite"):
        return create_engine(url, connect_args={"check_same_thread": False})
    # psycopg2 드라이버 호환: postgresql+psycopg:// → postgresql+psycopg2://
    if url.startswith("postgresql+psycopg://"):
        url = url.replace("postgresql+psycopg://", "postgresql+psycopg2://", 1)
    return create_engine(url, pool_pre_ping=True, pool_size=5, max_overflow=10)


def _try_connect(eng) -> bool:
    """
    엔진 연결 테스트.
    연결 성공 시 True, 실패 시 False 반환.
    """
    try:
        with eng.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


# PostgreSQL 연결 시도 → 실패 시 SQLite 폴백
engine = _make_engine(_DB_URL)
if not _DB_URL.startswith("sqlite") and not _try_connect(engine):
    print("[DB] PostgreSQL 연결 실패 -> SQLite 로컬 DB로 전환합니다.")
    engine = _make_engine(_SQLITE_URL)
else:
    db_type = "SQLite" if _DB_URL.startswith("sqlite") else "PostgreSQL"
    print(f"[DB] {db_type} 연결 성공")

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 베이스 클래스
Base = declarative_base()


def get_db():
    """
    FastAPI 의존성 주입용 DB 세션 생성기.
    요청마다 세션을 생성하고 완료 후 자동으로 닫음.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
