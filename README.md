# python_wrapper

Python wrapper for irbis64_client.dll

Supports:

* Windows environment only
* CPython 32-bit interpreter version 3.8

Example:

```python
import sys
from irbis import connect, disconnect, read_record, get_max_mfn, \
    hide_window, IRBIS_CATALOG

# Set blocking socket mode,
# get rid of obsessive windowhide_window()

# Data for the connection
HOST = '127.0.0.1'
PORT = '6666'
ARM = IRBIS_CATALOG
USER = 'librarian'
PASSWORD = 'secret'
DB = 'IBIS'

# Connect to the server
rc, ini = connect(HOST, PORT, ARM, USER, PASSWORD)
print('connect=', rc)
if rc < 0:
    print('EXIT')
    sys.exit(1)
else:
    print('connect=', ini)

# Read one record from the server
rc, record = read_record(DB, 1)
print('IC_read=', rc)
if rc >= 0:
    print('IC_read=', record)

# Get the maximal MFN
rc = get_max_mfn(DB)
print('IC_maxmfn=', rc)

# Disconnect from the server
print()
rc = disconnect(USER)
print('IC_unreg=', rc)

print()
print('That''s All, Folks!')
```

### Build status

[![Build status](https://img.shields.io/appveyor/ci/AlexeyMironov/python-wrapper.svg)](https://ci.appveyor.com/project/AlexeyMironov/python-wrapper/)
