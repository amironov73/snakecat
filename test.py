# coding: utf-8

"""
Простой тест работоспособности обёртки.
"""

import sys
from irbis import connect, disconnect, read_record, get_max_mfn, \
    hide_window, IRBIS_CATALOG

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
    print('EXIT')
    sys.exit(1)
else:
    print('connect=', ini)

# Чтение записи
rc, record = read_record(DB, 1)
print('IC_read=', rc)
if rc >= 0:
    print('IC_read=', record)

# Получение максимального MFN
rc = get_max_mfn(DB)
print('IC_maxmfn=', rc)

# Отключение от сервера
print()
rc = disconnect(USER)
print('IC_unreg=', rc)

print()
print('That''s All, Folks!')
