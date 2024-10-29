import time
from collections import defaultdict
from requests import Session
from models.schemas import Book, Recommend, BookLike, Child
from services.cf_rec_sys_service import cf_recommendation
from services.cs_rec_sys_service import cs_recommendation

def calculate_dynamic_weight(user_likes, user_count, min_users_threshold=100, min_likes_threshold=5, high_weight=0.7, low_weight=0.3):
    """
    동적 가중치를 계산하는 함수
    """
    if user_count < min_users_threshold or user_likes < min_likes_threshold:
        return low_weight, high_weight  # 콘텐츠 기반 필터링에 높은 가중치
    else:
        return high_weight, low_weight  # 사용자 기반 협업 필터링에 높은 가중치

def get_user_likes(db: Session, user_id: int) -> int:
    """
    주어진 사용자의 좋아요 수를 데이터베이스에서 가져오는 함수
    """
    try:
        like_count = db.query(BookLike).filter(BookLike.child_idx == user_id).count()
        return like_count
    except Exception as e:
        print(f"좋아요 수를 가져오는 중 오류 발생: {e}")
        return 0

def get_total_user_count(db: Session) -> int:
    """
    시스템의 전체 사용자 수를 가져오는 함수
    """
    try:
        user_count = db.query(Child).count()
        return user_count
    except Exception as e:
        print(f"전체 사용자 수를 가져오는 중 오류 발생: {e}")
        return 0
    
def hybrid_recommendation(db: Session, top_n: int = 30) -> None:
    """
    협업 필터링과 콘텐츠 기반 필터링 시스템의 결과를 결합하여 하이브리드 책 추천을 생성합니다.
    Parameters:
    - db (Session): 데이터베이스에 접근하기 위한 세션.
    - top_n (int): 각 사용자에게 반환할 상위 추천 수. 기본값은 30입니다.
    """
    try:
        start_time = time.time()  # 시작 시간 기록

        user_count = get_total_user_count(db)
        
        # 각 추천 시스템에서 추천 결과 생성
        recommendations_1 = cf_recommendation(db)  # {user_id: [(book_id, cf_score), ...]}
        recommendations_2 = cs_recommendation(db)  # {user_id: [(book_id, cs_score), ...]}

        hybrid_recommendations = {}

        # 모든 사용자 ID 가져오기
        all_users = set(recommendations_1.keys()).union(set(recommendations_2.keys()))

        for user in all_users:

            user_likes = get_user_likes(db, user)
            cf_weight, cs_weight = calculate_dynamic_weight(user_likes, user_count)  # 동적 가중치 계산
            book_scores = defaultdict(float)

            # 첫 번째 추천 시스템 점수 반영
            for book, cf_score in recommendations_1.get(user, []):
                # 두 번째 추천 시스템에 있는 책이면 점수 합산
                cs_score = next((score for b, score in recommendations_2.get(user, []) if b == book), 0)
                book_scores[book] += (cf_score * cf_weight) + (cs_score * cs_weight)

            # 두 번째 추천 시스템에만 있는 책 처리
            for book, cs_score in recommendations_2.get(user, []):
                if book not in book_scores:
                    book_scores[book] += cs_score * cs_weight

                
            # 추천 점수를 기준으로 정렬하고 상위 N개 추천
            top_books = sorted(book_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
            hybrid_recommendations[user] = [book for book, score in top_books]

        # 추천 결과를 데이터베이스에 저장
        recommend_entries = [
            Recommend(book_idx=book.book_idx if isinstance(book, Book) else book, child_idx=user)
            for user, books in hybrid_recommendations.items()
            for book in books
        ]

        db.bulk_save_objects(recommend_entries)
        db.commit()
        
        # 각 사용자에게 추천된 책 출력
        for user, recommended_books in hybrid_recommendations.items():
            recommended_titles = [
                book.book_title if isinstance(book, Book) else str(book)
                for book in recommended_books
            ]
            print(f"User {user}에게 추천된 책: {recommended_titles}")
        end_time = time.time()  # 종료 시간 기록
        elapsed_time = end_time - start_time  # 경과 시간 계산
        print(f"추천 생성에 걸린 시간: {elapsed_time:.2f} 초")
    
    except Exception as e:
        print(f"추천 시스템 실행 중 오류가 발생했습니다: {e}")
        print(f"오류의 타입: {type(e).__name__}")  # 예외의 타입 출력
    finally:
        db.close()  # DB 세션 종료

