# AlmaUBot
https://www.youtube.com/watch?v=wj1Vwq3IrL4&list=PLwVBSkoL97Q3phZRyInbM4lShvS1cBl-U&index=1 - гайд

~~База данных - https://customer.elephantsql.com\~~,
~~Хостинг бота - https://heroku.com~~

Хостинг бота - Google Cloud,

База данных - Google Cloud SQL

Список что нужно сделать:
1) Создать токен через botfather ✔
2) Создать основной функционал ✔
3) Сделать клавиатуру для получения расписания  ✔
4) Сделать клавиатуру для FAQ ✔
5) Создать и подключить бота к PostgreSql ✔
6) Добавить панель для админа  ✔
7) Сделать функцию массовой рассылки ✔
8) Сделать функцию массовой рассылки по дате и времени ❌
9) Добавить функцию обновления расписания для адвайзеров, через панель админа обновление поступает в бд ✔
10) Добавить возможность парсить platonus и получать оттуда данные (Невозможно сделать из-за защиты) ❌
11) Добавть возможность выбора языка бота (Eng, Ru, Kz) ❌
12) Перенести бота с pyTelegramBotAPI на aiogram ✔
13) Добавть возможность обновление кнопки расписания ✔
14) Добавть возможность удаление кнопки расписания ✔




**Для сервера:**
```
Обновить даемон - sudo systemctl daemon-reload
Незнаю чото - sudo systemctl enable bot
Стартануть бота - sudo systemctl start bot
Проверить статус - sudo systemctl status bot
Шобы остановить бота - sudo systemctl stop bot
Для просмотра логов - journalctl --no-pager
```

**Для создания сервиса:**
```
[Unit]
Description=Telegram bot 'Almau Bot'
After=syslog.target
After=network.target

[Service]
Type=simple
User=killka_m
WorkingDirectory=/home/killka_m/AlmaUBot_aiogram
ExecStart=/home/killka_m/AlmaUBot_aiogram/almaubotenv/bin/python3 app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
**Остальное:**
```
Войти в root - sudo -i
Как поменять название файла - mv название_файла тут_новое_название
Чтобы поменять линки:
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
```