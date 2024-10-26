-- 각 테이블 데이터만 싹 지워주기 (테이블은 삭제 안함)
SET FOREIGN_KEY_CHECKS = 0; -- 외래 키 제약 비활성화
TRUNCATE TABLE book;  -- 테이블 데이터 비우기
TRUNCATE TABLE book_mbti;
TRUNCATE TABLE child;
TRUNCATE TABLE child_mbti;
TRUNCATE TABLE user;
TRUNCATE TABLE recommend;
SET FOREIGN_KEY_CHECKS = 1; -- 외래 키 제약 다시 활성화


-- 유저 만명 더미 데이터 형성 프로시저
DELIMITER //
CREATE PROCEDURE InsertUserDummyData()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 10000 DO
        INSERT INTO user (created_at, updated_at, user_birth, user_email, user_gender, user_id, user_name, user_password, user_role)
        VALUES (NOW(), NOW(), DATE_ADD('1980-01-01', INTERVAL FLOOR(RAND() * 365 * 30) DAY), 
                CONCAT('user', i, '@example.com'), 
                IF(MOD(i, 2) = 0, 'Male', 'Female'), 
                CONCAT('user', i), 
                CONCAT('User ', i), 
                'password', 
                'USER');
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;


-- 책 mbti 더미데이터 생성 프로시저 
DELIMITER //
CREATE PROCEDURE InsertBookMBTIDummyData()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 10000 DO
        INSERT INTO book_mbti (mbti_e, mbti_s, mbti_t, mbti_j)
        VALUES (FLOOR(RAND() * 100), FLOOR(RAND() * 100), FLOOR(RAND() * 100), FLOOR(RAND() * 100));
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;


-- 책 만개 더미 데이터 형성 프로시저
DELIMITER //
CREATE PROCEDURE InsertBookDummyData()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 10000 DO
        INSERT INTO book (book_title, book_author, book_publisher, book_summary, book_content, book_mbti_id)
        VALUES (CONCAT('Book Title ', i), 
                CONCAT('Author ', i), 
                CONCAT('Publisher ', i), 
                'Sample summary text', 
                'Sample content text', 
                i);
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

-- 아이 MBTI 더미데이터 형성 프로시저 
DELIMITER //
CREATE PROCEDURE InsertChildMBTIDummyData()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 10000 DO
        INSERT INTO child_mbti (mbti_e, mbti_j, mbti_s, mbti_t, child_idx, child_mbti_idx, created_at, updated_at)
        VALUES (FLOOR(RAND() * 100), FLOOR(RAND() * 100), FLOOR(RAND() * 100), FLOOR(RAND() * 100), i, i, NOW(), NOW());
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;


-- 아이 만명 더미 데이터 형성 프로시저 
DELIMITER //
CREATE PROCEDURE InsertChildDummyData()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 10000 DO
        INSERT INTO child (child_name, child_age, child_birth, child_gender, child_mbti, parent_id)
        VALUES (CONCAT('Child', i), 
                FLOOR(RAND() * 10) + 5, 
                DATE_ADD('2010-01-01', INTERVAL FLOOR(RAND() * 3650) DAY), 
                IF(MOD(i, 2) = 0, 'Male', 'Female'), 
                CONCAT('MBTI', FLOOR(RAND() * 16) + 1), 
                i);
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

-- 좋아요 기록 5천개 더미 데이터 형성 프로시저
DELIMITER //
CREATE PROCEDURE InsertBookLikeDummyData()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 5000 DO
        INSERT INTO `kkul`.`book_like` 
        (`created_at`, `updated_at`, `is_like`, `book_idx`, `child_idx`)
        VALUES 
        (NOW(), NOW(), 
        IF(RAND() > 0.5, 1, 0),               -- is_like를 1 또는 0으로 랜덤 지정
         FLOOR(RAND() * 10000) + 1,            -- book_idx는 1부터 10000까지 랜덤
         FLOOR(RAND() * 10000) + 1);           -- child_idx는 1부터 10000까지 랜덤
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;


-- 각 프로시저 실행, 유저 만명 아이 만명 책 만개
CALL InsertUserDummyData();
CALL InsertBookMBTIDummyData();
CALL InsertBookDummyData();
CALL InsertChildMBTIDummyData();
CALL InsertChildDummyData();
CALL InsertBookLikeDummyData();






-- -- 유저 50명 아이 50명 책 50개 mbti 50개씩 SQL문

