# coding: utf-8

"""
Разбираемся, что не так с IC_update
"""

import sys
from ctypes import create_string_buffer, cast, c_char_p, byref
from irbis import IC_set_blocksocket, IC_reg, IC_unreg, \
    IC_recdummy, IC_fldadd, IC_update, from_utf

# Устанавливаем блокирующий режим сокета,
# чтобы не появлялось ненужное окно
IC_set_blocksocket(1)

# данные для подключения к серверу
HOST = b'127.0.0.1'
PORT = b'6666'
ARM = b'C'
USER = b'librarian'
PASSWORD = b'secret'
DB = b'IBIS'
BIG_ENOUGH = 32768

# Подключение к серверу
ini_buffer = create_string_buffer(BIG_ENOUGH)
ptr = cast(ini_buffer, c_char_p)
rc = IC_reg(HOST, PORT, ARM, USER, PASSWORD,
            byref(ptr), len(ini_buffer))
if rc < 0:
    print('ERROR:', rc)
    print('EXIT')
    sys.exit(1)

print('Connected\n')

record_buffer = create_string_buffer(BIG_ENOUGH)
ptr = cast(record_buffer, c_char_p)
IC_recdummy(ptr, BIG_ENOUGH)
IC_fldadd(ptr, 700, 0, b'^aOther author', BIG_ENOUGH)
IC_fldadd(ptr, 200, 0, b'^aTitle^eSubtitle^fResponsibility', BIG_ENOUGH)
IC_fldadd(ptr, 300, 0, b'Some comment', BIG_ENOUGH)
IC_fldadd(ptr, 920, 0, b'PAZK', BIG_ENOUGH)
print(from_utf(record_buffer.value))
print()

rc = IC_update(DB, 0, 1, byref(ptr), BIG_ENOUGH)
print('IC_update=', rc)

IC_unreg(USER)
print('Disconnected')
