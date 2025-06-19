import sqlite3

DB_PATH = 'brainline.db'

def cleanup_materials():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Удалить материалы, у которых не существует темы
    cursor.execute("""
        DELETE FROM materials
        WHERE theme_id NOT IN (SELECT id FROM themes)
    """)
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    print(f"Удалено материалов без темы: {deleted}")

if __name__ == "__main__":
    cleanup_materials()