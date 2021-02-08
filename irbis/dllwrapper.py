# coding: utf-8

"""
Модуль содержит импорты функций из irbis64_client.dll
"""

import sys
import os.path
from ctypes import windll, c_char, c_char_p, c_int, POINTER

if sys.maxsize != 0x7fffffff:
    print('Only 32-bit systems are supported', file=sys.stderr)
    sys.exit(1)

if os.name != 'Windows' and os.name != 'nt':
    print('Only Windows systems are supported', file=sys.stderr)
    sys.exit(1)

_me = os.path.abspath(os.path.dirname(__file__))
dll = windll.LoadLibrary(os.path.join(_me, 'irbis64_client.dll'))

######################################################################
# Функции общего назначения
######################################################################

# Регистрация клиента на сервере

IC_reg = dll.IC_reg
IC_reg.restype = c_int
IC_reg.argtypes = [c_char_p, c_char_p, c_char, c_char_p, c_char_p,
                   POINTER(c_char_p), c_int]

# Раз-регистрация клиента на сервере (сигнал об окончании работы)

IC_unreg = dll.IC_unreg
IC_unreg.restype = c_int
IC_unreg.argtypes = [c_char_p]

# Установка интервала подтверждения

IC_set_client_time_live = dll.IC_set_client_time_live
IC_set_client_time_live.restype = c_int
IC_set_client_time_live.argtypes = [c_int]

# Установка времени появления заставки ожидания

IC_set_show_waiting = dll.IC_set_show_waiting
IC_set_show_waiting.restype = c_int
IC_set_show_waiting.argtypes = [c_int]

# Установка режима работы через Web-шлюз

IC_set_webserver = dll.IC_set_webserver
IC_set_webserver.restype = c_int
IC_set_webserver.argtypes = [c_int]

# Установка имени шлюза при работе через Web-шлюз

IC_set_webcgi = dll.IC_set_webcgi
IC_set_webcgi.restype = c_int
IC_set_webcgi.argtypes = [c_char_p]

# Установка режима ожидания ответа от сервера

IC_set_blocksocket = dll.IC_set_blocksocket
IC_set_blocksocket.restype = c_int
IC_set_blocksocket.argtypes = [c_int]

# Определение завершения очередного обращения к серверу

IC_isbusy = dll.IC_isbusy
IC_isbusy.restype = c_int
IC_isbusy.argtypes = []

######################################################################
# Функции для работы с ресурсами
######################################################################

# Обновление INI-файла – профиля пользователя на сервере

IC_update_ini = dll.IC_update_ini
IC_update_ini.restype = c_int
IC_update_ini.argtypes = [c_char_p]

# Чтение текстового ресурса (файла)

IC_getresourse = dll.IC_getresourse
IC_getresourse.restype = c_int
IC_getresourse.argtypes = [c_int, c_char_p, c_char_p, POINTER(c_char_p), c_int]

# Очистка памяти кэша

IC_clearresourse = dll.IC_clearresourse
IC_clearresourse.restype = c_int
IC_clearresourse.argtypes = []

# Групповое чтение текстовых ресурсов

IC_getresoursegroup = dll.IC_getresoursegroup
IC_getresoursegroup.restype = c_int
IC_getresoursegroup.argtypes = [c_char_p, POINTER(c_char_p), c_int]

# Чтение двоичного ресурса

IC_getbinaryresourse = dll.IC_getbinaryresourse
IC_getbinaryresourse.restype = c_int
IC_getbinaryresourse.argtypes = [c_int, c_char_p, c_char_p,
                                 POINTER(c_char_p), c_int]

# Запись текстового ресурса на сервер

IC_putresourse = dll.IC_putresourse
IC_putresourse.restype = c_int
IC_putresourse.argtypes = [c_int, c_char_p, c_char_p, c_char_p]

######################################################################
# Функции для работы с мастер-файлом базы данных
######################################################################

# Чтение записи

IC_read = dll.IC_read
IC_read.restype = c_int
IC_read.argtypes = [c_char_p, c_int, c_int, POINTER(c_char_p), c_int]

# Чтение записи с расформатированием

