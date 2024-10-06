import sqlite3

def add_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    product TEXT NOT NULL,
    description TEXT NOT NULL,
    cost INTEGER NOT NULL
    )
    ''')

    cursor.execute('INSERT INTO Products (product, description, cost) VALUES (?, ?, ?)',
               ('Зелье Здоровья', 'Чувствуете недомогание? Болезни одолевают? '
                                  'Утром продумываете, как сползти с кровати, чтоб не заклинило нигде? '
                                  'Наше "Зелье здоровья", выведенное лучшими алхимиками, вернёт Вам здоровье!'
                , '1'))

    cursor.execute('INSERT INTO Products (product, description, cost) VALUES (?, ?, ?)',
               ('Зелье Любви', 'Вас никто не любит? Девушки не улыбаются Вам, '
                               'и даже бабушки не хотят, чтобы Вы переводили их через дорогу? '
                               'Принимайте наше зелье внутриутробно и купайтесь в любви!'
                , '2'))

    cursor.execute('INSERT INTO Products (product, description, cost) VALUES (?, ?, ?)',
               ('Зелье Красоты', 'Вы антипод Апполлона или Афродиты, '
                                 'и из зеркала на Вас смотрит страшный мордоворот? '
                                 'Вами пугают непослушных детей? Наша новинка "Зелье Красоты" превратит Вас '
                                   'в самого красивого человека на свете! '
                , '3'))



    cursor.execute('INSERT INTO Products (product, description, cost) VALUES (?, ?, ?)',
               ('Чудо-зелье Мудрости', 'Валяли дурака в школе, а теперь не можете написать рекурсию в Python? '
                          'Не беда - наше "Чудо-зелье Мудрости" превратит Вас из ничтожного глупца в великого мудреца! '
                                       'Принимайте на растущую Луну!'
                , '4'))
    connection.commit()  # сохранение изменений
    connection.close()

def select_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT product, description, cost FROM Products')
    selected_products = cursor.fetchall()
    connection.close()
    return selected_products

def about_product(n):
     return (f'Название: Продукт {n+1} - {select_products()[n][0]} |\n'
             f'Описание: {select_products()[n][1]} |\n'
             f'Цена: {(select_products()[n][2])*100} золотых монет.')


def count_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM Products ')
    number_of_products = cursor.fetchone()[0]
    connection.close()
    return number_of_products

# add_products()