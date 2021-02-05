# coding: utf-8

"""
Обертки для комфортной работы.
"""

from ctypes import create_string_buffer, c_char_p, cast, byref
from typing import TYPE_CHECKING
from irbis.constants import ANSI, UTF
from irbis.dllwrapper import IC_reg, IC_unreg, IC_read, IC_maxmfn, \
    IC_set_blocksocket
if TYPE_CHECKING:
    from typing import Optional, Tuple


def ansi_to_string(buffer: 'Optional[bytes]') -> str:
    """
    Превращаем буфер ctypes в обычную строку
    :param buffer: буфер
    :return: декодированная строка
    """
    if buffer:
        return buffer.rstrip(b'0').decode(ANSI)
    return ''


def utf_to_string(buffer: 'Optional[bytes]') -> str:
    """
    Превращаем буфер ctypes в обычную строку
    :param buffer: буфер
    :return: декодированная строка
    """
    if buffer:
        return buffer.rstrip(b'0').decode(UTF)
    return ''


def hide_window() -> None:
    """
    Прячем надоедливое окно, переходя в блокирующий режим сокетов.
    :return:
    """
    IC_set_blocksocket(1)


def connect(host: str, port: str, arm: str, user: str,
            password: str) -> 'Tuple[int, str]':
    """
    Подключение к серверу.
    :return: пару "код возврата-содержимое INI-файла"
    """
    answer_size = 32000
    buffer = create_string_buffer(answer_size)
    answer = cast(buffer, c_char_p)
    ret_code = IC_reg(host.encode(ANSI), port.encode(ANSI),
                      arm.encode(ANSI), user.encode(ANSI),
                      password.encode(ANSI), byref(answer),
                      answer_size)
    return ret_code, ansi_to_string(answer.value)


def disconnect(user: str) -> int:
    """
    Отключение от сервера.
    :return: код возврата
    """
    ret_code = IC_unreg(user.encode(ANSI))
    return ret_code


def get_max_mfn(database: str) -> int:
    """
    Получение следующего MFN для указанной базы
    :param database: имя базы данных
    :return: код возврата
    """
    ret_code = IC_maxmfn(database.encode(ANSI))
    return ret_code


def read_record(database: str, mfn: int) -> 'Tuple[int, str]':
    """
    Чтение записи с сервера
    :param database: имя базы данных
    :param mfn: MFN записи
    :return: пару "код возврата-запись"
    """
    answer_size = 32000
    buffer = create_string_buffer(answer_size)
    answer = cast(buffer, c_char_p)
    ret_code = IC_read(database.encode(ANSI), mfn, 0, byref(answer),
                       answer_size)
    return ret_code, utf_to_string(answer.value)
