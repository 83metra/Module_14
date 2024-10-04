import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')


for i in range(1, 11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'User{i}', f'example{i}@gmail.com', f'{i}0', '1000',))
# connection.commit()

for i in range(1, 11, 2):
    cursor.execute('UPDATE Users SET balance = ? WHERE id = ?', (500, i))
# connection.commit()

for i in range(1, 11, 3):
    cursor.execute('DELETE FROM Users WHERE id = ?', (i,))
# connection.commit()

cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != ?', (60,))
selected_users = cursor.fetchall()
for user in selected_users:
    print('Имя: {0} | Почта: {1} | Возраст: {2} | Баланс {3}'.format(user[0], user[1], user[2], user[3]))

connection.commit()
connection.close()
