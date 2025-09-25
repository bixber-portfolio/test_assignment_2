# resource_monitoring_system

## 🔍 Описание:
**RESOURCE_MONITORING_SYSTEM** - система мониторинга виртуальных машин, которые параллельно опрашивают определенный URL-адрес в Интернете. Система разработана на основе веб-приложения Django.


![logotype](https://firstvds.ru/sites/default/files/2024-04/240411_%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3_%D0%9C%D0%BE%D0%BD%D1%82%D0%B0%D0%B6%D0%BD%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C%201.png)

---

## 💡 Как начать пользоваться проектом:

1. **Склонировать репозиторий к себе на компьютер:**
```bash
# HTTPS протокол
git clone https://github.com/bixber-portfolio/test_assignment_2.git
```

2. **Открыть папку репозитория через IDE и перейти в папку с кодом проекта:**
```bash
# Относительно корневой папки
cd monitoring/
```

3. **Создать и активировать виртуальное окружение:**
```bash
# Для пользователей OC Windows:
python -m venv venv
source venv/Scripts/activate
# Для пользователей OC Linux/macOS:
python3 -m venv venv
source venv/bin/activate
```

4. **Обновить пакетный менеджер *pip*:**
```bash
# Для пользователей OC Windows:
python -m pip install --upgrade pip
# Для пользователей OC Linux/macOS:
python3 -m pip install --upgrade pip
```

5. **Установить зависимости из файла requirements.txt:**
```bash
# Для пользователей OC Windows:
pip install -r requirements.txt
# Для пользователей OC Linux/macOS:
pip3 install -r requirements.txt
```

6. **Зайти в файл *.env.dev* и сменить (при необходимости) данные БД:**
```bash
# Сопоставить имя пользователя и пароль СУБД MySQL с данными в файле (они должны совпадать)
DB_USER=root
DB_PASSWORD=root
```
![logotype](https://i.ibb.co/wFGWj4k0/Screenshot-1.png)

7. **Вручную создать базу данных в MySQL строкой запроса:**
```sql
-- Имя БД должно совпадать с именем переменной 'DB_NAME' в файле .env.dev
CREATE SCHEMA `monitoring` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
```

8. **Выполнить миграции Django в базе данных:**
```bash
# Для пользователей OC Windows:
python manage.py migrate
# Для пользователей OC Linux/macOS:
python3 manage.py migrate
```

9. **Загрузить тестовые данные (фикстуры) базы данных:**
```bash
# Для пользователей OC Windows:
python manage.py loaddata fixtures/initial_machines.json
# Для пользователей OC Linux/macOS:
python3 manage.py loaddata fixtures/initial_machines.json
```

---

10. **Запустить mock-server:**
```bash
# Для пользователей OC Windows:
python mock_server.py
# Для пользователей OC Linux/macOS:
python3 mock_server.py
```

11. **Запустить polling сервера виртуальными машинами в фоновом режиме:**
```bash
# Необходимо запускать в отдельном терминале Bash!
# Для пользователей OC Windows:
python manage.py run_poller  # [--interval=seconds, --concurrency=number] (опциональные параметры)
# Для пользователей OC Linux/macOS:
python3 manage.py run_poller
```
12. **Запустить веб-сервер Django для мониторинга виртуальных машин:**
```bash
# Необходимо запускать в отдельном терминале Bash!
# Для пользователей OC Windows:
python manage.py runserver
# Для пользователей OC Linux/macOS:
python3 manage.py runserver
```

---

## ▶️ Примеры использования:
> Перед запуском ознакомьтесь с условиями, описанные ниже в [примечании⬇️](#примечание)...
1. **Вывести мониторинговое окно и увидеть метрики по каждой виртуальной машине:**
Вы можете просмотреть результаты работы виртуальных машин при последней итерации опроса по URL-адресу, а также перейти по ссылке на каждую из них и послучить данные в формате JSON. Для этого необходимо выполнить все шаги в разделе 
[💡Как начать пользоваться проектом](#💡как-начать-пользоваться-проектом) и [перейти по URL-адресу в браузере](http://localhost:8000/):
    ```bash
    http://localhost:8000/
    ```
> Или же можно получить эти данные в табличном виде в БД через MySQL, выведя таблицу *monitoring_metric* на экран

2. **Просмотреть зафиксированные перегрузки виртуальных машин:**
Вы можете просмотреть какие виртуальные машины оказались перегружены и по какой причине. ДЛя этого необходимо открыть созданную БД в MySQL и вывести таблицу *monitoring_incident*. Фиксируется также время попадения виртуальной машины в инцидент.

---

### Примечание:
> **В данном руководстве, в качестве примера опрашиваемого URL-адреса был взят самодельный mock-server, работающий в фононом режиме асинхронно.**
Также, для запуска веб-приложения и обработки данных в БД Вам понадобится предварительно развернутый на вашем устройстве MySQL Server.

---

### Стек используемых технологий:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white) ![Aiohttp](https://img.shields.io/badge/aiohttp-%232C5bb4.svg?style=for-the-badge&logo=aiohttp&logoColor=white) ![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black) ![Google Chrome](https://img.shields.io/badge/Google%20Chrome-4285F4?style=for-the-badge&logo=GoogleChrome&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)


> Перечислено в порядке приоритета использования.
