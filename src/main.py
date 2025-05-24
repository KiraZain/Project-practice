import telebot
from telebot import types
from currency_converter import CurrencyConverter
from datetime import datetime


API_TOKEN = '7774198724:AAF6-wR17afOMUiFNojHLqCtlJkZMB2jC3M'

bot = telebot.TeleBot(API_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):

    markup = types.ReplyKeyboardMarkup()
    markup.add('Курсы валют', 'Бюджет', 'Напоминания о платежах', 'Расчет кредитования')

    bot.send_photo(
        chat_id=message.chat.id,
        photo=open('logo.png', 'rb'),
        caption="Добро пожаловать в ваш личный финансовый помощник!\n\n"
                "Я помогу вам быстро перевести нужные валюты, сформировать бюджет, "
                "напомню о предстоящих платежах и рассчитаю процентную ставку кредита.\n\n"
                "Выберите услугу:",
        reply_markup=markup
    )

# Обработчик для кнопки "Курсы валют"
amount = 0
currency = CurrencyConverter()

@bot.message_handler(func=lambda message: message.text == 'Курсы валют')
def currency_rates(message):
    bot.reply_to(message, "Введите сумму")
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    if message.text.strip() == "Главное меню":
        send_welcome(message)
        return

    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Впишите сумму')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        btn1 = types.KeyboardButton('USD/EUR')
        btn2 = types.KeyboardButton('EUR/USD')
        btn3 = types.KeyboardButton('USD/GBP')
        btn4 = types.KeyboardButton('Другое значение')
        btn_main_menu = types.KeyboardButton('Главное меню')
        markup.add(btn1, btn2, btn3, btn4, btn_main_menu)
        bot.send_message(message.chat.id, 'Выберите пару валют:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Сумма должна быть больше 0. Впишите сумму')
        bot.register_next_step_handler(message, summa)

@bot.message_handler(func=lambda message: message.text in ['USD/EUR', 'EUR/USD', 'USD/GBP', 'Другое значение'])
def handle_currency_selection(message):
    if message.text == "Главное меню":
        send_welcome(message)
        return

    if message.text != "Другое значение":
        values = message.text.split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново ввести сумму')
        bot.register_next_step_handler(message, summa)
    else:
        bot.send_message(message.chat.id, 'Введите пару значений через слэш')
        bot.register_next_step_handler(message, mycurrency)

def mycurrency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново ввести сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так. Впишите сумму')
        bot.register_next_step_handler(message, summa)


# Обработчик для кнопки "Расчет кредитования"

