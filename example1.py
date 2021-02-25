# coding: utf-8

"""
Ниже прилагается пример простой программы.

В каталоге находятся и загружаются 10 первых библиографических записей,
в которых автором является А. С. Пушкин. Показано нахождение
значения поля с заданным тегом и подполя с заданным кодом.

Также показано расформатирование записи в формат brief.
"""

import sys
from snakecat import connect, disconnect, read_record, hide_window, \
    IRBIS_CATALOG, error_to_string, search, fm, format_record

# Устанавливаем блокирующий режим сокета,
# чтобы не появлялось ненужное окно
hide_window()

# данные для подключения к серверу
HOST = '127.0.0.1'
PORT = '6666'
ARM = IRBIS_CATALOG
USER = 'librarian'
PASSWORD = 'secret'
DB = 'IBIS'

# Подключение к серверу
rc, ini = connect(HOST, PORT, ARM, USER, PASSWORD)
print('connect=', rc)
if rc < 0:
    print(error_to_string(rc))
    print('EXIT')
    sys.exit(1)

# Поиск записей
print()
_, found = search(DB, '"K=ПУШКИН$"')
print('Найдено записей:', len(found))

# Чтобы не распечатывать все найденные записи, отберем только 10 первых
for mfn in found[:10]:

    # Получаем запись из базы данных
    _, record = read_record(DB, mfn)
    title = fm(record, 200, 'a')
    print('Заглавие:', title)

    # Форматирование записи
    _c, description = format_record(DB, mfn, '@brief')
    print('Биб. описание:', description)

    print()  # Добавляем пустую строку

# Отключение от сервера
print()
rc = disconnect(USER)
print('IC_unreg=', rc)

print()
print('That''s All, Folks!')
