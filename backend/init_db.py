import sqlite3
import os

DB_PATH = 'brainline.db'

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('student', 'teacher', 'admin'))
    )
    """)

    # Таблица классов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT UNIQUE NOT NULL
    )
    """)

    # Таблица принадлежности пользователей к классам
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        class_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(class_id) REFERENCES classes(id)
    )
    """)

    # Таблица предметов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_name TEXT UNIQUE NOT NULL
    )
    """)

    # Таблица кто ведёт какой предмет
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(subject_id) REFERENCES subjects(id)
    )
    """)

    # Таблица тем (themes)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS themes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            theme_name TEXT NOT NULL,
            subject_id INTEGER NOT NULL,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    """)

    # Таблица материалов (materials)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            markdown_content TEXT NOT NULL,
            theme_id INTEGER NOT NULL,
            created_by INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(theme_id) REFERENCES themes(id),
            FOREIGN KEY(created_by) REFERENCES users(id)
        )
    """)

    # Таблица тестов (привязка к материалу)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        material_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        FOREIGN KEY(material_id) REFERENCES materials(id)
    )
    """)

    # Таблица вопросов теста
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id INTEGER NOT NULL,
        question_text TEXT NOT NULL,
        question_type TEXT NOT NULL, -- single, multiple, match
        FOREIGN KEY(test_id) REFERENCES tests(id)
    )
    """)

    # Таблица вариантов ответа (для single/multiple)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_options (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL,
        option_text TEXT NOT NULL,
        is_correct INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(question_id) REFERENCES test_questions(id)
    )
    """)

    # Таблица пар для соответствия (match)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_pairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL,
        left_text TEXT NOT NULL,
        right_text TEXT NOT NULL,
        FOREIGN KEY(question_id) REFERENCES test_questions(id)
    )
    """)

    # Таблица результатов прохождения тестов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        test_id INTEGER NOT NULL,
        correct_answers INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        percent REAL NOT NULL,
        passed_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(test_id) REFERENCES tests(id)
    )
    """)

    # Таблица медиафайлов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        material_id INTEGER NOT NULL,
        url TEXT NOT NULL,
        type TEXT NOT NULL, -- image, video, etc
        public_id TEXT,      -- для Cloudinary
        uploaded_at TEXT NOT NULL,
        FOREIGN KEY(material_id) REFERENCES materials(id)
    )
    """)

    conn.commit()
    conn.close()

initialize_database()