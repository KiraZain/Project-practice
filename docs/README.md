# ﻿**Вариативная часть**

# **Разработка Telegram-бота Финансовый помощник**

**Задачи, которые необходимо выполнить в ходе работы:**

- Изучить различные типы ботов, их классификацию и ключевые компоненты архитектуры. 
- Проанализировать, какие боты в данной среде уже существуют и активно используются.
- Изучить создание Telegram-ботов, архитектуру построения кода для их написания
- Сопоставить всю полученную информацию, на основе анализа расписать функции бота и выполнить пути реализации

**Изучение типов ботов, использующихся на рынке.**

Существует множество типов ботов, каждый из которых имеет свои уникальные функции и возможности. В процессе изучения я выделила несколько наиболее популярных типов:
### Информационные боты. Информационные боты предназначены для предоставления пользователям актуальной информации и новостей. Они могут охватывать различные темы, такие как политика, экономика, спорт, технологии и многое другое.
- ### Развлекательные боты. Эти боты созданы для того, чтобы развлекать пользователей и предоставлять им способы расслабления и отдыха.
- ### Образовательные боты. Образовательные боты помогают пользователям в обучении и развитии новых навыков.
- ### Торговые боты. Торговые боты облегчают процесс покупки и продажи товаров и услуг.
- ### Финансовые боты. Финансовые боты предназначены для управления личными финансами и получения информации о финансовых рынках.

- ### Поддержка и обслуживание клиентов. Эти боты используются компаниями для улучшения взаимодействия с клиентами.
  ### Однако в моём случае особое внимание привлекли финансовые боты. Они предназначены для того, чтобы помогать в управлении личными финансами, отслеживании расходов, составлении бюджета и планировании накоплений. Это всегда было актуальным и действительно способно упростить жизнь.
  Анализ существующих экономических ботов.

  |Money Lover|Бот для управления личными финансами и бюджетом.|Отслеживание расходов, планирование бюджета, напоминания.|
  | :- | :- | :- |
  |CoinMarketCap Bot|Бот для отслеживания криптовалют и финансовых рынков.|Котировки криптовалют, новости рынка, оповещения о ценах.|
  |Splitwise Bot|Бот для разделения расходов между друзьями или коллегами.|Создание групп, отслеживание долгов, уведомления о платежах.|
  |Personal Finances|Бот для учета личных финансов и планирования бюджета.|Управление доходами и расходами, создание отчетов.|
  |Expense Manager|Бот для учета ежедневных расходов и финансового планирования.|Ведение записей о расходах, создание бюджетов, напоминания.|
  |Cryptocurrency Bot|Бот для отслеживания и анализа криптовалютных рынков.|Графики цен, новости, прогнозы, уведомления о рыночных изменениях.|

  **Создание Telegram-ботов, архитектура построения кода.**

  Основные шаги в создании Telegram-бота

  Регистрация бота: для начала необходимо создать бота в Telegram. Это делается с помощью официального бота Telegram — BotFather. После создания бот получает уникальный токен, который используется для взаимодействия с Telegram API.

  Выбор платформы и языка программирования: Telegram-боты могут быть разработаны на различных языках программирования. Наиболее популярные — Python, JavaScript, PHP, Java и другие.

  Настройка окружения: установка необходимых библиотек и зависимостей. Например, для Python часто используют библиотеку python-telegram-bot.

  Настройте сервер или используйте облачные платформы, такие как Heroku или AWS, для развертывания бота.

  Тестирование и отладка: 

  Проверка работы бота в различных сценариях. Исправление ошибок и оптимизация кода для улучшения производительности.

  Архитектура построения кода

  Архитектура Telegram-бота может варьироваться в зависимости от сложности и функционала. Однако основные компоненты остаются неизменными:

- Основной модуль: точка входа в приложение, где происходит инициализация бота и настройка параметров.
- Обработчики (Handlers): обработчики используются для управления различными типами входящих сообщений и команд.
- Логика обработки: здесь реализуются основные функции бота. Например, вычисления, взаимодействие с базами данных или сторонними API.
- Взаимодействие с API: бот может взаимодействовать с различными API для получения данных или выполнения действий (например, получение курсов валют).

**Написание кода**

