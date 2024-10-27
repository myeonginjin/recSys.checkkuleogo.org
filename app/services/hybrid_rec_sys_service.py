import time
from requests import Session
from models.schemas import Book, Child, Recommend
from services.cf_rec_sys_service import cf_recommendation
from services.cs_rec_sys_service import cs_recommendation

def hybrid_recommendation(db: Session, top_n: int = 30) -> None:
    """
    협업 필터링과 콘텐츠 기반 필터링 시스템의 결과를 결합하여 하이브리드 책 추천을 생성합니다
    Parameters:
    - db (Session): 데이터베이스에 접근하기 위한 세션.
    - top_n (int): 각 사용자에게 반환할 상위 추천 수. 기본값은 30입니다.
    """
    try:
        start_time = time.time()  # 시작 시간 기록
        # 각 추천 시스템에서 추천 결과 생성
        recommendations_1 = cf_recommendation(db)
        recommendations_2 = cs_recommendation(db)

        # 하이브리드 추천 결과를 저장할 딕셔너리 초기화
        hybrid_recommendations = {}
        
        # 모든 사용자 ID 가져오기
        all_users = set(recommendations_1.keys()).union(set(recommendations_2.keys()))

        for user in all_users:
            # 두 추천 시스템에서 책 목록 가져오기
            books_1 = recommendations_1.get(user, [])
            books_2 = recommendations_2.get(user, [])

            # 두 책 목록 결합하여 중복 제거
            combined_books = list(set(books_1) | set(books_2))

            # 책 추천 점수 초기화
            book_scores = {book: 0 for book in combined_books}

            # 첫 번째 추천 시스템 점수 부여 (가중치 0.5)
            for book in books_1:
                book_scores[book] += 0.5

            # 두 번째 추천 시스템 점수 부여 (가중치 0.5)
            for book in books_2:
                book_scores[book] += 0.5

            # 두 추천 목록에서 공통으로 나타나는 책에 추가 가중치 부여
            common_books = set(books_1) & set(books_2)
            for book in common_books:
                book_scores[book] += 0.3  # 공통 책에 대한 추가 가중치

            # 추천 점수를 기준으로 정렬하고 상위 N개 추천
            top_books = sorted(book_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
            hybrid_recommendations[user] = [book for book, score in top_books]

        # 추천 결과를 데이터베이스에 저장할 준비
        recommend_entries = [
            Recommend(book_idx=book.book_idx if isinstance(book, Book) else book, child_idx=user)
            for user, books in hybrid_recommendations.items()
            for book in books
        ]

        # 추천 결과를 데이터베이스에 저장
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
