
# [Староста](https://icq.im/hw_bot)

<a href="https://icq.im/hw_bot"><img src="https://github.com/ICQ-BOTS/hw_bot/blob/main/hw.png" width="100" height="100"></a>

# Оглавление 
 - [Описание](https://github.com/ICQ-BOTS/hw_bot#описание)
 - [Установка](https://github.com/ICQ-BOTS/hw_bot#установка)
 - [Скриншоты работы](https://github.com/ICQ-BOTS/hw_bot#скриншоты-работы)

# Описание
Записывает расписание и домашнюю работу!

# Установка

1. Установка всех зависимостей 
```bash
pip install -r requirements.txt
```

2. Запуск space tarantool
```bash
tarantoolctl start hw.lua
```
> Файл из папки scheme нужно перекинуть в /etc/tarantool/instances.available

3. Вставляем токен в fate.bot

4. Запуск бота!
```bash
python3 hw_bot.py
```

# Скриншоты работы
<img src="https://github.com/ICQ-BOTS/hw_bot/blob/main/img/1.png" width="400">
<img src="https://github.com/ICQ-BOTS/hw_bot/blob/main/img/2.png" width="400">