-- INSERT INTO book_mbti (mbti_e, mbti_s, mbti_t, mbti_j) VALUES
-- (60, 70, 80, 90),  -- ID 1
-- (50, 60, 70, 80),  -- ID 2
-- (80, 50, 60, 70),  -- ID 3
-- (70, 80, 90, 60),  -- ID 4
-- (60, 70, 80, 50),  -- ID 5
-- (90, 40, 50, 60),  -- ID 6
-- (70, 30, 40, 80),  -- ID 7
-- (50, 60, 80, 70),  -- ID 8
-- (40, 90, 60, 50),  -- ID 9
-- (80, 60, 70, 40),  -- ID 10
-- (45, 55, 65, 75),  -- ID 11
-- (70, 60, 50, 40),  -- ID 12
-- (30, 40, 50, 60),  -- ID 13
-- (55, 65, 75, 85),  -- ID 14
-- (65, 45, 35, 55),  -- ID 15
-- (40, 50, 60, 70),  -- ID 16
-- (75, 85, 65, 55),  -- ID 17
-- (60, 40, 50, 30),  -- ID 18
-- (55, 75, 85, 45),  -- ID 19
-- (35, 45, 55, 65),  -- ID 20
-- (70, 80, 60, 50),  -- ID 21
-- (50, 70, 40, 60),  -- ID 22
-- (80, 60, 70, 55),  -- ID 23
-- (60, 70, 50, 40),  -- ID 24
-- (45, 65, 85, 55),  -- ID 25
-- (35, 55, 45, 75),  -- ID 26
-- (50, 60, 40, 30),  -- ID 27
-- (75, 55, 65, 45),  -- ID 28
-- (40, 50, 60, 80),  -- ID 29
-- (55, 65, 75, 85),  -- ID 30
-- (70, 80, 90, 60),  -- ID 31
-- (60, 40, 50, 30),  -- ID 32
-- (45, 55, 35, 75),  -- ID 33
-- (35, 65, 55, 85),  -- ID 34
-- (65, 45, 75, 55),  -- ID 35
-- (50, 70, 60, 40),  -- ID 36
-- (75, 85, 55, 65),  -- ID 37
-- (40, 50, 70, 60),  -- ID 38
-- (55, 35, 75, 65),  -- ID 39
-- (30, 40, 60, 50),  -- ID 40
-- (70, 60, 50, 80),  -- ID 41
-- (45, 55, 75, 65),  -- ID 42
-- (65, 75, 55, 35),  -- ID 43
-- (80, 70, 60, 50),  -- ID 44
-- (60, 40, 50, 70),  -- ID 45
-- (55, 65, 45, 35),  -- ID 46
-- (50, 60, 40, 70),  -- ID 47
-- (75, 85, 55, 65),  -- ID 48
-- (35, 55, 45, 65),  -- ID 49
-- (70, 50, 60, 80);  -- ID 50



-- INSERT INTO book (book_title, book_author, book_publisher, book_summary, book_content, book_mbti_id) VALUES
-- ('The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', 'A story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.', 'Gatsby believed in the green light, the orgastic future that year by year recedes before us.', 1),
-- ('To Kill a Mockingbird', 'Harper Lee', 'J.B. Lippincott & Co.', 'A novel about the serious issues of rape and racial inequality.', 'It’s never an insult to be called what somebody thinks is a bad name. It just shows you how poor that person is, it doesn’t hurt you.', 2),
-- ('1984', 'George Orwell', 'Secker & Warburg', 'A dystopian social science fiction novel and cautionary tale about the dangers of totalitarianism.', 'Big Brother is watching you.', 3),
-- ('Pride and Prejudice', 'Jane Austen', 'T. Egerton', 'A romantic novel of manners that depicts the British landed gentry at the end of the 18th century.', 'It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.', 4),
-- ('The Catcher in the Rye', 'J.D. Salinger', 'Little, Brown and Company', 'A story about a young boy’s experiences in New York City after being expelled from prep school.', 'People always think something’s all true.', 5),
-- ('The Hobbit', 'J.R.R. Tolkien', 'George Allen & Unwin', 'A fantasy novel that follows the adventures of Bilbo Baggins, a hobbit who embarks on a quest to help dwarves reclaim their mountain home.', 'In a hole in the ground there lived a hobbit.', 6),
-- ('Fahrenheit 451', 'Ray Bradbury', 'Ballantine Books', 'A dystopian novel that presents a future where books are outlawed and "firemen" burn any that are found.', 'It was a pleasure to burn.', 7),
-- ('Brave New World', 'Aldous Huxley', 'Chatto & Windus', 'A dystopian novel set in a technologically advanced future where humans are genetically engineered and conditioned for their roles in society.', 'Words can be like X-rays if you use them properly.', 8),
-- ('Moby Dick', 'Herman Melville', 'Harper & Brothers', 'The narrative of Captain Ahab’s obsessive quest to kill Moby Dick, the giant white whale.', 'Call me Ishmael.', 9),
-- ('War and Peace', 'Leo Tolstoy', 'The Russian Messenger', 'A historical novel that chronicles the history of the French invasion of Russia and the impact of the Napoleonic era on Tsarist society.', 'Well, Prince, so Genoa and Lucca are now just family estates of the Buonaparte.', 10),
-- ('Pride and Prejudice', 'Jane Austen', 'T. Egerton', 'A romantic novel about the emotional development of Elizabeth Bennet.', 'It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.', 11),
-- ('1984', 'George Orwell', 'Secker & Warburg', 'A cautionary tale about totalitarianism.', 'Big Brother is watching you.', 12),
-- ('Moby Dick', 'Herman Melville', 'Harper & Brothers', 'The quest of Ahab for revenge on the white whale, Moby Dick.', 'Call me Ishmael.', 13),
-- ('War and Peace', 'Leo Tolstoy', 'The Russian Messenger', 'The history of the French invasion of Russia.', 'We can know only that we know nothing. And that is the highest degree of human wisdom.', 14),
-- ('The Odyssey', 'Homer', 'Ancient Greek Publisher', 'The epic journey of Odysseus after the Trojan War.', 'Tell me, O muse, of that ingenious hero who travelled far and wide.', 15),
-- ('Brave New World', 'Aldous Huxley', 'Chatto & Windus', 'A dystopian novel set in a futuristic society.', 'Everybody is happy now.', 16),
-- ('Crime and Punishment', 'Fyodor Dostoevsky', 'The Russian Messenger', 'The psychological torment of Raskolnikov.', 'To go wrong in one’s own way is better than to go right in someone else’s.', 17),
-- ('Great Expectations', 'Charles Dickens', 'Chapman & Hall', 'The growth and development of Pip.', 'Ask no questions, and you’ll be told no lies.', 18),
-- ('Jane Eyre', 'Charlotte Brontë', 'Smith, Elder & Co.', 'The emotional journey of orphan Jane Eyre.', 'I am no bird; and no net ensnares me: I am a free human being with an independent will.', 19),
-- ('Wuthering Heights', 'Emily Brontë', 'Thomas Cautley Newby', 'A tale of the intense and almost demonic love between Catherine and Heathcliff.', 'Whatever our souls are made of, his and mine are the same.', 20),
-- ('The Catcher in the Rye', 'J.D. Salinger', 'Little, Brown and Company', 'The story of teenage rebellion and angst.', 'I am always saying "Glad to’ve met you" to somebody I’m not glad I met.', 21),
-- ('The Hobbit', 'J.R.R. Tolkien', 'George Allen & Unwin', 'The adventure of Bilbo Baggins in Middle-earth.', 'In a hole in the ground there lived a hobbit.', 22),
-- ('Les Misérables', 'Victor Hugo', 'A. Lacroix, Verboeckhoven & Cie.', 'The story of Jean Valjean and his struggles for redemption.', 'Even the darkest night will end and the sun will rise.', 23),
-- ('The Count of Monte Cristo', 'Alexandre Dumas', 'Pétion', 'A story of justice, revenge, and mercy.', 'Wait and hope.', 24),
-- ('Anna Karenina', 'Leo Tolstoy', 'The Russian Messenger', 'A tragic love story set in Russian high society.', 'All happy families are alike; each unhappy family is unhappy in its own way.', 25),
-- ('One Hundred Years of Solitude', 'Gabriel García Márquez', 'Harper & Row', 'The multi-generational story of the Buendía family.', 'There is always something left to love.', 26),
-- ('The Divine Comedy', 'Dante Alighieri', 'Nicholas Jenson', 'Dante’s journey through Hell, Purgatory, and Paradise.', 'Midway upon the journey of our life, I found myself within a forest dark, For the straightforward path had been lost.', 27),
-- ('Don Quixote', 'Miguel de Cervantes', 'Francisco de Robles', 'The adventures of Don Quixote and his squire, Sancho Panza.', 'The truth may be stretched thin, but it never breaks, and it always surfaces above lies, as oil floats on water.', 28),
-- ('Madame Bovary', 'Gustave Flaubert', 'Revue de Paris', 'The story of a young woman’s pursuit of passion.', 'Human speech is like a cracked kettle on which we tap crude rhythms for bears to dance to, while we long to make music that will melt the stars.', 29),
-- ('The Iliad', 'Homer', 'Ancient Greek Publisher', 'The epic story of the Trojan War.', 'Sing, O goddess, the anger of Achilles son of Peleus, that brought countless ills upon the Achaeans.', 30),
-- ('The Picture of Dorian Gray', 'Oscar Wilde', 'Lippincott’s Monthly Magazine', 'A novel about vanity and the nature of art.', 'The only way to get rid of a temptation is to yield to it.', 31),
-- ('Fahrenheit 451', 'Ray Bradbury', 'Ballantine Books', 'A dystopian story where books are outlawed.', 'It was a pleasure to burn.', 32),
-- ('The Old Man and the Sea', 'Ernest Hemingway', 'Charles Scribner’s Sons', 'An old fisherman’s struggle with a giant marlin.', 'But man is not made for defeat... A man can be destroyed but not defeated.', 33),
-- ('The Brothers Karamazov', 'Fyodor Dostoevsky', 'The Russian Messenger', 'A story of faith, doubt, and morality.', 'I think the devil doesn’t exist, but man has created him, he has created him in his own image and likeness.', 34),
-- ('Dracula', 'Bram Stoker', 'Archibald Constable and Company', 'The horror story of Count Dracula’s attempt to move from Transylvania to England.', 'There are darknesses in life and there are lights, and you are one of the lights, the light of all lights.', 35),
-- ('Frankenstein', 'Mary Shelley', 'Lackington, Hughes, Harding, Mavor & Jones', 'The story of Victor Frankenstein and his creation.', 'Beware; for I am fearless, and therefore powerful.', 36),
-- ('The Scarlet Letter', 'Nathaniel Hawthorne', 'Ticknor, Reed & Fields', 'The story of Hester Prynne, who conceives a daughter through an affair.', 'We dream in our waking moments, and walk in our sleep.', 37),
-- ('The Grapes of Wrath', 'John Steinbeck', 'The Viking Press', 'The struggles of the Joad family during the Great Depression.', 'Wherever there’s a fight so hungry people can eat, I’ll be there.', 38),
-- ('The Stranger', 'Albert Camus', 'Gallimard', 'The story of Meursault, an indifferent French Algerian.', 'Mother died today. Or, maybe, yesterday; I can’t be sure.', 39),
-- ('Catch-22', 'Joseph Heller', 'Simon & Schuster', 'The satirical story of Yossarian, a World War II bombardier.', 'Just because you’re paranoid doesn’t mean they aren’t after you.', 40),
-- ('Ulysses', 'James Joyce', 'Shakespeare and Company', 'A day in the life of Leopold Bloom in Dublin.', 'History, Stephen said, is a nightmare from which I am trying to awake.', 41),
-- ('Heart of Darkness', 'Joseph Conrad', 'Blackwood’s Magazine', 'The story of Marlow’s journey into the African Congo.', 'The horror! The horror!', 42),
-- ('A Tale of Two Cities', 'Charles Dickens', 'Chapman & Hall', 'A story set in London and Paris before and during the French Revolution.', 'It was the best of times, it was the worst of times.', 43),
-- ('Lolita', 'Vladimir Nabokov', 'Olympia Press', 'A controversial story of obsession.', 'You can always count on a murderer for a fancy prose style.', 44),
-- ('Beloved', 'Toni Morrison', 'Alfred A. Knopf', 'The haunting story of Sethe, a former slave.', 'Definitions belong to the definers, not the defined.', 45),
-- ('Invisible Man', 'Ralph Ellison', 'Random House', 'A young Black man’s search for his identity.', 'I am invisible, understand, simply because people refuse to see me.', 46),
-- ('The Sound and the Fury', 'William Faulkner', 'Jonathan Cape and Harrison Smith', 'A story of the Compson family in the South.', 'I give you the mausoleum of all hope and desire.', 47),
-- ('Gone with the Wind', 'Margaret Mitchell', 'Macmillan Publishers', 'The story of Scarlett O’Hara during and after the Civil War.', 'After all, tomorrow is another day.', 48),
-- ('Slaughterhouse-Five', 'Kurt Vonnegut', 'Delacorte Press', 'Billy Pilgrim’s experience during World War II.', 'So it goes.', 49),
-- ('To the Lighthouse', 'Virginia Woolf', 'Hogarth Press', 'A novel about the Ramsay family’s experiences over a decade.', 'The very stone one kicks with one’s boot will outlast Shakespeare.', 50);

-- INSERT INTO user (created_at, updated_at, user_birth, user_email, user_gender, user_id, user_name, user_password, user_role)
-- VALUES
-- (NOW(), NOW(), '1980-01-15', 'parent1@example.com', 'Male', 'parent1', 'Parent1 Name', 'password1', 'USER'),
-- (NOW(), NOW(), '1981-02-10', 'parent2@example.com', 'Female', 'parent2', 'Parent2 Name', 'password2', 'USER'),
-- (NOW(), NOW(), '1982-03-05', 'parent3@example.com', 'Male', 'parent3', 'Parent3 Name', 'password3', 'USER'),
-- (NOW(), NOW(), '1983-04-20', 'parent4@example.com', 'Female', 'parent4', 'Parent4 Name', 'password4', 'USER'),
-- (NOW(), NOW(), '1984-05-12', 'parent5@example.com', 'Male', 'parent5', 'Parent5 Name', 'password5', 'USER'),
-- (NOW(), NOW(), '1985-06-25', 'parent6@example.com', 'Female', 'parent6', 'Parent6 Name', 'password6', 'USER'),
-- (NOW(), NOW(), '1986-07-30', 'parent7@example.com', 'Male', 'parent7', 'Parent7 Name', 'password7', 'USER'),
-- (NOW(), NOW(), '1987-08-14', 'parent8@example.com', 'Female', 'parent8', 'Parent8 Name', 'password8', 'USER'),
-- (NOW(), NOW(), '1988-09-19', 'parent9@example.com', 'Male', 'parent9', 'Parent9 Name', 'password9', 'USER'),
-- (NOW(), NOW(), '1989-10-03', 'parent10@example.com', 'Female', 'parent10', 'Parent10 Name', 'password10', 'USER'),
-- (NOW(), NOW(), '1990-11-08', 'parent11@example.com', 'Male', 'parent11', 'Parent11 Name', 'password11', 'USER'),
-- (NOW(), NOW(), '1991-12-23', 'parent12@example.com', 'Female', 'parent12', 'Parent12 Name', 'password12', 'USER'),
-- (NOW(), NOW(), '1980-01-07', 'parent13@example.com', 'Male', 'parent13', 'Parent13 Name', 'password13', 'USER'),
-- (NOW(), NOW(), '1981-02-12', 'parent14@example.com', 'Female', 'parent14', 'Parent14 Name', 'password14', 'USER'),
-- (NOW(), NOW(), '1982-03-28', 'parent15@example.com', 'Male', 'parent15', 'Parent15 Name', 'password15', 'USER'),
-- (NOW(), NOW(), '1983-04-15', 'parent16@example.com', 'Female', 'parent16', 'Parent16 Name', 'password16', 'USER'),
-- (NOW(), NOW(), '1984-05-09', 'parent17@example.com', 'Male', 'parent17', 'Parent17 Name', 'password17', 'USER'),
-- (NOW(), NOW(), '1985-06-17', 'parent18@example.com', 'Female', 'parent18', 'Parent18 Name', 'password18', 'USER'),
-- (NOW(), NOW(), '1986-07-24', 'parent19@example.com', 'Male', 'parent19', 'Parent19 Name', 'password19', 'USER'),
-- (NOW(), NOW(), '1987-08-19', 'parent20@example.com', 'Female', 'parent20', 'Parent20 Name', 'password20', 'USER'),
-- (NOW(), NOW(), '1988-09-25', 'parent21@example.com', 'Male', 'parent21', 'Parent21 Name', 'password21', 'USER'),
-- (NOW(), NOW(), '1989-10-29', 'parent22@example.com', 'Female', 'parent22', 'Parent22 Name', 'password22', 'USER'),
-- (NOW(), NOW(), '1990-11-11', 'parent23@example.com', 'Male', 'parent23', 'Parent23 Name', 'password23', 'USER'),
-- (NOW(), NOW(), '1991-12-05', 'parent24@example.com', 'Female', 'parent24', 'Parent24 Name', 'password24', 'USER'),
-- (NOW(), NOW(), '1980-01-20', 'parent25@example.com', 'Male', 'parent25', 'Parent25 Name', 'password25', 'USER'),
-- (NOW(), NOW(), '1981-02-16', 'parent26@example.com', 'Female', 'parent26', 'Parent26 Name', 'password26', 'USER'),
-- (NOW(), NOW(), '1982-03-22', 'parent27@example.com', 'Male', 'parent27', 'Parent27 Name', 'password27', 'USER'),
-- (NOW(), NOW(), '1983-04-11', 'parent28@example.com', 'Female', 'parent28', 'Parent28 Name', 'password28', 'USER'),
-- (NOW(), NOW(), '1984-05-19', 'parent29@example.com', 'Male', 'parent29', 'Parent29 Name', 'password29', 'USER'),
-- (NOW(), NOW(), '1985-06-22', 'parent30@example.com', 'Female', 'parent30', 'Parent30 Name', 'password30', 'USER'),
-- (NOW(), NOW(), '1986-07-03', 'parent31@example.com', 'Male', 'parent31', 'Parent31 Name', 'password31', 'USER'),
-- (NOW(), NOW(), '1987-08-12', 'parent32@example.com', 'Female', 'parent32', 'Parent32 Name', 'password32', 'USER'),
-- (NOW(), NOW(), '1988-09-07', 'parent33@example.com', 'Male', 'parent33', 'Parent33 Name', 'password33', 'USER'),
-- (NOW(), NOW(), '1989-10-15', 'parent34@example.com', 'Female', 'parent34', 'Parent34 Name', 'password34', 'USER'),
-- (NOW(), NOW(), '1990-11-19', 'parent35@example.com', 'Male', 'parent35', 'Parent35 Name', 'password35', 'USER'),
-- (NOW(), NOW(), '1991-12-29', 'parent36@example.com', 'Female', 'parent36', 'Parent36 Name', 'password36', 'USER'),
-- (NOW(), NOW(), '1980-01-17', 'parent37@example.com', 'Male', 'parent37', 'Parent37 Name', 'password37', 'USER'),
-- (NOW(), NOW(), '1981-02-09', 'parent38@example.com', 'Female', 'parent38', 'Parent38 Name', 'password38', 'USER'),
-- (NOW(), NOW(), '1982-03-03', 'parent39@example.com', 'Male', 'parent39', 'Parent39 Name', 'password39', 'USER'),
-- (NOW(), NOW(), '1983-04-07', 'parent40@example.com', 'Female', 'parent40', 'Parent40 Name', 'password40', 'USER'),
-- (NOW(), NOW(), '1984-05-24', 'parent41@example.com', 'Male', 'parent41', 'Parent41 Name', 'password41', 'USER'),
-- (NOW(), NOW(), '1985-06-10', 'parent42@example.com', 'Female', 'parent42', 'Parent42 Name', 'password42', 'USER'),
-- (NOW(), NOW(), '1986-07-13', 'parent43@example.com', 'Male', 'parent43', 'Parent43 Name', 'password43', 'USER'),
-- (NOW(), NOW(), '1987-08-26', 'parent44@example.com', 'Female', 'parent44', 'Parent44 Name', 'password44', 'USER'),
-- (NOW(), NOW(), '1988-09-15', 'parent45@example.com', 'Male', 'parent45', 'Parent45 Name', 'password45', 'USER'),
-- (NOW(), NOW(), '1989-10-12', 'parent46@example.com', 'Female', 'parent46', 'Parent46 Name', 'password46', 'USER'),
-- (NOW(), NOW(), '1990-11-03', 'parent47@example.com', 'Male', 'parent47', 'Parent47 Name', 'password47', 'USER'),
-- (NOW(), NOW(), '1991-12-18', 'parent48@example.com', 'Female', 'parent48', 'Parent48 Name', 'password48', 'USER'),
-- (NOW(), NOW(), '1980-01-26', 'parent49@example.com', 'Male', 'parent49', 'Parent49 Name', 'password49', 'USER'),
-- (NOW(), NOW(), '1981-02-22', 'parent50@example.com', 'Female', 'parent50', 'Parent50 Name', 'password50', 'USER');


-- INSERT INTO `child_mbti` 
-- (`mbti_e`, `mbti_j`, `mbti_s`, `mbti_t`, `child_idx`, `child_mbti_idx`, `created_at`, `updated_at`)
-- VALUES
-- (60, 55, 70, 80, 1, 1, NOW(), NOW()),
-- (65, 50, 75, 85, 2, 2, NOW(), NOW()),
-- (70, 60, 65, 90, 3, 3, NOW(), NOW()),
-- (55, 45, 80, 70, 4, 4, NOW(), NOW()),
-- (75, 70, 60, 75, 5, 5, NOW(), NOW()),
-- (80, 65, 55, 85, 6, 6, NOW(), NOW()),
-- (50, 75, 70, 60, 7, 7, NOW(), NOW()),
-- (85, 80, 65, 55, 8, 8, NOW(), NOW()),
-- (65, 55, 75, 65, 9, 9, NOW(), NOW()),
-- (70, 60, 80, 50, 10, 10, NOW(), NOW()),
-- (55, 65, 85, 70, 11, 11, NOW(), NOW()),
-- (60, 50, 75, 60, 12, 12, NOW(), NOW()),
-- (80, 70, 55, 85, 13, 13, NOW(), NOW()),
-- (75, 65, 80, 60, 14, 14, NOW(), NOW()),
-- (70, 55, 65, 75, 15, 15, NOW(), NOW()),
-- (65, 50, 85, 70, 16, 16, NOW(), NOW()),
-- (55, 75, 60, 65, 17, 17, NOW(), NOW()),
-- (80, 65, 70, 50, 18, 18, NOW(), NOW()),
-- (60, 55, 85, 75, 19, 19, NOW(), NOW()),
-- (65, 80, 55, 85, 20, 20, NOW(), NOW()),
-- (70, 75, 60, 70, 21, 21, NOW(), NOW()),
-- (85, 55, 80, 65, 22, 22, NOW(), NOW()),
-- (60, 65, 70, 85, 23, 23, NOW(), NOW()),
-- (75, 50, 60, 55, 24, 24, NOW(), NOW()),
-- (80, 70, 85, 65, 25, 25, NOW(), NOW()),
-- (55, 65, 75, 70, 26, 26, NOW(), NOW()),
-- (65, 80, 70, 85, 27, 27, NOW(), NOW()),
-- (75, 60, 55, 65, 28, 28, NOW(), NOW()),
-- (70, 50, 85, 55, 29, 29, NOW(), NOW()),
-- (60, 75, 80, 85, 30, 30, NOW(), NOW()),
-- (80, 65, 60, 70, 31, 31, NOW(), NOW()),
-- (65, 55, 75, 80, 32, 32, NOW(), NOW()),
-- (70, 85, 60, 75, 33, 33, NOW(), NOW()),
-- (75, 80, 55, 65, 34, 34, NOW(), NOW()),
-- (60, 70, 85, 50, 35, 35, NOW(), NOW()),
-- (55, 65, 70, 60, 36, 36, NOW(), NOW()),
-- (80, 75, 55, 85, 37, 37, NOW(), NOW()),
-- (70, 60, 80, 75, 38, 38, NOW(), NOW()),
-- (65, 55, 75, 65, 39, 39, NOW(), NOW()),
-- (75, 80, 60, 85, 40, 40, NOW(), NOW()),
-- (70, 65, 55, 75, 41, 41, NOW(), NOW()),
-- (60, 85, 80, 50, 42, 42, NOW(), NOW()),
-- (55, 75, 85, 60, 43, 43, NOW(), NOW()),
-- (80, 65, 70, 75, 44, 44, NOW(), NOW()),
-- (65, 60, 55, 70, 45, 45, NOW(), NOW()),
-- (75, 50, 80, 85, 46, 46, NOW(), NOW()),
-- (70, 55, 60, 65, 47, 47, NOW(), NOW()),
-- (60, 65, 85, 75, 48, 48, NOW(), NOW()),
-- (55, 75, 70, 60, 49, 49, NOW(), NOW()),
-- (80, 85, 55, 80, 50, 50, NOW(), NOW());

-- INSERT INTO child (child_name, child_age, child_birth, child_gender, child_mbti, parent_id)
-- VALUES 
-- ('Child1', 6, '2018-02-14', 'Male', 'ENTJ', 1),
-- ('Child2', 7, '2017-05-11', 'Female', 'INTP', 2),
-- ('Child3', 8, '2016-08-23', 'Male', 'ENFP', 3),
-- ('Child4', 5, '2019-12-03', 'Female', 'ISTJ', 4),
-- ('Child5', 6, '2018-07-12', 'Male', 'INFJ', 5),
-- ('Child6', 7, '2017-10-17', 'Female', 'ENTP', 6),
-- ('Child7', 8, '2016-03-25', 'Male', 'ISFJ', 7),
-- ('Child8', 6, '2018-06-19', 'Female', 'INTJ', 8),
-- ('Child9', 5, '2019-09-01', 'Male', 'ENFJ', 9),
-- ('Child10', 7, '2017-11-09', 'Female', 'ESTJ', 10),
-- ('Child11', 8, '2016-04-14', 'Male', 'ESFP', 11),
-- ('Child12', 6, '2018-05-06', 'Female', 'ISTP', 12),
-- ('Child13', 7, '2017-03-20', 'Male', 'INFJ', 13),
-- ('Child14', 8, '2016-12-22', 'Female', 'ESTP', 14),
-- ('Child15', 5, '2019-01-28', 'Male', 'ISFP', 15),
-- ('Child16', 6, '2018-10-10', 'Female', 'INFP', 16),
-- ('Child17', 7, '2017-06-15', 'Male', 'ENTJ', 17),
-- ('Child18', 8, '2016-02-17', 'Female', 'INTP', 18),
-- ('Child19', 6, '2018-07-27', 'Male', 'ENFP', 19),
-- ('Child20', 5, '2019-05-08', 'Female', 'ISTJ', 20),
-- ('Child21', 7, '2017-04-02', 'Male', 'INFJ', 21),
-- ('Child22', 8, '2016-09-13', 'Female', 'ENTP', 22),
-- ('Child23', 6, '2018-11-20', 'Male', 'ISFJ', 23),
-- ('Child24', 7, '2017-12-01', 'Female', 'INTJ', 24),
-- ('Child25', 5, '2019-08-29', 'Male', 'ENFJ', 25),
-- ('Child26', 8, '2016-05-14', 'Female', 'ESTJ', 26),
-- ('Child27', 6, '2018-03-03', 'Male', 'ESFP', 27),
-- ('Child28', 7, '2017-09-21', 'Female', 'ISTP', 28),
-- ('Child29', 8, '2016-01-11', 'Male', 'INFJ', 29),
-- ('Child30', 5, '2019-04-05', 'Female', 'ESTP', 30),
-- ('Child31', 6, '2018-09-09', 'Male', 'ISFP', 31),
-- ('Child32', 7, '2017-02-02', 'Female', 'INFP', 32),
-- ('Child33', 8, '2016-06-23', 'Male', 'ENTJ', 33),
-- ('Child34', 5, '2019-07-18', 'Female', 'INTP', 34),
-- ('Child35', 6, '2018-12-15', 'Male', 'ENFP', 35),
-- ('Child36', 7, '2017-01-07', 'Female', 'ISTJ', 36),
-- ('Child37', 8, '2016-03-15', 'Male', 'INFJ', 37),
-- ('Child38', 5, '2019-10-25', 'Female', 'ENTP', 38),
-- ('Child39', 6, '2018-04-17', 'Male', 'ISFJ', 39),
-- ('Child40', 7, '2017-08-13', 'Female', 'INTJ', 40),
-- ('Child41', 8, '2016-11-06', 'Male', 'ENFJ', 41),
-- ('Child42', 6, '2018-01-22', 'Female', 'ESTJ', 42),
-- ('Child43', 7, '2017-05-16', 'Male', 'ESFP', 43),
-- ('Child44', 8, '2016-07-30', 'Female', 'ISTP', 44),
-- ('Child45', 5, '2019-06-18', 'Male', 'INFJ', 45),
-- ('Child46', 6, '2018-08-07', 'Female', 'ESTP', 46),
-- ('Child47', 7, '2017-03-11', 'Male', 'ISFP', 47),
-- ('Child48', 8, '2016-12-27', 'Female', 'INFP', 48),
-- ('Child49', 6, '2018-02-03', 'Male', 'ENTJ', 49),
-- ('Child50', 7, '2017-11-30', 'Female', 'INTP', 50);

