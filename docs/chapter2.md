# Высокоуровневые функции

### Подключение и отключение

**connect(host: str, port: str, arm: str, user: str,
          password: str) -> Tuple[int, str]**

Подключение к серверу -- регистрация клиента на сервере.

**disconnect(user: str) -> int:**

Отключение от сервера -- разрегистрация клиента на сервере, сигнал об окончании работы.

**is_busy() -> bool**

Определение, не занят ли в данный момент сервер обработкой запроса от данного клиента.

### Настройка клиента

**hide_window() -> None**

Прячем надоедливое окно, переходя в блокирующий режим сокетов.

### Функции работы с ресурсами

**read_file(database: str, file_name: str, 
            path: int = DBNPATH2) -> Tuple\[int, str\]**

Чтение текстового файла с сервера.

**write_file(database: str, file_name: str, content: str, 
             path: int = DBNPATH2) -> int**

Запись текстового файла на сервер.

**clear_cache() -> int**

Очистка локального кэша форматов, меню и прочих ресурсов, прочитанных с сервера.