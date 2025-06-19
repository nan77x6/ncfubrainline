import sqlite3

DB_PATH = 'brainline.db'

def clear_tests():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Удалить все варианты ответов
    cursor.execute("DELETE FROM test_options")
    # Удалить все пары для соответствий
    cursor.execute("DELETE FROM test_pairs")
    # Удалить все вопросы
    cursor.execute("DELETE FROM test_questions")
    # Удалить все тесты
    cursor.execute("DELETE FROM tests")
    conn.commit()
    conn.close()
    print("Все тесты, вопросы, варианты и пары удалены.")

if __name__ == "__main__":
    clear_tests()