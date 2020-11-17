# Сервис аутентификации

Данный документ содержит описание работы и информацию о развертке микросервиса, предназначенного для аутентификации пользователей.

Название: `auth`

Структура сервиса:

| Файл                 | Описание                                                   |
| -------------------- | ---------------------------------------------------------- |
| `auth.py`            | Код микросервиса                                           |
| `config.py`          | Конфигурационная информация для auth.py                    |
| `config.yml`         | Конфигурационный файл со строкой подключения к RabbitMQ    |
| `docker-compose.yml` | Изолированная развертка сервиса вместе с (RabbitMQ, Redis) |
| `run.sh`             | Файл для запуска сервиса из Docker контейнера              |
| `requirements.txt`   | Верхнеуровневые зависимости                                |
| `Dockerfile`         | Описание сборки контейнера сервиса                         |
| `README.md`          | Описание микросервиса                                      |

## API

### RPC

Регистрация нового пользователя (логин пользователя должен быть уникальным):

```bat
n.rpc.auth.register(login, password)

Args: login (unique), password
Returns: True if user was registered and False otherwise
```

Вход в систему (получение JWT токена):

```bat
n.rpc.auth.login(login, password)

Args: login, password
Returns: JWT or False if user is not valid
```

Проверка JWT токена на валидность:

```bat
n.rpc.auth.check_jwt(jwt_token)

Args: JWT-token
Returns: user login or False if token is not valid
```

Получение списка логинов всех пользователей:

```bat
n.rpc.auth.get_all_logins()

Args: nothing
Returns: [login_1, ..., login_n]
```

## Запуск

### Локальный запуск

Для локального запуска микросервиса требуется запустить контейнер с RabbitMQ.

```bat
docker-compose up -d
```

Затем из папки микросервиса вызвать

```bat
nameko run auth
```

Для проверки `rpc` запустите в командной строке:

```bat
nameko shell
```

После того как откроется интерактивная Python среда, обратитесь к сервису одной из команд, представленных выше в разделе `rpc`.

### Запуск в контейнере

Чтобы запустить микросервис в контейнере вызовите команду:

```bat
docker-compose up
```

> если вы не хотите просмотривать логи, добавьте флаг `-d` в конце

Микросервис запустится вместе с RabbitMQ и Redis в контейнерах.
