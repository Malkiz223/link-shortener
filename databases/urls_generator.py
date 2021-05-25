import sqlite3
from itertools import product
from string import ascii_letters, digits

from settings import DB_COMBINATIONS_NAME


def main():
    """
    Генерируем все комбинации символов латинского алфавита upper и lowercase, всех цифр.
    Получившиеся комбинации кладём в set, чтобы зарандомить последовательность.
    Делаем список из set'а и кладём их в базу вида "id | комбинация".
    """
    # соединяемся с базой
    conn = sqlite3.connect(DB_COMBINATIONS_NAME)
    cursor = conn.cursor()

    # генерируем все комбинации указанных символов и добавляем их в список
    all_combinations_of_characters = set(product(ascii_letters + digits, repeat=4))
    list_of_combinations = list(''.join(elem) for elem in all_combinations_of_characters)

    # добавляем в базу все комбинации символов
    for combination in list_of_combinations:
        cursor.execute("""INSERT INTO combinations (short_combination)
            VALUES (?)""", (combination,))
    else:
        conn.commit()


if __name__ == '__main__':
    main()
