<br>Веб-Сервис принимает на вход запросы с именем пользователя. Ему присваивается уникальный индефикатор (access_token).
<br>Вы можете загружать аудио файли в формате wav и сервис конвертирует их в mp3 фаил. Так же вы можете скачивать за 
<br>Как пользоваться сервисом:
<br>
<br>1)В файле .env измените переменные для подключения к нужной базе данных.
<br>
<br>2) Запустить docker-compose build. После создание контейнера запустить docker-compose up.
<br>
<br>3) Перейти на сайт http://127.0.0.1/docs. Здесь будет представлен весть функциолнал сервиса.
<br>
<br>4) Вкладка "/users" создаёт пользователя и присваевает уникальный индефикатор. Нажмите try it out, введите вместро string имя пользователя. В ответе будет id пользователя и его access_token.
<br>
<br>5) Вкладка "/users/{user_id}/recordings" позволяет загрузить wav фаил. Необходимо указать id пользователя, его access_token и выбрать фаил для загрузки. В ответе вы получите ссылку формата "http://localhost:8000/recordings/{recording_id}?user_id={user_id}&access_token={access_token})"
<br>
<br>6) С помощью полученной ссылки вы можете скачать загруженный ранее аудио фаил во вкладке "/recordings/{recording_id}". Вам необходимо просто вставить ссылку в поле url.
<br>
<br>
<br>P.S. 
<br>Если необходимо изменить ссылку на скачивание файла, это можно сделать в main.py, строка 61. Так же придётся убрать строки 71, 75, 76 если вы хотите убрать access_token в ссылке.
<br>
<br>
<br>
