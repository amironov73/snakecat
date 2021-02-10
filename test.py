# coding: utf-8

"""
Простой тест работоспособности обёртки.
"""

import sys
from ctypes import create_string_buffer
from irbis import connect, disconnect, read_record, get_max_mfn, \
    hide_window, IRBIS_CATALOG, error_to_string, from_utf, \
    IC_nfields, IC_fieldn, IC_field, search, search_format, \
    format_record, print_form, get_deleted_records

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
    print('ERROR:', error_to_string(rc))
    print('EXIT')
    sys.exit(1)
else:
    print('connect.length=', len(ini))
    print('connect=', ini)

# Чтение записи
rc, record = read_record(DB, 1)
print('IC_read=', rc)
if rc < 0:
    print('IC_read=', error_to_string(rc))
else:
    print('IC_read=', from_utf(record.value))

# Получение количества полей
print()
rc = IC_nfields(record.value)
print('IC_nfields=', rc)

# Получение подполя v200^a
rc = IC_fieldn(record.value, 200, 1)
print('IC_fieldn', rc)
answer = create_string_buffer(32000)
rc = IC_field(record.value, rc, b'a', answer, len(answer))
print('IC_field=', rc)
if rc >= 0:
    print('IC_field=', from_utf(answer.value))

# Получение максимального MFN
rc = get_max_mfn(DB)
print('get_max_mfn=', rc)

# Поиск записей
print()
rc, mfns = search(DB, '"K=БЕТОН$"')
print('search=', rc)
if rc >= 0:
    print('search=', mfns[:10])
rc, lines = search_format(DB, '"K=БЕТОН"', 'v200^a')
print('search_format=', rc)
if rc >= 0:
    print('search_format=', lines[:10])

# Форматирование записи
print()
rc, line = format_record(DB, 1, '@brief')
print('format_record=', rc)
if rc >= 0:
    print('format_record=', line)

# Табличная форма
print()
rc, form = print_form(DB, '@tabf1w', 'ЗАГОЛОВОК ФОРМЫ', '',
                      '"T=ALGEBR$"', 0, 0, '', '')
print('print_form=', rc)
if rc >= 0:
    print('print_form=', form)

# Список удаленных записей
print()
rc, mfns = get_deleted_records(DB)
print('get_deleted_records=', rc)
if rc >= 0:
    print('get_deleted_records=', mfns)

# Отключение от сервера
print()
rc = disconnect(USER)
print('disconnect=', rc)

print()
print('That''s All, Folks!')