Здесь показана инструкция реализации Telegram-бота, который предоставляет пользователю несколько функций для управления финансами: конвертацию валют, расчет кредитов, бюджетирование и напоминания о платежах. Он использует библиотеку pyTelegramBotAPI для взаимодействия с Telegram API.

**1.  Создайте бота в Telegram:**

Найдите в Telegram бота BotFather.

Используйте команду /newbot и следуйте инструкциям для создания нового бота.

После завершения процесса BotFather предоставит вам API-токен. Он должен быть вставлен в ваш код вместо API\_TOKEN.

![](Aspose.Words.1d81671e-0556-4098-b8de-65ad877a3cbc.001.png)

**2. Подготовьте необходимые файлы:**

Убедитесь, что у вас есть файл logo.png, который будет отправляться пользователям в приветственном сообщении.

**3. Импортируйте необходимые библиотеки :**

python

import telebot

from telebot import types

from currency\_converter import CurrencyConverter

from datetime import datetime

telebot и types: Библиотека для создания Telegram-ботов.

CurrencyConverter: используется для конвертации валют.

datetime: Для работы с датами (например, для напоминаний).

**4. Настройте API-токен и создайте объекта бота:**

python

API\_TOKEN = 'YOUR\_API\_TOKEN\_HERE'

bot = telebot.TeleBot(API\_TOKEN)

API\_TOKEN должен быть заменен на ваш токен, полученный от BotFather.

Создание экземпляра TeleBot для управления ботом.

![](Aspose.Words.1d81671e-0556-4098-b8de-65ad877a3cbc.002.png)

**5. Обработчик команды /start:**

@bot.message\_handler(commands=['start'])

def send\_welcome(message):

`    `markup = types.ReplyKeyboardMarkup()

`    `markup.add('Курсы валют', 'Бюджет', 'Напоминания о платежах', 'Расчет кредитования')

`    `bot.send\_photo(

`        `chat\_id=message.chat.id,

`        `photo=open('logo.png', 'rb'),

`        `caption="Добро пожаловать в ваш личный финансовый помощник!

`    `reply\_markup=markup\
)

Создает клавиатуру с кнопками для различных функций.

Отправляет приветственное сообщение с изображением (файл logo.png).

**6. Настройте конвертацию валют используя библиотеку CurrencyConverter :**

python

amount = 0

currency = CurrencyConverter()

@bot.message\_handler(func=lambda message: message.text == 'Курсы валют')

**def** currency\_rates(message):

`    `bot.reply\_to(message, "Введите сумму")

`    `bot.register\_next\_step\_handler(message, summa)

**def** mycurrency(message):\
`    `try:\
`        `values = message.text.upper().split('/')\
`        `res = currency.convert(amount, values[0], values[1])\
`        `bot.send\_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново ввести сумму')\
`        `bot.register\_next\_step\_handler(message, summa)\
`    `except Exception:\
`        `bot.send\_message(message.chat.id, 'Что-то не так. Впишите сумму')\
`        `bot.register\_next\_step\_handler(message, summa)

Запрашивает у пользователя сумму для конвертации.

Обрабатывает ввод и предлагает выбрать пару валют.

**7. Расчет кредитования:**

python

@bot.message\_handler(func=lambda message: message.text == 'Расчет кредитования')

**def** loan\_interest(message):

`    `markup = types.ReplyKeyboardMarkup(row\_width=1, resize\_keyboard=True)

`    `btn\_annuity = types.KeyboardButton('Аннуитетный платеж')

`    `btn\_differentiated = types.KeyboardButton('Дифференцированный платеж')

`    `markup.add(btn\_annuity, btn\_differentiated)

`    `bot.send\_message(message.chat.id, "Выберите тип кредитования:", reply\_markup=markup)

@bot.message\_handler(func=lambda message: message.text == 'Аннуитетный платеж')

**def** calculate\_annuity(message):

...

Предлагает выбрать тип платежа (аннуитетный или дифференцированный).

Выполняет расчет на основе пользовательского ввода (пример вычисления аннуитетного платежа).

