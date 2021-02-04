# coding: utf-8

"""
Простой тест работоспособности обёртки.
"""

import sys
from ctypes import c_char_p, create_string_buffer, byref, cast
from irbis import IC_set_blocksocket, IC_reg, IC_read, IC_unreg

answerSize: int = 32000
buffer = create_string_buffer(answerSize)
answer = cast(buffer, c_char_p)

# Устанавливаем блокирующий режим сокета,
# чтобы не появлялось ненужное окно
rc = IC_set_blocksocket(1)
print('IC_blocksocket=', rc)

HOST = b'127.0.0.1'
PORT = b'6666'
ARM = b'C'
USER = b'librarian'
PASSWORD = b'secret'
DB = b'IBIS'

# Подключение к серверу
rc = IC_reg(HOST, PORT, ARM, USER, PASSWORD, byref(answer), answerSize)
print('IC_reg=', rc)
if rc < 0:
    print('EXIT')
    sys.exit()
else:
    print('IC_reg=', answer.value)


# Чтение записи
rc = IC_read(DB, 1, 0, byref(answer), answerSize)
print('IC_read=', rc)
if rc >= 0:
    print('IC_read=', answer.value)

# Отключение от сервера
print()
rc = IC_unreg(USER)
print('IC_unreg=', rc)

print()
print('That''s All, Folks!')
