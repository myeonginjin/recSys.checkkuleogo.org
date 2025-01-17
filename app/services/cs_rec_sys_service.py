from sqlalchemy.orm import Session
from sqlalchemy import select
import numpy as np
from models.schemas import Book, Child, Recommend
import time


# 피벗 적용
def calculate_cosine_similarity_matrix(child_matrix, book_matrix):
    """모든 아이와 책의 코사인 유사도를 매트릭스로 계산하는 함수"""
    book_norms = np.linalg.norm(book_matrix, axis=1)
    child_norms = np.linalg.norm(child_matrix, axis=1)
    
    similarity_matrix = np.dot(child_matrix, book_matrix.T) / np.outer(
        child_norms, book_norms
    )
    return np.nan_to_num(similarity_matrix)


def cs_recommendation(session: Session):

    # 모든 책 데이터를 가져오기
    books = session.execute(select(Book)).scalars().all()
    # 활성화된 사용자만 필터링하여 가져오기
    children = (
        session.execute(select(Child).where(Child.is_active == True)).scalars().all()
    )

    # 각 아이와 책의 MBTI를 매트릭스로 변환
    book_vectors = np.array([get_book_mbti_vector(book) for book in books])
    child_vectors = np.array([get_child_mbti_vector(child) for child in children])

    # 모든 아이와 책 간의 유사도 매트릭스 계산
    similarity_matrix = calculate_cosine_similarity_matrix(child_vectors, book_vectors)

    recommendations = {}

    for i, child in enumerate(children):
        # 유사도 기준으로 상위 50개의 책 인덱스 추출
        top_book_indices = np.argsort(-similarity_matrix[i])[:50]

        # 추천 결과를 저장
        recommended_books = []
        for book_index in top_book_indices:
            book_id = books[book_index].book_idx
            score = similarity_matrix[i][book_index]
            recommended_books.append((book_id, score))

        recommendations[child.child_idx] = recommended_books

    return recommendations


def get_child_mbti_vector(child):
    """아이의 MBTI를 벡터로 변환하는 로직"""
    if child.childMBTI is None:
        print(f"{child.child_name}의 MBTI 정보가 없습니다.")
        return [0, 0, 0, 0]  # 기본값 반환

    child_mbti = child.childMBTI
    return [child_mbti.mbti_e, child_mbti.mbti_s, child_mbti.mbti_t, child_mbti.mbti_j]


def get_book_mbti_vector(book):
    """책의 MBTI를 벡터로 변환하는 로직"""
    mbti = book.bookMBTI
    return [mbti.mbti_e, mbti.mbti_s, mbti.mbti_t, mbti.mbti_j]
