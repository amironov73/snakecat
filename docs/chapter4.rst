=================
Служебные функции
=================

**from_ansi(buffer: Optional\[bytes\]) -> str**

    Конвертация буфера ctypes в обычную строку.

**from_utf(buffer: Optional\[bytes\]) -> str**

    Конвертация буфера ctypes в обычную строку.

**to_ansi(text: Optional\[str\]) -> bytes**

    Конвертация строки в байты в кодировке ANSI.

**to_utf(text: Optional\[str\]) -> bytes**

    Конвертация строки в байты в кодировке UTF-8.

**from_irbis(text: bytes) -> bytes**

    Замена псевдоразделителей строк на настоящие разделители.

**to_irbis(text: bytes) -> bytes**

    Замена разделителей строк на псевдоразделители.

**def error_to_string(ret_code: int) -> str**

    Получение текстового сообщения об ошибке по ее коду.
