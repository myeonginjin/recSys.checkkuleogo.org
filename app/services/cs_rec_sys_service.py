from sqlalchemy.orm import Session
from sqlalchemy import select
import numpy as np
from models.schemas import Book, Child, Recommend
import time


def calculate_cosine_similarity(child_vector, book_vector):
    """코사인 유사도를 계산하는 함수"""
    if np.linalg.norm(child_vector) == 0 or np.linalg.norm(book_vector) == 0:
        return 0.0
    return np.dot(child_vector, book_vector) / (
        np.linalg.norm(child_vector) * np.linalg.norm(book_vector)
    )


def recommend_books(session: Session):
    # 추천 생성 및 저장에 걸리는 시간 측정
    start_time = time.time()  # 시작 시간 기록
    cnt = 0  # 생성된 추천 도서 개수

    # 모든 아이와 책 데이터를 가져오기
    books = session.execute(select(Book)).scalars().all()
    children = session.execute(select(Child)).scalars().all()

    recommendations_to_add = []  # 일괄 저장을 위한 리스트

    for child in children:
        child_mbti = get_child_mbti_vector(child)  # 아이의 MBTI를 벡터로 변환하는 함수
        recommendations = []

        for book in books:
            book_mbti = get_book_mbti_vector(book)  # 책의 MBTI를 벡터로 변환하는 함수
            similarity = calculate_cosine_similarity(child_mbti, book_mbti)
            recommendations.append((book, similarity))

        # 유사도 기준으로 정렬하고 상위 10개의 책을 추천
        recommendations.sort(key=lambda x: x[1], reverse=True)
        top_books = recommendations[:10]

        # 추천 결과를 일괄 추가 리스트에 저장
        for book, _ in top_books:
            cnt += 1
            elapsed_time = time.time() - start_time  # 경과 시간 계산
            print(
                f"현재까지 생성된 추천 책 개수 : {cnt}     책 제목 : {book.book_title}     경과 시간: {elapsed_time:.2f} 초"
            )

            # 추천 객체를 리스트에 추가 (일괄 저장용)
            recommendations_to_add.append(
                Recommend(book_idx=book.book_idx, child_idx=child.child_idx)
            )

    # 모든 추천 결과를 일괄 커밋
    session.bulk_save_objects(recommendations_to_add)  # 일괄 저장
    session.commit()  # 최종 커밋

    # 전체 소요 시간 출력
    end_time = time.time()  # 끝 시간 기록
    total_time = end_time - start_time
    print(f"추천 목록 생성 및 저장에 걸린 총 시간: {total_time:.2f} 초")


def get_child_mbti_vector(child):
    """아이의 MBTI를 벡터로 변환하는 로직"""
    if child.childMBTI is None:
        print(f"{child.child_name}의 MBTI 정보가 없습니다.")
        return [0, 0, 0, 0]  # 기본값 반환

    child_mbti = child.childMBTI
    return [child_mbti.mbti_e, child_mbti.mbti_s, child_mbti.mbti_t, child_mbti.mbti_j]


def get_book_mbti_vector(book):
    """책의 MBTI를 벡터로 변환하는 로직"""
    mbti = book.bookMBTI  # book 객체에서 MBTI 정보 가져오기
    return [mbti.mbti_e, mbti.mbti_s, mbti.mbti_t, mbti.mbti_j]
