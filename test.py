# coding: utf-8

"""
Простой тест работоспособности обёртки.
"""

import sys
from ctypes import create_string_buffer, cast, c_char_p
from irbis import connect, disconnect, read_record, get_max_mfn, \
    hide_window, IRBIS_CATALOG, error_to_string, from_utf, \
    IC_nfields, IC_fieldn, IC_field, search, search_format, \
    format_record, print_form, read_terms, trim_prefix, read_file, \
    create_record, add_field, write_record, IC_getmfn

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
max_mfn = get_max_mfn(DB)
print('get_max_mfn=', max_mfn)

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

# Список терминов словаря
print()
rc, terms = read_terms(DB, 'K=БЕТОН')
print('read_terms=', rc)
if rc >= 0:
    print('read_terms', trim_prefix(terms, 'K='))

# # Список удаленных записей
# print()
# rc, mfns = get_deleted_records(DB)
# print('get_deleted_records=', rc)
# if rc >= 0:
#     print('get_deleted_records=', mfns)

# Чтение файлов с сервера
print()
rc, content = read_file(DB, 'yesno.mnu')
print('read_file=', rc)
if rc >= 0:
    print('read_file=', content)

# # Запись файла на сервер
# print()
# rc = write_file(DB, 'not_exist.txt',
#                 'Это тестовый файл\r\nНичего интересного в нем нет')
# print()
# print('write_file=', rc)

# Создание записи
print()
record = create_string_buffer(32768)
rc = create_record(record)
print('create_record=', rc)
if rc >= 0:
    print('create_record=', from_utf(record.value))
    ptr = cast(record, c_char_p)
    add_field(record, 200, '^aАвтор^eПодзаголовочные^fОтветственность')
    add_field(record, 300, 'Какой-то комментарий')
    rc = add_field(record, 920, 'PAZK')
    print('add_field=', rc)
    if rc >= 0:
        print('add_field=', from_utf(record.value))
        mfn = IC_getmfn(ptr)
        print('IC_getmfn=', mfn)
        print(from_utf(record.value))
        rc = write_record(DB, record)
        print('write_record=', rc)
        if rc >= 0:
            print('write_record=', from_utf(record.value))

# _, record = read_record(DB, 1)
# add_field(record, 300, 'Эта запись модифицирована из Python')
# rc = write_record(DB, record)
# print('write_record=', rc)

# Отключение от сервера
print()
rc = disconnect(USER)
print('disconnect=', rc)

print()
print('That''s All, Folks!')
