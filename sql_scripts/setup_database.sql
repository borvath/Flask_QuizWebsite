CREATE DATABASE IF NOT EXISTS quizmaker;
USE quizmaker;

CREATE TABLE IF NOT EXISTS user (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    type ENUM('teacher', 'student', 'admin') NOT NULL,
    PRIMARY KEY(id),
    UNIQUE INDEX username_UNIQUE (username ASC) VISIBLE
);

CREATE TABLE IF NOT EXISTS course (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    section INT NOT NULL,
    teacher_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT teacher_id FOREIGN KEY (teacher_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS quiz (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    author_id INT UNSIGNED NOT NULL,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE INDEX name_UNIQUE (name ASC) VISIBLE,
    CONSTRAINT author_id FOREIGN KEY (author_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS question (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    quiz_id INT UNSIGNED NOT NULL,
    content VARCHAR(500) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT quiz_id FOREIGN KEY (quiz_id) REFERENCES quiz(id)
);

CREATE TABLE IF NOT EXISTS answer (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    question_id INT UNSIGNED NOT NULL,
    content VARCHAR(500) NOT NULL,
    correct BOOLEAN NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT question_id FOREIGN KEY (question_id) REFERENCES question(id)
);

CREATE TABLE IF NOT EXISTS ratings (
    studentID INT UNSIGNED PRIMARY KEY,
    quizId INT UNSIGNED NOT NULL,
    studentRatings VARCHAR(250),
   amountOfStars INT UNSIGNED CHECK (amountOfStars >= 1 AND amountOfStars <= 5),
    CONSTRAINT quizId FOREIGN KEY (quizId) REFERENCES quiz(id)
    CONSTRAINT studentID FOREIGN KEY (studentID) REFERENCES user(id)
);