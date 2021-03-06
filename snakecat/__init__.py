# coding: utf-8

"""
Модуль содержит основную функциональность по работе с сервером ИРБИС64,
в т. ч. для манипуляций с записями.
"""

__version__ = '0.1.100'
__author__ = 'Alexey Mironov'
__email__ = 'amironov73@gmail.com'

__title__ = 'snakecat'
__summary__ = 'ctypes wrapper for irbis64_client.dll'
__uri__ = 'http://arsmagna.ru'

__license__ = 'MIT License'
__copyright__ = 'Copyright 2021 Alexey Mironov'


from snakecat.constants import NO_ERROR, ERR_USER, ERR_BUSY, \
    ERR_UNKNOWN, ERR_BUFSIZE, TERM_NOT_EXISTS, TERM_LAST_IN_LIST, \
    TERM_FIRST_IN_LIST, ERR_DBEWLOCK, ERR_RECLOCKED, VERSION_ERROR, \
    READ_WRONG_MFN, REC_DELETE, REC_PHYS_DELETE, ERROR_CLIENT_FMT, \
    SERVER_EXECUTE_ERROR, ANSWER_LENGTH_ERROR, WRONG_PROTOCOL, \
    CLIENT_NOT_IN_LIST, CLIENT_NOT_IN_USE, CLIENT_IDENTIFIER_WRONG, \
    CLIENT_LIST_OVERLOAD, CLIENT_ALREADY_EXISTS, CLIENT_NOT_ALLOWED, \
    WRONG_PASSWORD, FILE_NOT_EXISTS, SERVER_OVERLOAD, PROCESS_ERROR, \
    GLOBAL_ERROR, SYSPATH, DATAPATH, DBNPATH2, DBNPATH3, DBNPATH10, \
    FULLTEXTPATH, INTERNALRESOURCEPATH, IRBIS_READER, \
    IRBIS_ADMINISTRATOR, IRBIS_CATALOG, IRBIS_COMPLECT, \
    IRBIS_BOOKLAND, IRBIS_BOOKPROVD, MAX_POSTINGS_IN_PACKET, \
    ANSI, UTF

from snakecat.dllwrapper import IC_reg, IC_unreg, \
    IC_set_client_time_live, IC_set_show_waiting, IC_set_webserver, \
    IC_set_webcgi, IC_set_blocksocket, IC_isbusy, IC_update_ini, \
    IC_getresourse, IC_clearresourse, IC_getresoursegroup, \
    IC_getbinaryresourse, IC_putresourse, IC_read, IC_readformat, \
    IC_update, IC_updategroup, IC_runlock, IC_ifupdate, IC_maxmfn, \
    IC_fieldn, IC_field, IC_fldadd, IC_fldrep, IC_nfields, IC_nocc, \
    IC_fldtag, IC_fldempty, IC_changemfn, IC_recdel, IC_recundel, \
    IC_recunlock, IC_getmfn, IC_recdummy, IC_isactualized, IC_islocked, \
    IC_isdeleted, IC_nexttrm, IC_nexttrmgroup, IC_prevtrm, \
    IC_prevtrmgroup, IC_posting, IC_postinggroup, IC_postingformat, \
    IC_search, IC_searchscan, IC_sformat, IC_record_sformat, \
    IC_sformatgroup, IC_print, IC_stat, IC_gbl, IC_adm_restartserver, \
    IC_adm_getdeletedlist, IC_adm_getalldeletedlists, IC_adm_dbempty, \
    IC_adm_newdb, IC_adm_dbunlock, IC_adm_dbunlockmfn, \
    IC_adm_dbstartcreatedictionry, IC_adm_dbstartreorgmaster, \
    IC_adm_getclientlist, IC_adm_getclientslist, IC_adm_getprocesslist, \
    IC_adm_setclientslist, IC_adm_dbdelete, IC_adm_dbstartreorgdictionry, \
    IC_nooperation, IC_reset_delim, IC_delim_reset

from snakecat.comfort import connect, disconnect, read_record, \
    get_max_mfn, hide_window, error_to_string, from_ansi, \
    from_utf, search, search_format, format_record, fm, \
    print_form, get_deleted_records, to_ansi, to_utf, from_irbis, \
    to_irbis, read_terms, trim_prefix, read_file, clear_cache, \
    write_file, unlock_record, actualize_record, actualize_database, \
    create_record, add_field, write_record, replace_field, \
    remove_field, empty_record, delete_record, undelete_record, \
    mark_record_unlocked, record_locked, record_deleted, \
    record_actualized, use_web_gateway