@bot.message_handler(func=lambda message: message.text == 'Расчет кредитования')
def loan_interest(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_annuity = types.KeyboardButton('Аннуитетный платеж')
    btn_differentiated = types.KeyboardButton('Дифференцированный платеж')
    btn_main_menu = types.KeyboardButton('Главное меню')
    markup.add(btn_annuity, btn_differentiated, btn_main_menu)

    bot.send_message(message.chat.id, "Выберите тип кредитования:", reply_markup=markup)

# Обработчик для аннуитетного платежа
@bot.message_handler(func=lambda message: message.text == 'Аннуитетный платеж')
def calculate_annuity(message):
    bot.send_message(message.chat.id,
                     "Введите начальную сумму, процентную ставку и количество лет через запятую, например: 100000,5,10")
    bot.register_next_step_handler(message, process_annuity)

def process_annuity(message):
    try:
        loan_parts = message.text.split(',')
        if len(loan_parts) != 3:
            raise ValueError(
                "Неверный формат. Пожалуйста, введите начальную сумму, процентную ставку и количество лет через запятую.")

        principal, interest_rate, years = loan_parts
        principal = float(principal.strip())
        interest_rate = float(interest_rate.strip()) / 100
        years = int(years.strip())

        monthly_interest_rate = interest_rate / 12
        number_of_payments = years * 12

        annuity_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / (
                (1 + monthly_interest_rate) ** number_of_payments - 1)
        total_payment = annuity_payment * number_of_payments
        overpayment = total_payment - principal

        bot.send_message(message.chat.id,
                         f"Ежемесячный аннуитетный платеж: {annuity_payment:.2f}\n"
                         f"Общая сумма выплат: {total_payment:.2f}\n"
                         f"Переплата: {overpayment:.2f}")
    except ValueError as e:
        bot.send_message(message.chat.id, str(e))
        bot.register_next_step_handler(message, process_annuity)

# Обработчик для дифференцированного платежа
@bot.message_handler(func=lambda message: message.text == 'Дифференцированный платеж')
def calculate_differentiated(message):
    bot.send_message(message.chat.id,
                     "Введите начальную сумму, процентную ставку и количество лет через запятую, например: 100000,5,10")
    bot.register_next_step_handler(message, process_differentiated)

def process_differentiated(message):
    try:
        loan_parts = message.text.split(',')
        if len(loan_parts) != 3:
            raise ValueError(
                "Неверный формат. Пожалуйста, введите начальную сумму, процентную ставку и количество лет через запятую.")

        principal, interest_rate, years = loan_parts
        principal = float(principal.strip())
        interest_rate = float(interest_rate.strip()) / 100
        years = int(years.strip())

        number_of_payments = years * 12
        fixed_payment = principal / number_of_payments

        total_payment = 0
        first_payment = 0
        last_payment = 0

        for month in range(1, number_of_payments + 1):
            remaining_principal = principal - fixed_payment * (month - 1)
            monthly_interest = remaining_principal * interest_rate / 12
            monthly_payment = fixed_payment + monthly_interest

            if month == 1:
                first_payment = monthly_payment
            if month == number_of_payments:
                last_payment = monthly_payment

            total_payment += monthly_payment

        overpayment = total_payment - principal

        bot.send_message(message.chat.id,
                         f"Первый платеж: {first_payment:.2f}\n"
                         f"Последний платеж: {last_payment:.2f}\n"
                         f"Общая сумма выплат: {total_payment:.2f}\n"
                         f"Переплата: {overpayment:.2f}")
    except ValueError as e:
        bot.send_message(message.chat.id, str(e))
        bot.register_next_step_handler(message, process_differentiated)

@bot.message_handler(func=lambda message: message.text == 'Главное меню')
def main_menu(message):
    send_welcome(message)


# Обработчик для кнопки "Напоминания о платежах"
payments = []

@bot.message_handler(func=lambda message: message.text == 'Напоминания о платежах')
def reminders(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_add_payment = types.KeyboardButton('Добавить платеж')
    btn_view_payments = types.KeyboardButton('Просмотреть платежи')
    btn_main_menu = types.KeyboardButton('Главное меню')
    markup.add(btn_add_payment, btn_view_payments, btn_main_menu)

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Обработчик для добавления платежа
@bot.message_handler(func=lambda message: message.text == 'Добавить платеж')
def add_payment(message):
    bot.send_message(message.chat.id,
                     "Введите дату платежа (дд.мм.гггг) и описание с суммой через запятую, например: 10.10.2024, Интернет - 1200")
    bot.register_next_step_handler(message, process_payment)

def process_payment(message):
    if message.text.strip() == "Главное меню":
        send_welcome(message)
        return

    try:
        date, description = message.text.split(',', 1)
        date = date.strip()
        description = description.strip()

        datetime.strptime(date, "%d.%m.%Y")

        payments.append({"date": date, "description": description})
        bot.send_message(message.chat.id, "Платеж успешно добавлен!")
    except ValueError:
        bot.send_message(message.chat.id,
                         "Неверный формат. Пожалуйста, введите данные в формате: дд.мм.гггг, описание - сумма")
        bot.register_next_step_handler(message, process_payment)

# Обработчик для просмотра платежей
@bot.message_handler(func=lambda message: message.text == 'Просмотреть платежи')
def view_payments(message):
    if message.text.strip() == "Главное меню":
        send_welcome(message)
        return

    if not payments:
        bot.send_message(message.chat.id, "Список платежей пуст.")
    else:
        response = "Ваши платежи:\n"
        for payment in payments:
            response += f"{payment['date']}: {payment['description']}\n"
        bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == 'Главное меню')
def main_menu(message):
    send_welcome(message)


# Обработчик для кнопки "Бюджет"
income = {}
expenses = {}

@bot.message_handler(func=lambda message: message.text == 'Бюджет')
def budget(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_add_income = types.KeyboardButton('Добавить доход')
    btn_add_expense = types.KeyboardButton('Добавить расход')
    btn_view_budget = types.KeyboardButton('Просмотреть бюджет')
    btn_reset_budget = types.KeyboardButton('Сбросить бюджет')
    btn_main_menu = types.KeyboardButton('Главное меню')
    markup.add(btn_add_income, btn_add_expense, btn_view_budget, btn_reset_budget, btn_main_menu)

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Обработчик для добавления дохода
@bot.message_handler(func=lambda message: message.text == 'Добавить доход')
def add_income(message):
    bot.send_message(message.chat.id, "Введите сумму дохода и категорию через запятую, например: 5000, Зарплата")
    bot.register_next_step_handler(message, process_income)

def process_income(message):
    if message.text.strip() == "Главное меню":
        send_welcome(message)
        return

    try:
        amount, category = message.text.split(',', 1)
        amount = float(amount.strip())
        category = category.strip()

        if category in income:
            income[category] += amount
        else:
            income[category] = amount

        bot.send_message(message.chat.id, "Доход успешно добавлен!")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Пожалуйста, введите данные в формате: сумма, категория")
        bot.register_next_step_handler(message, process_income)

# Обработчик для добавления расхода
@bot.message_handler(func=lambda message: message.text == 'Добавить расход')
def add_expense(message):
    bot.send_message(message.chat.id, "Введите сумму расхода и категорию через запятую, например: 2000, Продукты")
    bot.register_next_step_handler(message, process_expense)

def process_expense(message):
    if message.text.strip() == "Главное меню":
        send_welcome(message)
        return

    try:
        amount, category = message.text.split(',', 1)
        amount = float(amount.strip())
        category = category.strip()

        if category in expenses:
            expenses[category] += amount
        else:
            expenses[category] = amount

        bot.send_message(message.chat.id, "Расход успешно добавлен!")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Пожалуйста, введите данные в формате: сумма, категория")
        bot.register_next_step_handler(message, process_expense)

# Обработчик для просмотра бюджета
@bot.message_handler(func=lambda message: message.text == 'Просмотреть бюджет')
def view_budget(message):
    if message.text.strip() == "Главное меню":
        send_welcome(message)
        return

    total_income = sum(income.values())
    total_expenses = sum(expenses.values())
    balance = total_income - total_expenses

    response = "Ваш бюджет:\n"
    response += f"Общий доход: {total_income:.2f}\n"
    response += f"Общий расход: {total_expenses:.2f}\n"
    response += f"Баланс: {balance:.2f}\n\n"

    response += "Доходы:\n"
    for category, amount in income.items():
        response += f"{category}: {amount:.2f}\n"

    response += "\nРасходы:\n"
    for category, amount in expenses.items():
        response += f"{category}: {amount:.2f}\n"

    bot.send_message(message.chat.id, response)

# Обработчик для сброса бюджета
@bot.message_handler(func=lambda message: message.text == 'Сбросить бюджет')
def reset_budget(message):
    if message.text.strip() == "Главное меню":
        send_welcome(message)
        return

    global income, expenses
    income = {}
    expenses = {}
    bot.send_message(message.chat.id, "Бюджет сброшен!")


if __name__ == "__main__":
    bot.polling(none_stop=True)
