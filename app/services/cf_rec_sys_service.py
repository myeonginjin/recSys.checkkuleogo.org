from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from models.schemas import Book, BookLike, Child, Recommend
import pandas as pd
import numpy as np


def get_user_item_matrix(likes_df: pd.DataFrame) -> pd.DataFrame:
    """사용자-아이템 행렬을 생성하는 함수"""
    return likes_df.pivot_table(
        index="user_idx", columns="book_idx", values="is_like", fill_value = -1 #행동패턴이 있는 모든 유저와 북으로 구성된 피벗 테이블 (담긴 정보는 좋아요/싫어요/무반응)
    )


def calculate_cosine_similarity(user_item_matrix: pd.DataFrame) -> pd.DataFrame:
    """코사인 유사도를 계산하는 함수"""
    return pd.DataFrame(   
        cosine_similarity(user_item_matrix), #라이브러리가 유저들의 행동패턴을 통해 유저간 유사도를 측정해놓은 테이블 만듦, 머신러닝에 쓰일 가공된 데이터를 만듦
        index=user_item_matrix.index,
        columns=user_item_matrix.index,
    )


def generate_recommendations( #머신러닝
    user_item_matrix: pd.DataFrame, user_similarities_df: pd.DataFrame, active_users: set
) -> dict:
    """추천 결과를 생성하는 함수"""
    recommendations = {}

    # 사용자 수 및 책 수를 가져옵니다.
    n_users, n_books = user_item_matrix.shape  ##행동패턴이 있는 모든 유저와 북으로 구성된 피벗 테이블의 행/열 길이

    # 추천 점수를 담을 배열 초기화
    scores = np.zeros((n_users, n_books))  #n_users는 피추천인, n_books 추천받을 책, n_users가 n_books열인 2차원 배열

    # 유사한 사용자들의 점수를 가중합하여 점수 계산
    for user_id in user_item_matrix.index:
        # 현재 사용자와 유사한 사용자 찾기 (상위 10명)
        similar_users = (
            user_similarities_df.loc[user_id].nlargest(10).index[1:] # user_id는 현재 피추천인 similar_users는 피추천인과 유사한 상위 10명 
        )  # 자기 자신 제외

        # 유사한 사용자가 없을 경우 건너뛰기
        if len(similar_users) == 0:
            continue

        sim_scores = user_similarities_df.loc[user_id][similar_users] #상위 10명의 각 유사도 점수

        # 유사한 사용자의 좋아요와 싫어요를 기반으로 가중 점수 계산
        for similar_user in similar_users:
            liked_books = user_item_matrix.loc[similar_user][   #랭커가 좋아요 누른 책 목록, 값은 1로
                user_item_matrix.loc[similar_user] == 1
            ].index
            disliked_books = user_item_matrix.loc[similar_user][  #랭커가 싫어요 누른 책 목록, 값은 0으로
                user_item_matrix.loc[similar_user] == 0
            ].index

            # user_item_matrix의 유효한 열(책 인덱스)만 사용
            liked_books_valid = liked_books[liked_books.isin(user_item_matrix.columns)] #혹시나 user_item_matrix에 없는 아이템인지 확인 (단순한 유효성 검사)
            disliked_books_valid = disliked_books[ #위와 동일 
                disliked_books.isin(user_item_matrix.columns)
            ]

            # 유효한 liked_books가 있을 경우 점수 계산
            if not liked_books_valid.empty:
                for book in liked_books_valid: #피추천인과 유사한 랭커들이 좋아요 누른 책 목록
                    book_index = user_item_matrix.columns.get_loc(book)
                    scores[   #피추천인 행, 추천받을 책 열로 이루어진 배열에, 만족예측점수를 넣는다. (이 점수는 코사인 유사도를 통해 계산된 유저간 해턴 유사도)
                        user_item_matrix.index.get_loc(user_id), book_index
                    ] += sim_scores[similar_user]

            # 유효한 disliked_books가 있을 경우 점수 계산
            if not disliked_books_valid.empty:
                for book in disliked_books_valid:
                    book_index = user_item_matrix.columns.get_loc(book)
                    scores[
                        user_item_matrix.index.get_loc(user_id), book_index
                    ] -= sim_scores[similar_user] #싫어요 패턴일 시 점수를 차감. 싫어요가 많을 시 오히려 추천받지 않아야할 책. 

    # 각 사용자의 책 추천 목록 생성, 여기서 휴면 유저는 추천에서 제외. 이곳에서 해주는 이유는 그 사람의 행동패턴은 머신러닝에 학습 데이터로 활용되어야 함
    for user_id in user_item_matrix.index:
        if user_id not in active_users:  # 휴면 유저는 추천에서 제외
            continue

        user_books = user_item_matrix.loc[user_id]  # 사용자가 이미 평가한 책
        # 추천 점수에서 사용자가 평가하지 않은 책만 필터링하고 상위 50개 추천
        recommended_books = pd.Series(
            scores[user_item_matrix.index.get_loc(user_id)],
            index=user_item_matrix.columns,
        )
        recommended_books = recommended_books[user_books == -1].nlargest(50) #아직 평가를 하지 않은 책으로만 추천을 받아야함. 

        # 추천 책과 점수를 튜플로 묶어서 저장
        recommendations[user_id] = [  
            (book, recommended_books[book]) for book in recommended_books.index  #최종적으로 책idx와 책 추천 SCORE
        ]

    return recommendations


def cf_recommendation(db: Session) -> None:
    """추천 시스템 실행 함수"""
    try:
        # Child 테이블에서 is_active 상태가 True인 사용자만 필터링
        active_users_query = db.query(Child.child_idx).filter(Child.is_active == True).all()
        active_users = set(user.child_idx for user in active_users_query)  # 추천 대상 유저 목록

        likes_query = ( #읽을 수 있는 타입의 좋아요 테이블
            db.query(BookLike)
            .join(Child, BookLike.child_idx == Child.child_idx)
            .all()
        )
        likes_data = [ #가공된 좋아요 테이블
            (BookLike.book_idx, BookLike.child_idx, BookLike.is_like)
            for BookLike in likes_query
        ]
        likes_df = pd.DataFrame(likes_data, columns=["book_idx", "user_idx", "is_like"]) #행은 idx

        user_item_matrix = get_user_item_matrix(likes_df) 
        user_similarities_df = calculate_cosine_similarity(user_item_matrix) #행 유저, 열 유저 그리고 테이블에 담긴 정보는 행-열 유저간의 유사도 정도 (0.0~1.0)

        recommendations = generate_recommendations(
            user_item_matrix, user_similarities_df, active_users    #user_similarities_df를 통해 피추천인과 유사한 사람을 찾고, user_item_matrix에서 그 사람의 좋아요 항목을 찾는다.
        )
        return recommendations
    except Exception as e:
        print(f"CF : 추천 시스템 실행 중 오류가 발생했습니다: {e}")
        print(f"오류의 타입: {type(e).__name__}")  # 예외의 타입 출력
        return {}
