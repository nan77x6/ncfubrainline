import sqlite3

# --- Добавление первого администратора ---

# Данные пользователя
login = "admin"
password = "admin"  # Пароль хранится в открытом виде (НЕ рекомендуется для продакшена)
full_name = "Администратор"
role = "admin"  # 'student', 'teacher' или 'admin'

conn = sqlite3.connect('brainline.db')
cursor = conn.cursor()

# Проверяем, есть ли уже такой пользователь
cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
if cursor.fetchone() is None:
    cursor.execute(
        "INSERT INTO users (login, password, full_name, role) VALUES (?, ?, ?, ?)",
        (login, password, full_name, role)
    )
    print(f"Пользователь {login} успешно создан.")
else:
    print(f"Пользователь {login} уже существует.")

conn.commit()
conn.close()