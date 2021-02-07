# coding: utf-8

"""
Обертки для комфортной работы.
"""

from ctypes import create_string_buffer, c_char_p, cast, byref
from typing import TYPE_CHECKING
from irbis.constants import ANSI, UTF, ERR_BUFSIZE
from irbis.dllwrapper import IC_reg, IC_unreg, IC_read, IC_maxmfn, \
    IC_set_blocksocket, IC_search, IC_sformat, IC_fieldn, IC_field
if TYPE_CHECKING:
    from typing import Optional, Tuple, List, Any


def error_to_string(ret_code: int) -> str:
    """
    Получение текстового сообщения об ошибке по ее коду.
    :param ret_code: код ошибки
    :return: текстовое сообщение об ошибке
    """
    if ret_code >= 0:
        return 'Нормальное завершение'

    error_dictionary = {
        -1: 'прервано пользователем или общая ошибка',
        -2: 'не завершена обработка предыдущего запроса',
        -3:  ' неизвестная ошибка',
        -4:  'выходной буфер мал',
        -140:  'заданный MFN вне пределов БД',
        -202:  'термин не существует',
        -203:  'последний термин',
        -204:  'первый термин',
        -300:  'монопольная блокировка БД',
        -602:  'запись заблокирована на ввод',
        -603:  'запись логически удалена',
        -608:  'при записи обнаружено несоответстивие версий',
        -605:  'запись физически удалена',
        -999:  'ошибка в формате',
        -1111:  'ошибка выполнения на сервере',
        -1112:  'несоответсвие полученной и реальной длины',
        -2222:  'ошибка протокола',
        -3333:  'незарегистрированный клиент',
        -3334:  'незарегистрированный клиент не сделал irbis-reg',
        -3335:  'неправильный уникальный идентификатор',
        -3336:  'зарегистрировано максимально допустимое число клиентов',
        -3337:  'клиент уже зарегистрирован',
        -3338:  'нет доступа к командам АРМа',
        -4444:  'неверный пароль',
        -5555:  'файл не существует',
        -6666:  'сервер перегружен',
        -7777:  'не удалось запустить/прервать поток',
        -8888:  'gbl обрушилась'
    }

    try:
        return error_dictionary[ret_code]
    except KeyError:
        return 'неизвестная ошибка'


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
    :param host: адрес хоста
    :param port: номер порта
    :param arm: код АРМ
    :param user: логин пользователя
    :param password: пароль
    :return: пара "код возврата-содержимое INI-файла"
    """
    answer_size = 32768
    while True:
        buffer = create_string_buffer(answer_size)
        answer = cast(buffer, c_char_p)
        ret_code = IC_reg(host.encode(ANSI), port.encode(ANSI),
                          arm.encode(ANSI), user.encode(ANSI),
                          password.encode(ANSI), byref(answer),
                          answer_size)
        if ret_code == ERR_BUFSIZE:
            # на всякий случай разрегистриемся
            IC_unreg(user.encode(ANSI))
            # повторим попытку с увеличенным буфером
            answer_size *= 2
        else:
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


def read_record(database: str, mfn: int) -> 'Tuple[int, c_char_p]':
    """
    Чтение записи с сервера.
    :param database: имя базы данных
    :param mfn: MFN записи
    :return: пара "код возврата-запись"
    """
    answer_size = 32768
    while True:
        buffer = create_string_buffer(answer_size)
        answer = cast(buffer, c_char_p)
        ret_code = IC_read(database.encode(ANSI), mfn, 0, byref(answer),
                           answer_size)
        if ret_code == ERR_BUFSIZE:
            answer_size *= 2
        else:
            return ret_code, answer


def search(database: str, expression: str) -> 'Tuple[int, List[int]]':
    """
    Прямой поиск по словарю
    :param database: имя базы данных
    :param expression: поисковое выражение
    :return: пара "код возврата-найденные MFN"
    """
    answer_size = 32768
    while True:
        buffer = create_string_buffer(answer_size)
        answer = cast(buffer, c_char_p)
        ret_code = IC_search(database.encode(ANSI),
                             expression.encode(UTF), 32768, 1,
                             b'', answer, answer_size)
        if ret_code == ERR_BUFSIZE:
            answer_size *= 2
        else:
            lines = utf_to_string(answer.value).split('#\r\n')
            result = [int(line) for line in lines if line]
            return ret_code, result


def search_format(database: str, expression: str, format_spec: str) \
        -> 'Tuple[int, List[str]]':
    """
    Прямой поиск по словарю с расформатированием
    :param database: имя базы данных
    :param expression: поисковое выражение
    :param format_spec: специфификация формата
    :return: пара "код возврата-расформатированные записи"
    """
    answer_size = 32768
    while True:
        buffer = create_string_buffer(answer_size)
        answer = cast(buffer, c_char_p)
        ret_code = IC_search(database.encode(ANSI),
                             expression.encode(UTF), 32768, 1,
                             format_spec.encode(UTF),
                             answer, answer_size)
        if ret_code == ERR_BUFSIZE:
            answer_size *= 2
        else:
            lines = utf_to_string(answer.value).split('\r\n')
            return ret_code, lines


def format_record(database: str, mfn: int, format_spec: str) \
        -> 'Tuple[int, str]':
    """
    Расформатирование записи по ее MFN.
    :param database: имя базы данных
    :param mfn: MFN записи
    :param format_spec: спецификация формата
    :return: пара "код возврата-расформатированная запись"
    """
    answer_size = 32768
    while True:
        buffer = create_string_buffer(answer_size)
        answer = cast(buffer, c_char_p)
        ret_code = IC_sformat(database.encode(ANSI),
                              mfn, format_spec.encode(UTF),
                              answer, answer_size)
        if ret_code == ERR_BUFSIZE:
            answer_size *= 2
        else:
            lines = utf_to_string(answer.value).split('\r\n')
            return ret_code, lines[1]


def fm(record: 'Any', tag: int, subfield: str = '') -> str:
    """
    Извлечение значения поля или подполя с указанной меткой.
    :param record: запись
    :param tag: метка поля
    :param subfield: разделитель подполя (опционально)
    :return: значение поля или подполя
    """
    index = IC_fieldn(record.value, tag, 1)
    if index < 0:
        return ''
    answer_size = 32768
    while True:
        answer = create_string_buffer(answer_size)
        IC_field(record.value, index, subfield.encode(ANSI),
                 answer, answer_size)
        return utf_to_string(answer.value)