IC_readformat = dll.IC_readformat
IC_readformat.restype = c_int
IC_readformat.argtypes = [c_char_p, c_int, c_int, c_char_p,
                          POINTER(c_char_p), c_int, POINTER(c_char_p),
                          c_int]

# Запись/обновление записи в базе данных

IC_update = dll.IC_read
IC_update.restype = c_int
IC_update.argtypes = [c_char_p, c_int, c_int, POINTER(c_char_p), c_int]

# Групповая запись/обновление записей в базе данных

IC_updategroup = dll.IC_updategroup
IC_updategroup.restype = c_int
IC_updategroup.argtypes = [c_char_p, c_int, c_int, c_char_p, c_int]

# Разблокировать запись

IC_runlock = dll.IC_runlock
IC_runlock.restype = c_int
IC_runlock.argtypes = [c_char_p, c_int]

# Актуализировать запись

IC_ifupdate = dll.IC_ifupdate
IC_ifupdate.restype = c_int
IC_ifupdate.argtypes = [c_char_p, c_int]

# Получить максимальный MFN базы данных

IC_maxmfn = dll.IC_maxmfn
IC_maxmfn.restype = c_int
IC_maxmfn.argtypes = [c_char_p]

# # Связанная групповая запись/обновление записей в базах данных
#
# IC_updategroup_sinhronize = dll.IC_updategroup_sinhronize
# IC_updategroup_sinhronize.restype = c_int
# IC_updategroup_sinhronize.argtypes = [c_int, c_int, c_char_p,
#                                      POINTER(c_char_p), c_int]

######################################################################
# Функции для работы с записью
######################################################################

# Определить порядковый номер поля в записи

IC_fieldn = dll.IC_fieldn
IC_fieldn.restype = c_int
IC_fieldn.argtypes = [c_char_p, c_int, c_int]

# Прочитать заданное поле/подполе

IC_field = dll.IC_field
IC_field.restype = c_int
IC_field.argtypes = [c_char_p, c_int, c_char, c_char_p, c_int]

# Добавить поле в запись

IC_fldadd = dll.IC_fldadd
IC_fldadd.restype = c_int
IC_fldadd.argtypes = [c_char_p, c_int, c_int, c_char_p, c_int]

# Заменить поле

IC_fldrep = dll.IC_fldrep
IC_fldrep.restype = c_int
IC_fldrep.argtypes = [c_char_p, c_int, c_char_p, c_int]

# Определить количеств полей в записи

IC_nfields = dll.IC_nfields
IC_nfields.restype = c_int
IC_nfields.argtypes = [c_char_p]

# Определить количество повторений поля с заданной меткой

IC_nocc = dll.IC_nocc
IC_nocc.restype = c_int
IC_nocc.argtypes = [c_char_p, c_int]

# Определить метку поля с заданным порядковым номером

IC_fldtag = dll.IC_fldtag
IC_fldtag.restype = c_int
IC_fldtag.argtypes = [c_char_p, c_int]

# Опустошить запись

IC_fldempty = dll.IC_fldempty
IC_fldempty.restype = c_int
IC_fldempty.argtypes = [c_char_p]

# Поменять MFN записи

IC_changemfn = dll.IC_changemfn
IC_changemfn.restype = c_int
IC_changemfn.argtypes = [c_char_p, c_int]

# Установить признак логически удаленной записи

IC_recdel = dll.IC_recdel
IC_recdel.restype = c_int
IC_recdel.argtypes = [c_char_p]

# Снять признак логически удаленной записи

IC_recundel = dll.IC_recundel
IC_recundel.restype = c_int
IC_recundel.argtypes = [c_char_p]

# Снять признак заблокированности

IC_recunlock = dll.IC_recunlock
IC_recunlock.restype = c_int
IC_recunlock.argtypes = [c_char_p]

# Прочитать MFN записи

IC_getmfn = dll.IC_getmfn
IC_getmfn.restype = c_int
IC_getmfn.argtypes = [c_char_p]

# Создать пустую запись

IC_recdummy = dll.IC_recdummy
IC_recdummy.restype = c_int
IC_recdummy.argtypes = [c_char_p, c_int]

