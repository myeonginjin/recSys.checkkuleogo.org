import mysql.connector
import numpy as np
import pandas as pd

# MySQL connection setup
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootroot",
    database="kkuleogi"
)

cursor = db_connection.cursor()

# 사용자 수 설정
num_users = 30  # 사용자 수
num_books = 40  # 총 책 수 (31~40)

# 가상의 장르 데이터 (예시)
genres = {
    'Fantasy': range(31, 34),  # 31, 32, 33
    'Science Fiction': range(34, 38),  # 34, 35, 36, 37
    'Romance': range(38, 41)  # 38, 39, 40
}

# 사용자 패턴 설정 (30명의 사용자 프로필을 무작위로 생성)
user_profiles = {
    i: np.random.choice(['Fantasy', 'Science Fiction', 'Romance'], size=np.random.randint(1, 4), replace=False).tolist()
    for i in range(1, num_users + 1)
}

# 사용자-책 피드백 데이터 생성
likes_data = []
for user_id in range(1, num_users + 1):
    preferred_genres = user_profiles[user_id]  # 사용자 프로필에 따라 선호 장르 선택
    liked_books = []

    # 선호하는 장르의 책을 랜덤으로 선택
    for genre in preferred_genres:
        book_ids = genres[genre]
        if len(book_ids) > 0:
            num_to_choose = np.random.randint(1, min(4, len(book_ids) + 1))  # 최대 장르의 책 수까지 선택
            liked_books.extend(np.random.choice(book_ids, size=num_to_choose, replace=False))

    # 싫어요 책 수 결정 (무작위로 선택)
    disliked_books = np.random.choice(range(31, num_books + 1), size=np.random.randint(0, 3), replace=False)

    # 좋아요 데이터 추가
    for book_id in liked_books:
        likes_data.append((user_id, book_id, 1))  # 좋아요는 1

    # 싫어요 데이터 추가
    for book_id in disliked_books:
        likes_data.append((user_id, book_id, -1))  # 싫어요는 -1

# 데이터프레임으로 변환
likes_df = pd.DataFrame(likes_data, columns=['user_id', 'book_id', 'is_like'])

# 데이터베이스에 저장
insert_query = """
INSERT INTO book_like (child_idx, book_idx, is_like) VALUES (%s, %s, %s)
"""
for index, row in likes_df.iterrows():
    try:
        cursor.execute(insert_query, (int(row['user_id']), int(row['book_id']), int(row['is_like'])))
    except mysql.connector.Error as err:
        print(f"Error: {err} - Row: {row}")

# Commit the transaction
db_connection.commit()

# Close the cursor and connection
cursor.close()
db_connection.close()

print(f"Inserted {len(likes_df)} records into the book_like table.")