principal, interest\_rate, years = loan\_parts\
principal = float(principal.strip())\
interest\_rate = float(interest\_rate.strip()) / 100\
years = int(years.strip())\
\
monthly\_interest\_rate = interest\_rate / 12\
number\_of\_payments = years \* 12\
\
annuity\_payment = principal \* (monthly\_interest\_rate \* (1 + monthly\_interest\_rate) \*\* number\_of\_payments) / (\
`        `(1 + monthly\_interest\_rate) \*\* number\_of\_payments - 1)\
total\_payment = annuity\_payment \* number\_of\_payments\
overpayment = total\_payment - principal

**8. Напоминания о платежах:**

@bot.message\_handler(func=lambda message: message.text == 'Напоминания о платежах')

**def** reminders(message):

`    `markup = types.ReplyKeyboardMarkup(row\_width=1, resize\_keyboard=True)

`    `btn\_add\_payment = types.KeyboardButton('Добавить платеж')

`    `btn\_view\_payments = types.KeyboardButton('Просмотреть платежи')

`    `markup.add(btn\_add\_payment, btn\_view\_payments)

`    `bot.send\_message(message.chat.id, "Выберите действие:", reply\_markup=markup)

@bot.message\_handler(func=lambda message: message.text == 'Добавить платеж')

**def** add\_payment(message):

...

Позволяет добавлять и просматривать запланированные платежи.

**Пример кода по просмотру платежа c помощью списка:**

@bot.message\_handler(func=lambda message: message.text == 'Просмотреть платежи')\
def view\_payments(message):\
`    `if message.text.strip() == "Главное меню":\
`        `send\_welcome(message)\
`        `return\
\
`    `if not payments:\
`        `bot.send\_message(message.chat.id, "Список платежей пуст.")\
`    `else:\
`        `response = "Ваши платежи:\n"\
`        `for payment in payments:\
`            `response += f"{payment['date']}: {payment['description']}\n"\
`        `bot.send\_message(message.chat.id, response)

**9. Управление бюджетом:**

@bot.message\_handler(func=lambda message: message.text == 'Бюджет')

**def** budget(message):

`    `markup = types.ReplyKeyboardMarkup(row\_width=1, resize\_keyboard=True)

`    `btn\_add\_income = types.KeyboardButton('Добавить доход')

`    `btn\_add\_expense = types.KeyboardButton('Добавить расход')

`    `btn\_view\_budget = types.KeyboardButton('Просмотреть бюджет')

`    `btn\_reset\_budget = types.KeyboardButton('Сбросить бюджет')

`    `markup.add(btn\_add\_income, btn\_add\_expense, btn\_view\_budget, btn\_reset\_budget)

`    `bot.send\_message(message.chat.id, "Выберите действие:", reply\_markup=markup)

@bot.message\_handler(func=lambda message: message.text == 'Добавить доход')

**def** add\_income(message):

...

Управляет добавлением доходов и расходов, а также просмотром и сбросом бюджета.

Использует словари income и expenses для хранения данных:

@bot.message\_handler(func=lambda message: message.text == 'Добавить доход')\
def add\_income(message):\
`    `bot.send\_message(message.chat.id, "Введите сумму дохода и категорию через запятую, например: 5000, Зарплата")\
`    `bot.register\_next\_step\_handler(message, process\_income)\
\
def process\_income(message):\
`    `if message.text.strip() == "Главное меню":\
`        `send\_welcome(message)\
`        `return\
\
`    `try:\
`        `amount, category = message.text.split(',', 1)\
`        `amount = float(amount.strip())\
`        `category = category.strip()\
\
`        `if category in income:\
`            `income[category] += amount\
`        `else:\
`            `income[category] = amount\
\
`        `bot.send\_message(message.chat.id, "Доход успешно добавлен!")\
`    `except ValueError:\
`        `bot.send\_message(message.chat.id, "Неверный формат. Пожалуйста, введите данные в формате: сумма, категория")\
`        `bot.register\_next\_step\_handler(message, process\_income)

**10. Запустите бота:**

python

if \_\_name\_\_ == "\_\_main\_\_":

`    `bot.polling(none\_stop=True)

Запускает бота в режиме постоянного опроса, чтобы он мог обрабатывать входящие сообщения.

Этот код создает многофункционального бота, который может помочь пользователям управлять своими финансами. Каждый раздел кода отвечает за конкретную функциональность бота, от обработки команд и сообщений до выполнения вычислений и взаимодействия с пользователем.

![](Aspose.Words.1d81671e-0556-4098-b8de-65ad877a3cbc.003.png)
