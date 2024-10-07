import sqlite3

filename = 'products_14_4.db'
def initiate_db():
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description,
    price INTEGER NOT NULL
    )
    ''')

    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                   ('Зелье Здоровья', 'Чувствуете недомогание? Болезни одолевают? '
                                      'Утром продумываете, как сползти с кровати, чтоб не заклинило нигде? '
                                      'Наше "Зелье здоровья", выведенное лучшими алхимиками, вернёт Вам здоровье!'
                    , '100'))

    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                   ('Зелье Любви', 'Вас никто не любит? Девушки не улыбаются Вам, '
                                   'и даже бабушки не хотят, чтобы Вы переводили их через дорогу? '
                                   'Принимайте наше зелье внутриутробно и купайтесь в любви!'
                    , '200'))

    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                   ('Зелье Красоты', 'Вы антипод Апполлона или Афродиты, '
                                     'и из зеркала на Вас смотрит страшный мордоворот? '
                                     'Вами пугают непослушных детей? '
                                     'Наша новинка "Зелье Красоты" превратит Вас '
                                     'в самого красивого человека на свете! '
                    , '300'))

    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                   ('Чудо-зелье Мудрости', 'Валяли дурака в школе, '
                                           'а теперь не можете написать рекурсию в Python? '
                                           'Не беда - наше "Чудо-зелье Мудрости" превратит '
                                           'Вас из ничтожного глупца в великого мудреца! '
                                           'Принимайте на растущую Луну внутриутробно '
                                           'и втирайте в темечко!'
                    , '400'))

    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                   ('Зелье Силы', 'Нет сил поднять даже чайник с плиты? '
                                  'Тощий тщедушный задохлик? '
                                  'Не в состоянии даже идти против ветра? '
                                  'Испейте наше инновационное "Зелье силы",'
                                  'только оно превратит Вас в сильнейшего силача мира!'
                                  'Принимать внутриутробно.'
                    , '500'))

    connection.commit()  # сохранение изменений
    connection.close()


def get_all_products():
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('SELECT title, description, price FROM Products')
    selected_products = cursor.fetchall()
    connection.close()
    return selected_products

def count_products():
    '''
    Функция подсчитывает количество строк в базе данных.
    Возвращает число.
    :return:
    '''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM Products ')
    number_of_products = cursor.fetchone()[0]
    connection.close()
    return number_of_products