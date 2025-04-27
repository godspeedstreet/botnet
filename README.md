# Telegram Bot с товарами / Telegram Bot with Products

## Описание / Description

Этот проект — Telegram-бот для продажи товаров и управления подписками.  
This project is a Telegram bot for selling products and managing subscriptions.

## Возможности / Features

- Главное меню с кнопками / Main menu with buttons
- Просмотр профиля / View profile
- Активация промокода / Promo code activation
- Выбор и оплата подписки / Subscription selection and payment
- Проверка оплаты вручную / Manual payment check

## Установка / Installation

1. Клонируйте репозиторий / Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <project-folder>
   ```

2. Установите зависимости / Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` и добавьте ваш токен бота / Create a `.env` file and add your bot token:
   ```
   BOT_TOKEN=ваш_токен_бота
   ```

## Запуск / Running

```bash
python bot.py
```

## Структура кода / Code Structure

- `bot.py` — основной файл бота / main bot file
  - Клавиатуры (меню) / Keyboards (menus)
  - Обработчики команд и сообщений / Command and message handlers
  - ConversationHandler для промокодов / Promo code ConversationHandler
  - Основная функция запуска / Main run function
- `requirements.txt` — зависимости / dependencies

## Использование / Usage

- `/start` — запуск бота / start the bot
- Кнопки меню для навигации / Use menu buttons for navigation
- Для активации промокода выберите соответствующую кнопку / To activate a promo code, select the corresponding button
