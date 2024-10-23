from sqlalchemy import Column, TEXT, BIGINT, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Book(Base):
    __tablename__ = "book"

    book_idx = Column(BIGINT, primary_key=True, autoincrement=True)
    book_title = Column(TEXT, nullable=False)
    book_author = Column(TEXT, nullable=False)
    book_publisher = Column(TEXT, nullable=False)
    book_summary = Column(TEXT, nullable=True)
    book_content = Column(TEXT, nullable=True)
    book_mbti_id = Column(BIGINT, nullable=True)  # ForeignKey 설정이 필요하면 추가
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )
