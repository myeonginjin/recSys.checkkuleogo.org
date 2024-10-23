INSERT INTO book_mbti (mbti_e, mbti_s, mbti_t, mbti_j) VALUES
(60, 70, 80, 90),  -- ID 1
(50, 60, 70, 80),  -- ID 2
(80, 50, 60, 70),  -- ID 3
(70, 80, 90, 60),  -- ID 4
(60, 70, 80, 50),  -- ID 5
(90, 40, 50, 60),  -- ID 6
(70, 30, 40, 80),  -- ID 7
(50, 60, 80, 70),  -- ID 8
(40, 90, 60, 50),  -- ID 9
(80, 60, 70, 40);  -- ID 10

INSERT INTO book (book_title, book_author, book_publisher, book_summary, book_content, book_mbti_id) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', 'A story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.', 'Gatsby believed in the green light, the orgastic future that year by year recedes before us.', 1),
('To Kill a Mockingbird', 'Harper Lee', 'J.B. Lippincott & Co.', 'A novel about the serious issues of rape and racial inequality.', 'It’s never an insult to be called what somebody thinks is a bad name. It just shows you how poor that person is, it doesn’t hurt you.', 2),
('1984', 'George Orwell', 'Secker & Warburg', 'A dystopian social science fiction novel and cautionary tale about the dangers of totalitarianism.', 'Big Brother is watching you.', 3),
('Pride and Prejudice', 'Jane Austen', 'T. Egerton', 'A romantic novel of manners that depicts the British landed gentry at the end of the 18th century.', 'It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.', 4),
('The Catcher in the Rye', 'J.D. Salinger', 'Little, Brown and Company', 'A story about a young boy’s experiences in New York City after being expelled from prep school.', 'People always think something’s all true.', 5),
('The Hobbit', 'J.R.R. Tolkien', 'George Allen & Unwin', 'A fantasy novel that follows the adventures of Bilbo Baggins, a hobbit who embarks on a quest to help dwarves reclaim their mountain home.', 'In a hole in the ground there lived a hobbit.', 6),
('Fahrenheit 451', 'Ray Bradbury', 'Ballantine Books', 'A dystopian novel that presents a future where books are outlawed and "firemen" burn any that are found.', 'It was a pleasure to burn.', 7),
('Brave New World', 'Aldous Huxley', 'Chatto & Windus', 'A dystopian novel set in a technologically advanced future where humans are genetically engineered and conditioned for their roles in society.', 'Words can be like X-rays if you use them properly.', 8),
('Moby Dick', 'Herman Melville', 'Harper & Brothers', 'The narrative of Captain Ahab’s obsessive quest to kill Moby Dick, the giant white whale.', 'Call me Ishmael.', 9),
('War and Peace', 'Leo Tolstoy', 'The Russian Messenger', 'A historical novel that chronicles the history of the French invasion of Russia and the impact of the Napoleonic era on Tsarist society.', 'Well, Prince, so Genoa and Lucca are now just family estates of the Buonaparte.', 10);