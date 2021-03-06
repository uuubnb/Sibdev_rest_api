README
=====================

Этот README документирует и описывает все шаги, необходимые для создания и запуска веб-приложения.


### Задание 1: Рабочее окружение

##### Начнем с рабочего окружения: репозитория, среды разработки и запуска локального сервера. 

Разрабатывать код будем в локальном репозитории, а загружать результаты — в удаленный. Там их будет проверять наставник. Договоримся: при каждой отправке merge request будем указывать номер задания и описывать выполненную работу в описании.
У нас будет стаб — заготовка приложения. С ней и будем работать.

##### Ход работы:

* Склонировать репозиторий проекта себе в рабочую папку.
* В репозитории ответвиться от ветки `master` и создать ветку `feature/#1`.
* Скачать и настроить [PyCharm](https://www.jetbrains.com/pycharm/) по [инструкции](https://docs.google.com/document/d/13G_jjdX4nLDUtsrl7vB2l6YQUNFWFhW0Oi_2yanylXY/).
* Запустить локальный сервер. Как это сделать — описано в Readme стаба.
* Отправить merge request в `master` наставнику.


### Задание 2: Первое Django-приложение

##### Прежде чем приступить к разработке нашего приложения, потренируемся на отвлеченном примере.

У нас заготовлено небольшое тренировочное приложение: `/server/apps/test`.
Оно работает с 2 строками. Для приложения есть API, который позволяет выполнять запросы: GET, POST, PUT, PATCH, DELETE.

Приложение работает на Django Rest Framework (далее — DRF). Мы будем разбираться с этим фреймворком на протяжении всей практики.

Для приложения есть 3 теста, которые оно не проходит. Вот почему:
1) Должно быть можно выполнять только запросы GET, POST;
2) 2-я строка должна генерироваться автоматически;
3) Через POST должно быть достаточно передавать только 1 строку.

В ходе этого задания удовлетворим тесты. Немного теории о каждом.

1) В DRF за применимость методов API отвечают viewsets. Наш `TestViewSet` содержит мало кода и наследует `ModelViewSet`. `ModelViewSet` наследует много миксинов и `GenericViewSet`. Чтобы разрешить только методы GET и POST, нужно как-то изменить наследование `TestViewSet`.

2) С автоматической генерацией помогают `signals`. Сейчас нужный `signal` не срабатывает, как надо. Чтобы срабатывал — нужно немного изменить логику.

3) Чтобы POST принимал только 1 строку — это к `serializer`. У него есть `class Meta`, в котором заданы модель `Test` и параметр `fields = ‘__all__’`. То есть, этот `serializer` работает со всеми полями Test. Параметр можно изменить: `fields = (‘name’, )`. Но тогда GET не вернет второе поле. Поможет следующая строка: `extra_kwargs = {'random_string': {'read_only': True}}`. 

Разобравшись с этим заданием, мы поймем основы DRF и приступим к разработке нашего основного приложения.


### Задание 3: Авторизация и регистрация

##### Теперь мы знаем, что к чему. Перейдем к разработке основного приложения.

У нас будет 2 вида пользователей: обычные пользователи и владельцы заведений. 
Обычные пользователи — неавторизованные — могут только просматривать заведения. 
Владельцы заведений — авторизованные — могут еще и управлять своими. 
С регистрации и авторизации мы и начнем.

К счастью, у нас есть DRF. А у DRF есть почти готовое решение нашей задачи. Наша модель пользователя содержит 2 поля: логин, пароль. В ходе задания мы настроим авторизацию по токену. Далее создадим приложение users. В нем настроим serializer и viewset для модели пользователя. Ограничим методы API только методом POST. Настроим роутинг.


### Задание 4: Модель заведения

Теперь у нас есть пользователи.
У пользователей есть заведения. Каждое заведение обладает набором свойств. 
Значения одних задает пользователь, другие — рассчитываются автоматически.

Задаются пользователем:
* название заведения,
* фотография заведения,
* режим работы в часах «с» и «до»,
* адрес заведения.
Рассчитываются автоматически:
* средняя стоимость блюд;
* координаты заведения,
* владелец (тот, кто добавил заведение).
Для средней стоимости блюд пока сделаем заглушку. Расчет сделаем, когда будет модель блюда.


### Задание 5: Модели блюда и ингридиента

Мы сделали модель заведения. Но отложили расчет средней стоимости блюд. Для этого нужна модель блюда. Моделями блюда и ингредиента мы сейчас и займемся.
У заведения есть блюда. Блюда состоят из ингредиентов. Мы уже умеем создавать модели. Так что, как говорится, cut the crap: прикинем свойства — и приступим.

Блюдо:
* название,
* фотография,
* суммарная калорийность (считается автоматически),
* цена,
* массив ингредиентов.

Ингредиент:
* название,
* калорийность.


### Задание 6: Права доступа

Итак, у нас 4 сущности: пользователь, заведение, блюдо, ингредиент. Только авторизованный пользователь может создавать заведения, блюда. Редактировать заведение может только его создатель. Добавлять и редактировать блюда заведения может только создатель заведения. Просматривать заведения с их блюдами могут все. 
В ходе этого задания мы реализуем все эти ограничения.


### Задание 7: Документирование кода

Итак, мы разработали бэкенд. Мы молодцы!
Представим: мы отложили проект в папку «Важные достижения в моей жизни». Но спустя год решили его передать коллеге или доработать сами. Придется потратить время, чтобы разобраться в коде. Причем не только коллеге, но и нам — чтобы вспомнить всё спустя год. Можно облегчить эту боль: заранее сделать
документацию. 

Есть сервисы, которые автоматически документируют код. Например, Swagger. Его и интегрируем в проект. Он сгенерирует документацию, а мы ее доработаем.


### Задание 8: Покрытие тестами

Кроме документации нам понадобятся тесты. Они позволяют убедиться, что все части веб-приложения ведут себя так, как ожидалось. Это обеспечивает безопасность при доработках, рефакторинге и командной работе.
Есть 3 типа тестов. Юнит-тесты проверяют отдельный модуль приложения.

Интеграционные — модули в связке. E2E-тесты — всё приложение с точки зрения пользователя. 
Мы покроем юнит-тестами несколько запросов.


### Задание 9: Кеширование

##### В этом задании научимся кешировать данные.
Кеширование нужно в высоконагруженных сервисах. В таких сервисах много запросов к базе данных, что перегружает ее. Чтобы не допускать этого, разработчики используют кеширование. Тогда часто запрашиваемая информация временно хранится и отдается не из БД, а из кеша. Кеш — как бы посредник между БД и клиентом.

Чтобы настроить кеширование, воспользуемся сервисом Redis.


### Задание 10: Настройка веб-сервера

Сейчас API возвращает текстовые данные, а также статические и медиа-объекты. В реальных проектах, возвращать статику и медиа — работа веб-сервера. Веб-сервер справляется с этим быстрее.

Воспользуемся веб-сервером Nginx. Установим и настроим его так, чтобы он возвращал статику и медиа. Остальные запросы пусть обрабатывает Django. В директории Nginx уже есть файл nginx.conf, он имеет минимальную настройку, которая позволяет получать коды состояния от сервера.

