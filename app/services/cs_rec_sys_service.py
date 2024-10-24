from sqlalchemy.orm import Session
from sqlalchemy import select
import numpy as np
from models.schemas import Book, Child, Recommend


def calculate_cosine_similarity(child_vector, book_vector):
    """코사인 유사도를 계산하는 함수"""
    if np.linalg.norm(child_vector) == 0 or np.linalg.norm(book_vector) == 0:
        return 0.0
    return np.dot(child_vector, book_vector) / (
        np.linalg.norm(child_vector) * np.linalg.norm(book_vector)
    )


def recommend_books(session: Session):

    # 모든 아이와 책 데이터를 가져오기
    books = session.execute(select(Book)).scalars().all()
    children = session.execute(select(Child)).scalars().all()

    print("1")
    # print(children)

    for c in children:
        print(c.child_name)

    for child in children:
        child_mbti = get_child_mbti_vector(child)  # 아이의 MBTI를 벡터로 변환하는 함수
        recommendations = []

        print("\n\n 2 : " + child.child_name + " \n\n")

        for book in books:

            print("3 : " + book.book_title)

            book_mbti = get_book_mbti_vector(book)  # 책의 MBTI를 벡터로 변환하는 함수
            similarity = calculate_cosine_similarity(child_mbti, book_mbti)

            recommendations.append((book, similarity))

        # 유사도 기준으로 정렬하고 상위 10개의 책을 추천
        recommendations.sort(key=lambda x: x[1], reverse=True)
        top_books = recommendations[:10]

        # 추천 결과를 recommend 테이블에 저장
        for book, _ in top_books:
            session.add(Recommend(book_idx=book.book_idx, child_idx=child.child_idx))
    session.commit()


def get_child_mbti_vector(child):
    """아이의 MBTI를 벡터로 변환하는 로직"""
    # 예시: [mbti_e, mbti_s, mbti_t, mbti_j] 형태로 반환
    if child.childMBTI is None:
        print(f"{child.child_name}의 MBTI 정보가 없습니다.")
        return [0, 0, 0, 0]  # 기본값 반환

    child_mbti = child.childMBTI

    print("\n\n>>> " + child.child_name + " <<<<\n\n")

    return [child_mbti.mbti_e, child_mbti.mbti_s, child_mbti.mbti_t, child_mbti.mbti_j]


def get_book_mbti_vector(book):
    """책의 MBTI를 벡터로 변환하는 로직"""
    mbti = book.bookMBTI  # book 객체에서 MBTI 정보 가져오기
    return [mbti.mbti_e, mbti.mbti_s, mbti.mbti_t, mbti.mbti_j]
