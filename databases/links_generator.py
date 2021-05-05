"""
Генерируем все комбинации символов латинского алфавита upper и lowercase, всех цифр.
Получившиеся комбинации кладём в set, чтобы зарандомить последовательность.
Делаем список из set'а и кладём их в базу вида "id | комбинация"

Делаем другой модуль, которым будем доставать из базы строку с максимальным id и комбинацией в переменные,
Затем удалять строку с данным id из базы комбинаций, и добавлять строку в базу вида "пришедший id|отправляемый юзеру id"
"""
import time
from itertools import product
import sqlite3
import string
import settings

# соединяемся с базой
conn = sqlite3.connect(settings.DB_COMBINATIONS_NAME)
cursor = conn.cursor()


# генерируем все комбинации указанных символов и добавляем их в список
all_combinations_of_characters = set(product(string.ascii_letters + string.digits, repeat=4))
list_of_combinations = list(''.join(elem) for elem in all_combinations_of_characters)

# добавляем в базу все комбинации символов
start_time = time.time()
for combination in list_of_combinations:
    cursor.execute("""INSERT INTO combinations (short_combination)
        VALUES (?)""", (combination,))
else:
    conn.commit()

print('Весь скрипт выполнен за', time.time() - start_time)
