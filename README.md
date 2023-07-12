# DIY Wiki bot - телеграм бот
Проект DIY Wiki bot это интерактивный помощник, который позволяет пользователям получать информацию о различных DIY проектах. Бот предоставляет доступ к огромной базе знаний, в которой содержатся инструкции, советы и схемы для самостоятельного создания различных объектов.

## Функциональность
1) Поиск проектов: пользователи могут искать проекты по ключевым словам в базе данных DIY Wiki Bot. Результаты поиска представляются в виде текстовых сообщений с кратким описанием и ссылками на полные инструкции.<details><summary><strong>Сведения</strong></summary>
Поиск проектов происходит через инлайн режим:<br/><img src="https://i.ibb.co/gJ1vccR/Screenshot-125.jpg" align="center" width="500px" alt="Screenshot-125" border="0"><br/>
</details>

2) Категории: пользователи могут просматривать проекты по категориям, таким как электроника, мебель, ремонт, садоводство и т.д.<details><summary><strong>Сведения</strong></summary>
  Для инлайн кнопок написан алгоритм для красивого вывода кнопок(не как обычно таблица по типу n*m):<img src="https://i.ibb.co/RNF3Xb3/Screenshot-126.jpg" align="center" width="500px" alt="Screenshot-126" border="0">
</details>

3) Тренды: пользователи могут смотреть сортированные по избранным DIY проекты из базы данных DIY Wiki Bot.<details><summary><strong>Сведения</strong></summary>Кнопка "Смотреть" ведет на статью в телеграф.<br/><img src="https://i.ibb.co/Q9HbmMQ/Screenshot-128.jpg" align="center" width="500px" alt="Screenshot-126" border="0"><br/>
</details>

4) Фавориты, прочитанные, законченные: пользователи могут сохранять интересующие их проекты в список "Фавориты" и в "Прочитанные", "Законченные" для последующего доступа.<details><summary><strong>Сведения</strong></summary>
  У каждой плашки с информацией о DIY проекте, есть кнопки с добавлением в "Избранное" для последующего доступа к ним<br/><img src="https://i.ibb.co/kMB6mWc/Screenshot-130.jpg" align="center" width="500px" alt="Screenshot-130" border="0"><br/>
</details>

5) Паки изображений: пользователи могут поменять темы изображений на главных плашках.<details><summary><strong>Сведения</strong></summary>
  Меняются картинки в каждой главной плашке<br/><img src="https://i.ibb.co/5Bmz9Q1/Screenshot-131.jpg" align="center" width="500px" alt="Screenshot-131" border="0">
</details>

6) Загрузка изобржений на сервис telegraph по команде /upload_photo

## Установка и запуск
- [ ] Клонируйте репозиторий на локальный сервер
Команда для клонирования:
  ```
  git clone https://github.com/Iki-oops/yamdb_final.git
  ```

- [ ] Измените .env.dist на .env и настройте переменные окружения .env
  > Необходимо создать бота в телеграм и получить его токен. Ссылка на бота, который создает ботов: https://t.me/BotFather

- [ ] Создайте виртуальное окружение и установите все необходимые зависимости:
  ```
  python3 -m venv venv
  pip install requirements.txt
  ```

- [ ] Сделайте миграции:
  ```
  python django_app.py makemigrations
  python django_app.py migrate
  ```

- [ ] Запустите приложение:
  ```
  python bot.py
  ```

### Стек технологий:
 - Язык программирования: python
 - Фреймворк: Django ORM
 - База данных: postgreSQL
 - Библиотеки: aiogram, aiohttp

### Ссылка на бота: https://t.me/DIY_wiki_bot
  > Иногда может быть выключен
