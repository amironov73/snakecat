======================
Низкоуровневые функции
======================

Функции общего назначения
=========================

**IC_reg(host: c_char_p, port: c_char_p, arm: c_char, username: c_char_p, password: c_char_p, answer: POINTER(c_char_p), answer_size: c_int) -> c_int**

    Регистрация клиента на сервере.

    * **host** - адрес сервера в числовом виде (например 192.168.5.140).
    * **port** - рабочий порт сервера (6666).
    * **arm** - тип клиента.
    * **username** - имя пользователя, зарегистрированного на сервере.
    * **password** - пароль пользователя.
    * **answer** - выходной буфер для возвращаемых данных.
    * **answer_size** - размер выходного буфера в байтах.

**IC_unreg(username: c_char_p) -> c_int**

    Раз-регистрация клиента на сервере (сигнал об окончании работы).

    * **username** - имя пользователя, использованное при регистрации на сервере.

**IC_set_client_time_live(interval: c_int) -> c_int**

    Установка интервала подтверждения.

    * **interval** - интервал в минутах.

**IC_set_show_waiting(interval: c_int) -> c_int**

    Установка времени появления заставки ожидания.

    * **interval** - интервал в секундах.

**IC_set_webserver(option: c_int) -> c_int**

    Установка режима работы через Web-шлюз.

    * **option** - включение (1) или выключение (0) режима работы через Web-шлюз.

**IC_set_webcgi(cgi: c_char_p) -> c_int**

    Установка имени шлюза при работе через Web-шлюз.

    * **cgi** - имя шлюза (по умолчанию - /cgi-bin/wwwirbis.exe).

**IC_set_blocksocket(opt: c_int) -> c_int**

    Установка режима ожидания ответа от сервера.

    * **opt** - включение (1) или выключение (0) режима блокирующего ожидания ответа от сервера. По умолчанию блокирующий режим выключен.

**IC_isbusy() -> c_int**

    Определение завершения очередного обращения к серверу.

    Код возврата: 1 - выполняется запрос к серверу, 0 - обращение к серверу завершено.

Функции для работы с ресурсами
==============================

**IC_update_ini(ini_file: c_char_p) -> c_int**

    Обновление INI-файла – профиля пользователя на сервере.

    * **ini_file** - набор измененных строк в виде структуры INI-файла (в ANSI-кодировке).

**IC_getresourse**

    Чтение текстового ресурса (файла).

**IC_clearresourse**

    Очистка памяти кэша.

    В результате выполнения функции очищается кэш, в котором сохраняются запрошенные текстовые ресурсы (после чего при их запросе они берутся с сервера). При выполнении функции не производится обращение на сервер.

**IC_getresoursegroup**

    Групповое чтение текстовых ресурсов.

**IC_getbinaryresourse**

    Чтение двоичного ресурса.

**IC_putresourse**

    Запись текстового ресурса на сервер.

Функции для работы с мастер-файлом базы данных
==============================================

**IC_read**

**IC_readformat**

**IC_update**

**IC_updategroup**

**IC_runlock**

**IC_ifupdate**

**IC_maxmfn**

Функции для работы с записью
============================

**IC_fieldn**

**IC_field**

**IC_fldadd**

**IC_fldrep**

**IC_nfields**

**IC_nocc**

**IC_fldtag**

**IC_fldempty**

**IC_changemfn**

**IC_recdel**

**IC_recundel**

**IC_recunlock**

**IC_getmfn**

**IC_recdummy**

**IC_isactualized**

**IC_islocked**

**IC_isdeleted**

Функции для работы со словарем базы данных
==========================================

**IC_nexttrm**

**IC_nexttrmgroup**

**IC_prevtrm**

**IC_prevtrmgroup**

**IC_posting**

**IC_postinggroup**

**IC_postingformat**

Функции поиска
==============

**IC_search**

**IC_searchscan**

Функции форматирования
======================

**IC_sformat**

**IC_record_sformat**

**IC_sformatgroup**

Функции пакетной обработки
==========================

**IC_print**

**IC_stat**

**IC_gbl**

Функции администратора
======================

**IC_adm_restartserver**

**IC_adm_getdeletedlist**

**IC_adm_getalldeletedlists**

**IC_adm_dbempty**

**IC_adm_dbdelete**

**IC_adm_newdb**

**IC_adm_dbunlock**

**IC_adm_dbunlockmfn**

**IC_adm_dbstartcreatedictionry**

**IC_adm_dbstartreorgdictionry**

**IC_adm_dbstartreorgmaster**

**IC_adm_getclientlist**

**IC_adm_getclientslist**

**IC_adm_getprocesslist**

**IC_adm_setclientslist**

Вспомогательные функции
=======================

**IC_nooperation() -> c_int**

Подтверждение регистрации.

**IC_getposting(c_char_p, c_int) -> c_int**

Получить элемент исходной ссылки.

**IC_reset_delim(c_char_p) -> c_char_p**

Заменить реальные разделители строк $0D0A на псевдоразделители $3130.

**IC_delim_reset(c_char_p) -> c_char_p**

Заменить псевдоразделители $3130 на реальные разделители строк $0D0A.
