"""
1) Берём ссылку от пользователя (не проводим валидацию)
2) Удаляем из базы комбинаций последнее по ID значение, предварительно записав его в переменную
3) Кладём в базу ссылок ссылку пользователя и комбинацию из предыдущего пункта
4) Возвращаем юзеру строку вида http://malkiz.online/{combination}
"""

import sqlite3
import settings

# присоединяемся к базе со ссылками
connect_urls = sqlite3.connect(settings.DB_URLS_NAME)
cursor_urls = connect_urls.cursor()

# присоединяемся к базе с комбинациями
connect_combinations = sqlite3.connect(settings.DB_COMBINATIONS_NAME)
cursor_combinations = connect_combinations.cursor()


def take_combination_from_base() -> str:
    sql_last_id = """SELECT combination FROM """
    cursor_combinations.execute()
