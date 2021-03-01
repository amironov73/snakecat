# coding: utf-8

"""
Обертки для комфортной работы.
"""

from ctypes import create_string_buffer, c_char_p, cast, byref
from typing import TYPE_CHECKING
from snakecat.constants import ANSI, UTF, ERR_BUFSIZE, TERM_NOT_EXISTS, \
    TERM_FIRST_IN_LIST, TERM_LAST_IN_LIST, DBNPATH2, ERR_UNKNOWN
from snakecat.dllwrapper import IC_reg, IC_unreg, IC_read, IC_maxmfn, \
    IC_set_blocksocket, IC_search, IC_sformat, IC_fieldn, IC_field, \
    IC_print, IC_adm_getdeletedlist, IC_reset_delim, IC_delim_reset, \
    IC_nexttrm, IC_prevtrm, IC_getresourse, IC_clearresourse, \
    IC_putresourse, IC_runlock, IC_ifupdate, IC_recdummy, IC_fldadd, \
    IC_update, IC_fldrep, IC_fldempty, IC_recdel, IC_recundel, \
    IC_recunlock, IC_isactualized, IC_islocked, IC_isdeleted, \
    IC_isbusy, IC_set_webserver, IC_set_webcgi
if TYPE_CHECKING:
    from typing import Optional, Tuple, List
    from ctypes import Array, c_char


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


def from_ansi(buffer: 'Optional[bytes]') -> str:
    """
    Превращаем буфер ctypes в обычную строку.
    :param buffer: буфер
    :return: декодированная строка
    """
    if buffer:
        return buffer.rstrip(b'0').decode(ANSI)
    return ''


def from_utf(buffer: 'Optional[bytes]') -> str:
    """
    Превращаем буфер ctypes в обычную строку.
    :param buffer: буфер
    :return: декодированная строка
    """
    if buffer:
        return buffer.rstrip(b'0').decode(UTF)
    return ''


def to_ansi(text: 'Optional[str]') -> bytes:
    """
    Конвертируем строку в байты в кодировке ANSI.
    :param text: текст для конверсии
    :return: ANSI-байты
    """
    if not text:
        return b''
    return text.encode(ANSI)


def to_utf(text: 'Optional[str]') -> bytes:
    """
    Конвертируем строку в байты в кодировке UTF-8.
    :param text: текст для конверсии
    :return: UTF-байты
    """
    if not text:
        return b''
    return text.encode(UTF)


def to_irbis(text: bytes) -> bytes:
    """
    Заменяем разделители строк на псевдоразделители.
    :param text: текст для обработки
    :return: обработанный текст
    """
    return IC_reset_delim(text)


def from_irbis(text: bytes) -> bytes:
    """
    Заменяем псевдоразделители строк на настоящие разделители.
    :param text: текст для обработки
    :return: обработанный текст
    """
    return IC_delim_reset(text)


def hide_window() -> None:
    """
    Прячем надоедливое окно, переходя в блокирующий режим сокетов.
    :return:
    """
    IC_set_blocksocket(1)


def use_web_gateway(cgi: 'Optional[str]' = None) -> int:
    """
    Установка режима работы через Web-шлюз.
    :param cgi: путь к шлюзу (по умолчанию ``/cgi-bin/wwwirbis.exe``)
    :return: код возврата
    """
    ret_code = IC_set_webserver(1)
    if ret_code < 0:
        return ret_code
    if cgi:
        ret_code = IC_set_webcgi(to_ansi(cgi))
    return ret_code


