# AlmaUBot
https://www.youtube.com/watch?v=wj1Vwq3IrL4&list=PLwVBSkoL97Q3phZRyInbM4lShvS1cBl-U&index=1 - гайд

~~База данных - https://customer.elephantsql.com\~~,
~~Хостинг бота - https://heroku.com~~
База данных - Google Cloud SQL,
Хостинг бота - Google Cloud

**Для сервера:**
```
Обновить даемон - sudo systemctl daemon-reload
Первоначальная команда включения сервиса - sudo systemctl enable bot
Запустить бота - sudo systemctl start bot
Проверить статус и логи - sudo systemctl status bot
Для останвоки - sudo systemctl stop bot
Для перезапуска - sudo systemctl restart bot
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
User=botadmin
WorkingDirectory=/home/botadmin/almaubot
ExecStart=/home/botadmin/almaubot/myprojectenv/bin/python app.py
Restart=Always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
**Остальное:**
```
Войти в root - sudo -i
Как поменять название файла - mv название_файла тут_новое_название
Чтобы поменять линки питона:
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 (единица в конце обозначает приоритет)
```
**Настройка сервера**
```
sudo apt -y upgrade
1) sudo -i
2) adduser botadmin
3) войти в etc/sudoers и выдать нужному пользователю root права
4) sudo nano /etc/ssh/sshd_config . PasswordAuthentication сделать yes
чтобы можно было подключаться через ip,
   Потом - sudo systemctl reload sshd
5) git clone проекта,
6) sudo apt-get install python3-pip
   sudo -H pip3 install --upgrade pip
   sudo -H pip3 install virtualenv
7) virtualenv myprojectenv - создаем виртуальное окружение
8) source myprojectenv/bin/activate - входим в него
9) pip install -r requirements.txt - устанавливаем зависимости
10) sudo nano /etc/systemd/system/bot.service - создаем bot.service
```
**Настройка PostgreSQL сервера**
```
1) Созать сервер в CloudSql
2) Подключиться к нему через pgadmin
3) Создать базу данных и из бекапа вытащить данные
```
**Установка redis storage**
```
1) Linux - sudo apt-get install redis-server
   sudo systemctl enable redis-server.service
   sudo systemctl restart redis-server.service
2) Windows - https://www.youtube.com/watch?v=rcH6Ao9MMGU&feature=youtu.be ,
   https://github.com/microsoftarchive/redis/releases/tag/win-3.2.100
```