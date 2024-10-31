import numpy as np
from sqlalchemy.orm import Session
from sklearn.metrics.pairwise import cosine_similarity


def mbti_to_vector(mbti: str) -> np.array:
    """
    MBTI를 4차원 벡터로 변환
    E/I, S/N, T/F, J/P 각각을 1 또는 -1로 변환
    """
    mbti_map = {"E": 1, "I": -1, "S": 1, "N": -1, "T": 1, "F": -1, "J": 1, "P": -1}
    return np.array([mbti_map[mbti[i]] for i in range(4)])


def calculate_average_mbti_vector(book_mbtis):
    """
    추천된 책 목록의 MBTI를 벡터로 변환한 후 평균 벡터를 계산
    """
    vectors = [mbti_to_vector(mbti) for mbti in book_mbtis if mbti]
    if not vectors:
        return None
    return np.mean(vectors, axis=0)


def vector_to_mbti(vector: np.array) -> str:
    """
    평균 벡터를 가장 가까운 MBTI로 변환
    """
    traits = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
    return "".join([traits[i][0] if vector[i] > 0 else traits[i][1] for i in range(4)])


def update_user_mbti_with_vector(db: Session, hybrid_recommendations: dict):
    """
    추천 목록을 기반으로 유저의 MBTI를 벡터 방식으로 동적으로 업데이트
    """
    try:
        for user, recommended_books in hybrid_recommendations.items():
            # 추천된 책 목록의 MBTI 속성 수집
            book_mbtis = [
                db.query(Book).filter(Book.book_idx == book_id).first().mbti
                for book_id in recommended_books
                if db.query(Book).filter(Book.book_idx == book_id).first().mbti
            ]

            if not book_mbtis:
                continue

            # 추천된 책 MBTI 평균 벡터 계산
            avg_mbti_vector = calculate_average_mbti_vector(book_mbtis)

            # 유저의 기존 MBTI를 벡터로 변환
            user_record = db.query(Child).filter(Child.child_idx == user).first()
            if not user_record or not user_record.mbti:
                continue
            user_mbti_vector = mbti_to_vector(user_record.mbti)

            # 유사도 계산 및 사용자 MBTI 업데이트 결정
            similarity = cosine_similarity([user_mbti_vector], [avg_mbti_vector])[0][0]
            if similarity < 0.95:  # 유사도가 낮으면 업데이트
                new_mbti = vector_to_mbti(avg_mbti_vector)
                user_record.mbti = new_mbti
                print(f"User {user}의 MBTI가 {new_mbti}로 업데이트되었습니다.")

        db.commit()  # 모든 변경 사항 커밋
    except Exception as e:
        print(f"MBTI 업데이트 중 오류 발생: {e}")
    finally:
        db.close()  # DB 세션 종료
