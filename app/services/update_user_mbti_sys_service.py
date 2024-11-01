from sqlalchemy.orm import Session
from models.schemas import BookMBTI, Child, ChildMBTI, ChildMBTILog, BookLike
from sqlalchemy import func


def calculate_average_mbti_vector(mbti_vectors):
    """
    평균 MBTI 벡터를 계산하는 함수
    """
    if not mbti_vectors:
        return None
    
    total_mbti = [0, 0, 0, 0]
    for vector in mbti_vectors:
        total_mbti[0] += vector.mbti_e
        total_mbti[1] += vector.mbti_s
        total_mbti[2] += vector.mbti_t
        total_mbti[3] += vector.mbti_j
    
    avg_mbti = [int(value / len(mbti_vectors)) for value in total_mbti]
    return avg_mbti


def update_user_mbti_with_likes(db: Session, hybrid_recommendations: dict) -> None:
    try:
        # 추천된 사용자만 좋아요 누른 책의 MBTI 정보 가져오기
        user_ids = hybrid_recommendations.keys()
        likes_query = (
            db.query(BookLike)
            .filter(BookLike.child_idx.in_(user_ids))
            .all()
        )
        
        # 사용자별 좋아요 누른 책 수집
        user_book_likes = {}
        for like in likes_query:
            if like.child_idx not in user_book_likes:
                user_book_likes[like.child_idx] = []
            user_book_likes[like.child_idx].append(like.book_idx)
        
        # 책 ID별 MBTI 벡터 매핑
        all_book_ids = [book_id for book_ids in user_book_likes.values() for book_id in book_ids]
        mbti_vectors = db.query(BookMBTI).filter(BookMBTI.book_idx.in_(all_book_ids)).all()
        book_mbti_map = {vector.book_idx: vector for vector in mbti_vectors}
        
        # 사용자별 평균 MBTI 벡터 계산 및 업데이트 데이터 생성
        update_data = []
        new_log_data = []
        for user_id, book_ids in user_book_likes.items():
            user_mbti_vectors = [book_mbti_map[book_id] for book_id in book_ids if book_id in book_mbti_map]
            avg_mbti_vector = calculate_average_mbti_vector(user_mbti_vectors)
            if not avg_mbti_vector:
                continue
            
            # 사용자의 기존 MBTI 정보 가져오기
            child_mbti = db.query(ChildMBTI).filter(ChildMBTI.child_idx == user_id).first()
            if child_mbti:
                # 기존 MBTI와 새 MBTI 로그 출력
                old_mbti = (child_mbti.mbti_e, child_mbti.mbti_s, child_mbti.mbti_t, child_mbti.mbti_j)
                new_mbti = tuple(avg_mbti_vector)
                
                # 업데이트 데이터 추가
                child_mbti.mbti_e, child_mbti.mbti_s, child_mbti.mbti_t, child_mbti.mbti_j = avg_mbti_vector
                update_data.append(child_mbti)
            else:
                # 사용자가 기존에 MBTI 정보가 없을 경우 새로 생성
                new_child_mbti = ChildMBTI(
                    child_idx=user_id,
                    mbti_e=avg_mbti_vector[0],
                    mbti_s=avg_mbti_vector[1],
                    mbti_t=avg_mbti_vector[2],
                    mbti_j=avg_mbti_vector[3],
                )
                db.add(new_child_mbti)

            # ChildMBTILog에 로그 추가
            new_child_mbti_log = ChildMBTILog(
                child_idx=user_id,
                mbti_e=avg_mbti_vector[0],
                mbti_s=avg_mbti_vector[1],
                mbti_t=avg_mbti_vector[2],
                mbti_j=avg_mbti_vector[3],
                is_survey_result=False
            )
            new_log_data.append(new_child_mbti_log)
        
        # 벌크 업데이트 및 로그 삽입 수행
        if update_data:
            db.bulk_save_objects(update_data)
        if new_log_data:
            db.bulk_save_objects(new_log_data)
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"UD : 사용자 MBTI 업데이트 중 오류 발생: {e}")
        print(f"오류의 타입: {type(e).__name__}")