__all__ = ['NO_ERROR', 'ERR_USER', 'ERR_BUSY', 'ERR_UNKNOWN',
           'ERR_BUFSIZE', 'TERM_NOT_EXISTS', 'TERM_LAST_IN_LIST',
           'TERM_FIRST_IN_LIST', 'ERR_DBEWLOCK', 'ERR_RECLOCKED',
           'VERSION_ERROR', 'READ_WRONG_MFN', 'REC_DELETE',
           'REC_PHYS_DELETE', 'ERROR_CLIENT_FMT',
           'SERVER_EXECUTE_ERROR', 'ANSWER_LENGTH_ERROR',
           'WRONG_PROTOCOL', 'CLIENT_NOT_IN_LIST',
           'CLIENT_NOT_IN_USE', 'CLIENT_IDENTIFIER_WRONG',
           'CLIENT_LIST_OVERLOAD', 'CLIENT_ALREADY_EXISTS',
           'CLIENT_NOT_ALLOWED', 'WRONG_PASSWORD', 'FILE_NOT_EXISTS',
           'SERVER_OVERLOAD', 'PROCESS_ERROR', 'GLOBAL_ERROR',
           'SYSPATH', 'DATAPATH', 'DBNPATH2', 'DBNPATH3', 'DBNPATH10',
           'FULLTEXTPATH', 'INTERNALRESOURCEPATH', 'IRBIS_READER',
           'IRBIS_ADMINISTRATOR', 'IRBIS_CATALOG', 'IRBIS_COMPLECT',
           'IRBIS_BOOKLAND', 'IRBIS_BOOKPROVD',
           'MAX_POSTINGS_IN_PACKET', 'ANSI', 'UTF',
           'IC_reg', 'IC_unreg', 'IC_set_client_time_live',
           'IC_set_show_waiting', 'IC_set_webserver', 'IC_set_webcgi',
           'IC_set_blocksocket', 'IC_isbusy', 'IC_update_ini',
           'IC_getresourse', 'IC_clearresourse', 'IC_getresoursegroup',
           'IC_getbinaryresourse', 'IC_putresourse', 'IC_read',
           'IC_readformat', 'IC_update', 'IC_updategroup',
           'IC_runlock', 'IC_ifupdate', 'IC_maxmfn',
           'IC_fieldn', 'IC_field', 'IC_fldadd', 'IC_fldrep',
           'IC_nfields', 'IC_nocc', 'IC_fldtag', 'IC_fldempty',
           'IC_changemfn', 'IC_recdel', 'IC_recundel', 'IC_recunlock',
           'IC_getmfn', 'IC_recdummy', 'IC_isactualized', 'IC_islocked',
           'IC_isdeleted', 'IC_nexttrm', 'IC_nexttrmgroup', 'IC_prevtrm',
           'IC_prevtrmgroup', 'IC_posting', 'IC_postinggroup',
           'IC_postingformat', 'IC_search', 'IC_searchscan',
           'IC_sformat', 'IC_record_sformat', 'IC_sformatgroup',
           'IC_print', 'IC_stat', 'IC_gbl', 'IC_adm_restartserver',
           'IC_adm_getdeletedlist', 'IC_adm_getalldeletedlists',
           'IC_adm_dbempty', 'IC_adm_newdb', 'IC_adm_dbunlock',
           'IC_adm_dbunlockmfn', 'IC_adm_dbstartcreatedictionry',
           'IC_adm_dbstartreorgmaster', 'IC_adm_getclientlist',
           'IC_adm_getclientslist', 'IC_adm_getprocesslist',
           'IC_adm_setclientslist', 'IC_adm_dbdelete',
           'IC_adm_dbstartreorgdictionry', 'IC_nooperation',
           'IC_delim_reset', 'IC_reset_delim',
           'connect', 'disconnect', 'read_record', 'get_max_mfn',
           'hide_window', 'error_to_string', 'from_ansi',
           'from_utf', 'search', 'search_format', 'format_record',
           'fm', 'print_form', 'get_deleted_records', 'to_ansi',
           'to_utf', 'from_irbis', 'to_irbis', 'read_terms',
           'trim_prefix', 'read_file', 'clear_cache', 'write_file',
           'unlock_record', 'actualize_record', 'actualize_database',
           'create_record', 'add_field', 'write_record', 'replace_field',
           'remove_field', 'empty_record', 'delete_record',
           'undelete_record', 'mark_record_unlocked', 'record_locked',
           'record_actualized', 'record_deleted', 'use_web_gateway']