def connect(host: str, port: str, arm: str, user: str,
            password: str) -> 'Tuple[int, str]':
    """
    Подключение к серверу -- регистрация клиента на сервере.
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
        ret_code = IC_reg(to_ansi(host), to_ansi(port), to_ansi(arm),
                          to_ansi(user), to_ansi(password),
                          byref(answer), answer_size)
        if ret_code == ERR_BUFSIZE:
            # на всякий случай разрегистриемся
            IC_unreg(user.encode(ANSI))
            # повторим попытку с увеличенным буфером
            answer_size *= 2
        else:
            return ret_code, from_ansi(answer.value)


def disconnect(user: str) -> int:
    """
    Отключение от сервера - разрегистрация клиента на сервере,
    сигнал об окончании работы.
    :return: код возврата
    """
    ret_code = IC_unreg(to_ansi(user))
    return ret_code


def is_busy() -> bool:
    """
    Определение, не занят ли в данный момент сервер обработкой запроса
    от данного клиента.
    :return: `true` если занят
    """
    return IC_isbusy() == 1


def get_max_mfn(database: str) -> int:
    """
    Получение следующего MFN для указанной базы
    :param database: имя базы данных
    :return: код возврата
    """
    ret_code = IC_maxmfn(to_ansi(database))
    return ret_code


def read_record(database: str, mfn: int) -> 'Tuple[int, Array[c_char]]':
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
        ret_code = IC_read(to_ansi(database), mfn, 0, byref(answer),
                           answer_size)
        if ret_code == ERR_BUFSIZE:
            answer_size *= 2
        else:
            return ret_code, buffer


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
        ret_code = IC_search(to_ansi(database), to_utf(expression),
                             32768, 1, b'', answer, answer_size)
        if ret_code == ERR_BUFSIZE:
            answer_size *= 2
        else:
            lines = from_utf(answer.value).split('#\r\n')
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
        ret_code = IC_search(to_ansi(database), to_utf(expression),
                             32768, 1, to_utf(format_spec), answer,
                             answer_size)
        if ret_code == ERR_BUFSIZE:
            answer_size *= 2
        else:
            lines = from_utf(answer.value).split('\r\n')
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
        ret_code = IC_sformat(to_ansi(database), mfn, to_utf(format_spec),
                              answer, answer_size)
        if ret_code == ERR_BUFSIZE:
            answer_size *= 2
        else:
            lines = from_utf(answer.value).split('\r\n')
            return ret_code, lines[1]


def print_form(database: str, table: str, head: str, model: str,
               search_expression: str, min_mfn: int, max_mfn: int,
               sequential: str, mfn_list: str) -> 'Tuple[int, str]':
    """
    Формирование выходной табличной формы.
    :param database: имя базы данных
    :param table: имя табличной формы с предшествующим '@'
    :param head: заголовки над таблицей (до 3 строк)
    :param model: значение модельного поля
    :param search_expression: поисковое выражение
    :param min_mfn: минимальный MFN
    :param max_mfn: максимальный MFN
    :param sequential: выражение для последовательного поиска
    :param mfn_list: список MFN записей
    :return: пара "код возврата-сформированная форма"
    """
    answer_size = 524288
    while True:
        buffer = create_string_buffer(answer_size)
        answer = cast(buffer, c_char_p)
        ret_code = IC_print(to_ansi(database), to_ansi(table), to_utf(head),
                            to_ansi(model), to_utf(search_expression), min_mfn,
                            max_mfn, to_utf(sequential), to_ansi(mfn_list),
                            answer, answer_size)
        if ret_code == ERR_BUFSIZE:
            answer_size *= 2
        else:
            result = from_utf(answer.value)
            return ret_code, result


def get_deleted_records(database: str) -> 'Tuple[int, List[int]]':
    """
    Получение списка удаленных записей.
    :param database: имя базы данных
    :return: пара "код возврата-список MFN удаленных записей"
    """
    answer_size = 32768
    while True:
        buffer = create_string_buffer(answer_size)
        answer = cast(buffer, c_char_p)
        ret_code = IC_adm_getdeletedlist(to_ansi(database), answer,
                                         answer_size)
        if ret_code == ERR_BUFSIZE:
            answer_size *= 2
        else:
            if ret_code < 0:
                return ret_code, []

            lines = from_utf(answer.value).split('\r\n')
            result = [int(line.split('#', 1)[1]) for line in lines if line]
            return ret_code, result


def fm(record: 'Array[c_char]', tag: int, subfield: str = '',
       repeat: int = 1) -> str:
    """
    Извлечение значения поля или подполя с указанной меткой.
    :param record: запись
    :param tag: метка поля
    :param subfield: разделитель подполя (опционально)
    :param repeat: номер повторения поля, отсчет с 1 (по умолчанию 1)
    :return: значение поля или подполя
    """
    ptr = cast(record, c_char_p)
    index = IC_fieldn(ptr, tag, repeat)
    if index < 0:
        return ''
    answer_size = 32768
    while True:
        answer = create_string_buffer(answer_size)
        IC_field(ptr, index, to_ansi(subfield), answer, answer_size)
        return from_utf(answer.value)


def read_terms(database: str, first_term: str, term_count: int = 100,
               reverse: bool = False) -> 'Tuple[int, List[Tuple[str, int]]]':
    """
    Чтение терминов словаря, начиная с указанного.
    :param database: имя базы данных
    :param first_term: первый термин
    :param term_count: необходимое количество терминов
    :param reverse: в обратном порядке?
    :return: кортеж "код возврата-список кортежей
    'термин-количество ссылок на него'"
    """
    function = IC_prevtrm if reverse else IC_nexttrm
    answer_size = 32768
    while True:
        answer = create_string_buffer(answer_size)
        ret_code = function(to_ansi(database), to_utf(first_term), term_count,
                            answer, answer_size)
        if ret_code == ERR_BUFSIZE:
            answer_size *= 2
        else:
            good_codes = [TERM_NOT_EXISTS, TERM_FIRST_IN_LIST,
                          TERM_LAST_IN_LIST]
            if ret_code < 0 and ret_code not in good_codes:
                return ret_code, []

            if ret_code in good_codes:
                ret_code = 0
            lines = from_utf(answer.value).split('\r\n')
            parts = [line.split('#', 1) for line in lines if line]
            result = [(part[1], int(part[0])) for part in parts
                      if parts[1]]
            return ret_code, result


def trim_prefix(terms: 'List[Tuple[str, int]]', prefix: str) -> \
                'List[Tuple[str, int]]':
    """
    Удаляет указанный префикс у всех терминов в списке.
    :param terms: термины, подлежащие обработке
    :param prefix: префикс для удаления
    :return: список кортежей "термин-количество ссылок на него"
    """
    prefix_length = len(prefix)
    result = [(term[0][prefix_length:], term[1]) for term in terms]
    return result


def read_file(database: 'Optional[str]', file_name: str,
              path: int = DBNPATH2) -> 'Tuple[int, str]':
    """
    Чтение текстового файла с сервера.
    :param database: имя базы данных (не используется для кодов
    SYSPATH и DATAPATH)
    :param file_name: имя файла
    :param path: код пути
    :return: код возврата и содержимое файла (пустая строка,
    если такого файла нет)
    """
    answer_size = 32768
    while True:
        buffer = create_string_buffer(answer_size)
        answer = cast(buffer, c_char_p)
        ret_code = IC_getresourse(path, to_ansi(database),
                                  to_ansi(file_name), byref(answer),
                                  answer_size)
        if ret_code == ERR_BUFSIZE:
            answer_size *= 2
        else:
            if ret_code < 0:
                return ret_code, ''
            return ret_code, from_ansi(answer.value)


def clear_cache() -> int:
    """
    Очистка локального кэша форматов, меню и прочих ресурсов,
    прочитанных с сервера.
    :return: код возврата
    """
    return IC_clearresourse()


def write_file(database: 'Optional[str]', file_name: str, content: str,
               path: int = DBNPATH2) -> int:
    """
    Запись текстового файла на сервер.
    :param database: имя базы данных
    :param file_name: имя файла
    :param content: содержимое файла
    :param path: код пути
    :return: код возврата
    """
    return IC_putresourse(path, to_ansi(database), to_ansi(file_name),
                          to_irbis(to_ansi(content)))


def unlock_record(database: str, mfn: int) -> int:
    """
    Разблокирование указанной записи.
    :param database: имя базы данных
    :param mfn: MFN записи
    :return: код возврата
    """
    return IC_runlock(to_ansi(database), mfn)


def actualize_record(database: str, mfn: int) -> int:
    """
    Актуализация указанной записи.
    :param database: имя базы данных
    :param mfn: MFN записи
    :return: код возврата
    """
    return IC_ifupdate(to_ansi(database), mfn)


def actualize_database(database: str) -> int:
    """
    Актуализация всех неактуализированных записей в указанной базе данных.
    :param database: имя базы данных
    :return: код возврата
    """
    return IC_ifupdate(to_ansi(database), 0)


def create_record(record: 'Array[c_char]') -> int:
    """
    Создание пустой записи.
    :param record: буфер для создаваемой записи
    :return: код возврата
    """
    ptr = cast(record, c_char_p)
    return IC_recdummy(ptr, len(record))


def add_field(record: 'Array[c_char]', tag: int, field: str) -> int:
    """
    Добавление поля в конец записи.
    :param record: запись
    :param tag: метка поля
    :param field: текст добавляемого поля
    :return: код возврата
    """
    ptr = cast(record, c_char_p)
    return IC_fldadd(ptr, tag, 0, to_utf(field), len(record))


def write_record(database: str, record: 'Array[c_char]') -> int:
    """
    Сохранение или обновление записи в указанной базе данных.
    :param database: имя базы данных
    :param record: запись, подлежащая сохранению
    :return: код возврата
    """
    ptr = cast(record, c_char_p)
    return IC_update(to_ansi(database), 0, 1, byref(ptr), len(record))


def replace_field(record: 'Array[c_char]', tag: int, repeat: int,
                  field: str) -> int:
    """
    Замена поля в записи.
    :param record: запись
    :param tag: метка заменяемого поля
    :param repeat: повторение поля (отсчет от 1)
    :param field: новое значение поля
    :return: код возврата
    """
    ptr = cast(record, c_char_p)
    index = IC_fieldn(ptr, tag, repeat)
    if index < 0:
        return ERR_UNKNOWN
    return IC_fldrep(ptr, index, to_utf(field), len(record))


def remove_field(record: 'Array[c_char]', tag: int, repeat: int) -> int:
    """
    Удаление поля из записи.
    :param record: запись
    :param tag: метка удаляемого поля
    :param repeat: повторение поля (отсчет от 1)
    :return: код возврата
    """
    ptr = cast(record, c_char_p)
    index = IC_fieldn(ptr, tag, repeat)
    if index < 0:
        return ERR_UNKNOWN
    return IC_fldrep(ptr, index, b'', len(record))


def empty_record(record: 'Array[c_char]') -> int:
    """
    Опустошение записи (удаление из нее всех полей).
    :param record: запись
    :return: код возврата
    """
    return IC_fldempty(cast(record, c_char_p))


def delete_record(record: 'Array[c_char]') -> int:
    """
    Установить в клиентской копии записи признак логического удаления.
    :param record: запись
    :return: код возврата
    """
    return IC_recdel(cast(record, c_char_p))


def undelete_record(record: 'Array[c_char]') -> int:
    """
    Удалить из клиентской копии записи признак логического удаления.
    :param record: запись
    :return: код возврата
    """
    return IC_recundel(cast(record, c_char_p))


def mark_record_unlocked(record: 'Array[c_char]') -> int:
    """
    Удалить из клиентской копии записи признак блокировки.
    :param record: запись
    :return: код возврата
    """
    return IC_recunlock(cast(record, c_char_p))


def record_actualized(record: 'Array[c_char]') -> bool:
    """
    Определение, установлен ли в локальной копии записи признак актуализации.
    :param record: запись
    :return: `true`, если признак установлен
    """
    return IC_isactualized(cast(record, c_char_p)) == 1


def record_locked(record: 'Array[c_char]') -> bool:
    """
    Определение, установлен ли в локальной копии записи признак блокировки.
    :param record: запись
    :return: `true`, если признак установлен
    """
    return IC_islocked(cast(record, c_char_p)) == 1


def record_deleted(record: 'Array[c_char]') -> bool:
    """
    Определение, установлен ли в локальной копии записи признак удаления.
    :param record: запись
    :return: `true`, если признак установлен
    """
    return IC_isdeleted(cast(record, c_char_p)) == 1