# Прочитать в статусе записи признак актуализированности

IC_isactualized = dll.IC_isActualized
IC_isactualized.restype = c_int
IC_isactualized.argtypes = [c_char_p]

# прочитать в статусе записи признак блокировки

IC_islocked = dll.IC_isLocked
IC_islocked.restype = c_int
IC_islocked.argtypes = [c_char_p]

# прочитать в статусе записи признак логического удаления

IC_isdeleted = dll.IC_isDeleted
IC_isdeleted.restype = c_int
IC_isdeleted.argtypes = [c_char_p]

######################################################################
# Функции для работы со словарем базы данных
######################################################################

# Получить список терминов словаря, начиная с заданного

IC_nexttrm = dll.IC_nexttrm
IC_nexttrm.restype = c_int
IC_nexttrm.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int]

# Получить список терминов словаря, начиная с заданного,
# и расформатировать записи, соответствующие первой ссылке каждого термина

IC_nexttrmgroup = dll.IC_nexttrmgroup
IC_nexttrmgroup.restype = c_int
IC_nexttrmgroup.argtypes = [c_char_p, c_char_p, c_int, c_char_p,
                            c_char_p, c_int]

# Получить список терминов словаря, начиная с заданного, в обратном порядке

IC_prevtrm = dll.IC_prevtrm
IC_prevtrm.restype = c_int
IC_prevtrm.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int]

# Получить список терминов словаря, начиная с заданного, в обратном порядке
# и расформатировать записи, соответствующие первой ссылке каждого термина

IC_prevtrmgroup = dll.IC_prevtrmgroup
IC_prevtrmgroup.restype = c_int
IC_prevtrmgroup.argtypes = [c_char_p, c_char_p, c_int, c_char_p,
                            c_char_p, c_int]

# Получить список ссылок для заданного термина

IC_posting = dll.IC_posting
IC_posting.restype = c_int
IC_posting.argtypes = [c_char_p, c_char_p, c_int, c_int, c_char_p, c_int]

# Получить список первых ссылок для списка заданных терминов

IC_postinggroup = dll.IC_postinggroup
IC_postinggroup.restype = c_int
IC_postinggroup.argtypes = [c_char_p, c_char_p, c_char_p, c_int]

# Получить список ссылок для заданного термина и расформатировать
# записи им соответствующие

IC_postingformat = dll.IC_postingformat
IC_postingformat.restype = c_int
IC_postingformat.argtypes = [c_char_p, c_char_p, c_int, c_int, c_char_p,
                             c_char_p, c_int, c_char_p, c_int]

######################################################################
# Функции поиска
######################################################################

# Прямой (по словарю) поиск записей по заданному поисковому выражению

IC_search = dll.IC_search
IC_search.restype = c_int
IC_search.argtypes = [c_char_p, c_char_p, c_int, c_int, c_char_p,
                      c_char_p, c_int]

# Последовательный поиск по результату прямого поиска и/или
# по заданному диапазону записей

IC_searchscan = dll.IC_searchscan
IC_searchscan.restype = c_int
IC_searchscan.argtypes = [c_char_p, c_char_p, c_int, c_int, c_char_p,
                          c_int, c_int, c_char_p, c_char_p, c_int]

######################################################################
# Функции форматирования
######################################################################

# Расформатирование записи, заданной по номеру (mfn)

IC_sformat = dll.IC_sformat
IC_sformat.restype = c_int
IC_sformat.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]

# Расформатирование записи в клиентском представлении

IC_record_sformat = dll.IC_record_sformat
IC_record_sformat.restype = c_int
IC_record_sformat.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]

# Расформатирование группы записей

IC_sformatgroup = dll.IC_sformatgroup
IC_sformatgroup.restype = c_int
IC_sformatgroup.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]

######################################################################
# Функции пакетной обработки
######################################################################

# Формирование выходной табличной формы

IC_print = dll.IC_print
IC_print.restype = c_int
IC_print.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p,
                     c_int, c_int, c_char_p, c_char_p, c_char_p, c_int]

# Формирование выходной формы в виде статистических распределений

