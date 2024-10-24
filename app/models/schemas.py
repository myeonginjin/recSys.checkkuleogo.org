from sqlalchemy import Column, TEXT, BIGINT, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = "book"

    book_idx = Column(BIGINT, primary_key=True, autoincrement=True)
    book_title = Column(TEXT, nullable=False)
    book_author = Column(TEXT, nullable=False)
    book_publisher = Column(TEXT, nullable=False)
    book_summary = Column(TEXT, nullable=True)
    book_content = Column(TEXT, nullable=True)
    bookMBTI = relationship("BookMBTI", uselist=False, back_populates="book")
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class BookMBTI(Base):
    __tablename__ = "book_mbti"

    book_mbti_idx = Column(BIGINT, primary_key=True, autoincrement=True)
    book_idx = Column(
        BIGINT, ForeignKey("book.book_idx"), nullable=False
    )  # ForeignKey 타입 수정
    mbti_e = Column(Integer)
    mbti_s = Column(Integer)
    mbti_t = Column(Integer)
    mbti_j = Column(Integer)

    # Book과의 관계 설정 (1:1 관계)
    book = relationship("Book", back_populates="bookMBTI")


class Child(Base):
    __tablename__ = "child"

    child_idx = Column(BIGINT, primary_key=True, autoincrement=True)
    child_name = Column(TEXT, nullable=False)
    child_age = Column(TEXT, nullable=False)
    child_birth = Column(TIMESTAMP, nullable=False)
    child_gender = Column(TEXT, nullable=False)
    child_mbti = Column(TEXT, nullable=True)
    childMBTI = relationship("ChildMBTI", uselist=False, back_populates="child")
    parent_id = Column(BIGINT, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class ChildMBTI(Base):
    __tablename__ = "child_mbti"

    child_mbti_idx = Column(BIGINT, primary_key=True, autoincrement=True)
    child_idx = Column(
        BIGINT, ForeignKey("child.child_idx"), nullable=False
    )  # ForeignKey 타입 수정
    mbti_e = Column(Integer)
    mbti_s = Column(Integer)
    mbti_t = Column(Integer)
    mbti_j = Column(Integer)

    # Child와의 관계 설정 (1:1 관계)
    child = relationship("Child", back_populates="childMBTI")


class Recommend(Base):
    __tablename__ = "recommend"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    book_idx = Column(
        BIGINT, ForeignKey("book.book_idx"), nullable=False
    )  # ForeignKey 추가
    child_idx = Column(
        BIGINT, ForeignKey("child.child_idx"), nullable=False
    )  # ForeignKey 추가
