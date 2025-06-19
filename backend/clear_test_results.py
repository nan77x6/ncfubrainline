import sqlite3

DB_PATH = 'brainline.db'

def clear_test_results():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM test_results")
    conn.commit()
    conn.close()
    print("Таблица test_results успешно очищена.")

if __name__ == "__main__":
    clear_test_results()