IC_stat = dll.IC_stat
IC_stat.restype = IC_stat
IC_stat.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int,
                    c_char_p, c_char_p, c_char_p, c_int]

# Выполнение задания на глобальную корректировку

IC_gbl = dll.IC_gbl
IC_gbl.restype = c_int
IC_gbl.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int, c_int,
                   c_char_p, c_char_p, c_char_p, c_int]

######################################################################
# Функции администратора
######################################################################

# Перезапустить сервер ИРБИС64

IC_adm_restartserver = dll.IC_adm_restartserver
IC_adm_restartserver.restype = c_int
IC_adm_restartserver.argtypes = []

# Получить список удаленных документов

IC_adm_getdeletedlist = dll.IC_adm_getDeletedList
IC_adm_getdeletedlist.restype = c_int
IC_adm_getdeletedlist.argtypes = [c_char_p, c_char_p, c_int]

# Получить общие сведения о базе данных: списки
# удаленных/заблокированных/неактуализированных, максимальный MFN
# и признак монопольной блокировки

IC_adm_getalldeletedlists = dll.IC_adm_getallDeletedLists
IC_adm_getalldeletedlists.restype = c_int
IC_adm_getalldeletedlists.argtypes = [c_char_p, c_char_p, c_int]

# Опустошить базу данных

IC_adm_dbempty = dll.IC_adm_dbempty
IC_adm_dbempty.restype = c_int
IC_adm_dbempty.argtypes = [c_char_p]

# Удалить базу данных

IC_adm_dbdelete = dll.IC_adm_dbdelete
IC_adm_dbdelete.restype = c_int
IC_adm_dbdelete.argtypes = [c_char_p]

# Создать новую базу данных электронного каталога

IC_adm_newdb = dll.IC_adm_newdb
IC_adm_newdb.restype = c_int
IC_adm_newdb.argtypes = [c_char_p, c_char_p, c_int]

# Снять монопольную блокировку базы данных

IC_adm_dbunlock = dll.IC_adm_DBunlock
IC_adm_dbunlock.restype = c_int
IC_adm_dbunlock.argtypes = [c_char_p]

# Снять блокировку заданных записей

IC_adm_dbunlockmfn = dll.IC_adm_DBunlockMFN
IC_adm_dbunlockmfn.restype = c_int
IC_adm_dbunlockmfn.argtypes = [c_char_p, c_char_p]

# Создать словарь базы данных заново

IC_adm_dbstartcreatedictionry = dll.IC_adm_DBStartCreateDictionry
IC_adm_dbstartcreatedictionry.restype = c_int
IC_adm_dbstartcreatedictionry.argtypes = [c_char_p]

# Реорганизовать словарь базы данных

IC_adm_dbstartreorgdictionry = dll.IC_adm_DBStartReorgDictionry
IC_adm_dbstartreorgdictionry.restype = c_int
IC_adm_dbstartreorgdictionry.argtypes = [c_char_p]

# Реорганизовать файл документов базы данных

IC_adm_dbstartreorgmaster = dll.IC_adm_DBStartReorgMaster
IC_adm_dbstartreorgmaster.restype = c_int
IC_adm_dbstartreorgmaster.argtypes = [c_char_p]

# Получить список зарегистрированных (текущих) клиентов

IC_adm_getclientlist = dll.IC_adm_getClientlist
IC_adm_getclientlist.restype = c_int
IC_adm_getclientlist.argtypes = [c_char_p, c_int]

# Получить список клиентов для доступа к серверу

IC_adm_getclientslist = dll.IC_adm_getClientslist
IC_adm_getclientslist.restype = c_int
IC_adm_getclientslist.argtypes = [c_char_p, c_int]

# Получить список запущенных процессов на сервере

IC_adm_getprocesslist = dll.IC_adm_getProcessList
IC_adm_getprocesslist.restype = c_int
IC_adm_getprocesslist.argtypes = [c_char_p, c_int]

# Обновить список клиентов для доступа к серверу

IC_adm_setclientslist = dll.IC_adm_SetClientslist
IC_adm_setclientslist.restype = c_int
IC_adm_setclientslist.argtypes = [c_char_p]
