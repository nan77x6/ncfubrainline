import sqlite3

DB_PATH = 'brainline.db'

def clear_user_links():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_subjects")
    cursor.execute("DELETE FROM user_classes")
    conn.commit()
    conn.close()
    print("Таблицы user_subjects и user_classes успешно очищены.")

if __name__ == "__main__":
    clear_user_links()