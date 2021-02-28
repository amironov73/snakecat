=================
Служебные функции
=================

**def from_ansi(buffer: Optional\[bytes\]) -> str**

    Превращаем буфер ctypes в обычную строку.

**def from_utf(buffer: Optional\[bytes\]) -> str**

    Превращаем буфер ctypes в обычную строку.

**def to_ansi(text: str) -> bytes**

    Конвертируем строку в байты в кодировке ANSI.

**def to_utf(text: str) -> bytes**

    Конвертируем строку в байты в кодировке UTF-8.

**def from_irbis(text: bytes) -> bytes**

    Заменяем псевдоразделители строк на настоящие разделители.

**def to_irbis(text: bytes) -> bytes**

    Заменяем разделители строк на псевдоразделители.
