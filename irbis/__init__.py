# coding: utf-8

"""
Модуль содержит основную функциональность по работе с сервером ИРБИС64,
в т. ч. для манипуляций с записями.
"""

from irbis.dllwrapper import IC_reg, IC_unreg, \
    IC_set_client_time_live, IC_set_show_waiting, IC_set_webserver, \
    IC_set_webcgi, IC_set_blocksocket, IC_isbusy, IC_update_ini, \
    IC_getresourse, IC_clearresourse, IC_getresoursegroup, \
    IC_getbinaryresourse, IC_putresourse, IC_read, IC_readformat, \
    IC_update, IC_updategroup, IC_runlock, IC_ifupdate, IC_maxmfn

__all__ = ['IC_reg', 'IC_unreg', 'IC_set_client_time_live',
           'IC_set_show_waiting', 'IC_set_webserver', 'IC_set_webcgi',
           'IC_set_blocksocket', 'IC_isbusy', 'IC_update_ini',
           'IC_getresourse', 'IC_clearresourse', 'IC_getresoursegroup',
           'IC_getbinaryresourse', 'IC_putresourse', 'IC_read',
           'IC_readformat', 'IC_update', 'IC_updategroup',
           'IC_runlock', 'IC_ifupdate', 'IC_maxmfn']
