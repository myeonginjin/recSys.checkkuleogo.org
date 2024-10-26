from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from models.schemas import Book, BookLike, Child, Recommend
import pandas as pd
import numpy as np


def get_user_item_matrix(likes_df: pd.DataFrame) -> pd.DataFrame:
    """사용자-아이템 행렬을 생성하는 함수"""
    return likes_df.pivot_table(
        index="user_idx", columns="book_idx", values="is_like", fill_value=-1
    )


def calculate_cosine_similarity(user_item_matrix: pd.DataFrame) -> pd.DataFrame:
    """코사인 유사도를 계산하는 함수"""
    return pd.DataFrame(
        cosine_similarity(user_item_matrix),
        index=user_item_matrix.index,
        columns=user_item_matrix.index,
    )


def generate_recommendations(
    user_item_matrix: pd.DataFrame, user_similarities_df: pd.DataFrame
) -> dict:
    """추천 결과를 생성하는 함수"""
    recommendations = {}

    # 사용자 수 및 책 수를 가져옵니다.
    n_users, n_books = user_item_matrix.shape

    # 추천 점수를 담을 배열 초기화
    scores = np.zeros((n_users, n_books))

    # 유사한 사용자들의 점수를 가중합하여 점수 계산
    for user_id in user_item_matrix.index:
        # 현재 사용자와 유사한 사용자 찾기 (상위 5명)
        similar_users = (
            user_similarities_df.loc[user_id].nlargest(6).index[1:]
        )  # 자기 자신 제외

        # 유사한 사용자가 없을 경우 건너뛰기
        if len(similar_users) == 0:
            continue

        sim_scores = user_similarities_df.loc[user_id][similar_users]

        # 유사한 사용자의 좋아요와 싫어요를 기반으로 가중 점수 계산
        for similar_user in similar_users:
            liked_books = user_item_matrix.loc[similar_user][
                user_item_matrix.loc[similar_user] == 1
            ].index
            disliked_books = user_item_matrix.loc[similar_user][
                user_item_matrix.loc[similar_user] == 0
            ].index

            # user_item_matrix의 유효한 열(책 인덱스)만 사용
            liked_books_valid = liked_books[liked_books.isin(user_item_matrix.columns)]
            disliked_books_valid = disliked_books[
                disliked_books.isin(user_item_matrix.columns)
            ]

            # 유효한 liked_books가 있을 경우 점수 계산
            if not liked_books_valid.empty:
                for book in liked_books_valid:
                    book_index = user_item_matrix.columns.get_loc(book)
                    scores[
                        user_item_matrix.index.get_loc(user_id), book_index
                    ] += sim_scores[similar_user]

            # 유효한 disliked_books가 있을 경우 점수 계산
            if not disliked_books_valid.empty:
                for book in disliked_books_valid:
                    book_index = user_item_matrix.columns.get_loc(book)
                    scores[
                        user_item_matrix.index.get_loc(user_id), book_index
                    ] -= sim_scores[similar_user]

    # 각 사용자의 책 추천 목록 생성
    for user_id in user_item_matrix.index:
        user_books = user_item_matrix.loc[user_id]  # 사용자가 이미 평가한 책
        # 추천 점수에서 사용자가 평가하지 않은 책만 필터링하고 상위 5개 추천
        recommended_books = pd.Series(
            scores[user_item_matrix.index.get_loc(user_id)],
            index=user_item_matrix.columns,
        )
        recommended_books = recommended_books[user_books == -1].nlargest(5)
        recommendations[user_id] = recommended_books.index.tolist()

    return recommendations


def run_recommendation(db: Session) -> None:
    """추천 시스템 실행 함수"""
    try:
        likes_query = db.query(BookLike).all()
        likes_data = [
            (BookLike.book_idx, BookLike.child_idx, BookLike.is_like)
            for BookLike in likes_query
        ]
        likes_df = pd.DataFrame(likes_data, columns=["book_idx", "user_idx", "is_like"])

        user_item_matrix = get_user_item_matrix(likes_df)
        user_similarities_df = calculate_cosine_similarity(user_item_matrix)

        recommendations = generate_recommendations(
            user_item_matrix, user_similarities_df
        )

        # 추천 결과를 한 번에 추가
        recommend_entries = [
            Recommend(book_idx=book_id, child_idx=user_id)
            for user_id, book_list in recommendations.items()
            for book_id in book_list
        ]

        db.bulk_save_objects(
            recommend_entries
        )  # bulk_save_objects를 사용하여 성능 향상
        db.commit()
        print("추천 결과가 데이터베이스에 저장되었습니다.")
        # 추천 목록을 콘솔에 출력
        for user_id, book_list in recommendations.items():
            print(f"User {user_id}에게 추천된 책: {book_list}")
    except Exception as e:
        print(f"추천 시스템 실행 중 오류가 발생했습니다: {e}")
        print(f"오류의 타입: {type(e).__name__}")  # 예외의 타입 출력
