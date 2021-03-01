# Snake Cat

## cpython wrapper for irbis64_client.dll

<img src="assets/snakecat.jpg" alt="Snake Cat" width="100" style="float: left; padding-right: 10px;"/>

Supports:

* Windows environment only
* CPython 32-bit interpreter version 3.6+

Example:

```python
import sys
import snakecat as irbis

# Set blocking socket mode,
# get rid of obsessive window
irbis.hide_window()

# Data for the connection
HOST = '127.0.0.1'
PORT = '6666'
ARM = 'C'
USER = 'librarian'
PASSWORD = 'secret'
DB = 'IBIS'

# Connect to the server
rc, ini = irbis.connect(HOST, PORT, ARM, USER, PASSWORD)
print('connect=', rc)
if rc < 0:
    print(irbis.error_to_string(rc))
    print('EXIT')
    sys.exit(1)
else:
    print('connect=', ini)

# Read one record from the server
rc, record = irbis.read_record(DB, 1)
print('read_record=', rc)
if rc >= 0:
    print('IC_read=', record)

# Get the maximal MFN
rc = irbis.get_max_mfn(DB)
print('get_max_mfn=', rc)

# Disconnect from the server
print()
rc = irbis.disconnect(USER)
print('disconnect=', rc)

print()
print('That''s All, Folks!')
```

### Build status

[![Build status](https://img.shields.io/appveyor/ci/AlexeyMironov/python-wrapper.svg)](https://ci.appveyor.com/project/AlexeyMironov/python-wrapper/)

### Documentation (in russian)

[![Badge](https://readthedocs.org/projects/snakecat/badge/)](https://snakecat.readthedocs.io/) 
