import sqlite3

# Данные пользователя
user_data = {
    "login": "admin",
    "password": "admin",
    "full_name": "Нерсесов Артур Николаевич",
    "role": "admin"  # может быть: 'student', 'teacher', 'admin'
}

# Подключение к базе данных
conn = sqlite3.connect('brainline.db')
cursor = conn.cursor()

try:
    cursor.execute("""
        INSERT INTO users (login, password, full_name, role)
        VALUES (?, ?, ?, ?)
    """, (
        user_data["login"],
        user_data["password"],
        user_data["full_name"],
        user_data["role"]
    ))
    conn.commit()
    print(f"Пользователь '{user_data['login']}' успешно добавлен.")
except sqlite3.IntegrityError as e:
    print("Ошибка при добавлении пользователя:", e)
finally:
    conn.close()
