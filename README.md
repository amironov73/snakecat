# python_wrapper

Python wrapper for irbis64_client.dll

Supports:

* Windows environment only
* CPython 32-bit interpreter version 3.8

Example:

```python
from irbis import *

answerSize: int = 32000
buffer = create_string_buffer(answerSize)
answer = cast(buffer, c_char_p)

# Set blocking socket mode,
# get rid of obsessive window
rc = IC_set_blocksocket(1)
print('IC_blocksocket=', rc)

host = b'127.0.0.1'
port = b'6666'
arm = b'C'
user = b'librarian'
password = b'secret'
db = b'IBIS'

# Connect to the server
rc = IC_reg(host, port, arm, user, password, byref(answer), answerSize)
print('IC_reg=', rc)
if rc < 0:
    print('EXIT')
    exit()
else:
    print('IC_reg=', answer.value)

# Read one record from the server
rc = IC_read(db, 1, 0, byref(answer), answerSize)
print('IC_read=', rc)
if rc >= 0:
    print('IC_read=', answer.value)

# Disconnect from the server
print()
rc = IC_unreg(user)
print('IC_unreg=', rc)

print()
print('That''s All, Folks!')
```

### Build status

[![Build status](https://img.shields.io/appveyor/ci/AlexeyMironov/irbis64-client.svg)](https://ci.appveyor.com/project/AlexeyMironov/irbis64-client/)
