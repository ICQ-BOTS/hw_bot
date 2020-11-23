<img src="https://github.com/ICQ-BOTS/hw_bot/blob/main/hw.png" width="100" height="100">


# Староста
[Староста](https://icq.im/hw_bot)

Старт:
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