from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, ConversationHandler
import os
from dotenv import load_dotenv

load_dotenv()

# Список действующих промокодов
VALID_PROMO_CODES = ["TEST2024", "SPRING2024", "BOTNET50"]

# Состояния для ConversationHandler
ENTER_PROMO = 1

# кнопки главного меню
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("BOTNETSN0S (СН0С)", callback_data="botnetsn0s")],
        [InlineKeyboardButton("👤Мой профиль", callback_data="profile")],
        [InlineKeyboardButton("📌Канал", url="https://t.me/+RcVhLGySh7s0Y2Qy")],
        [InlineKeyboardButton("📟Мануал", url="https://telegra.ph/SNOSER-FAQ-02-25")],
        [InlineKeyboardButton("🔑Активировать промокод", callback_data="promo")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_subscription_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎁1 МЕСЯЦ - 650Р/6.5$", callback_data="sub_1month")],
        [InlineKeyboardButton("📘3 МЕСЯЦА - 1200Р/12$", callback_data="sub_3month")],
        [InlineKeyboardButton("🔏НАВСЕГДА - 2800Р/28$", callback_data="sub_forever")],
        [InlineKeyboardButton("🔑СКРИПТЫ + ОБУЧЕНИЕ + ХОСТ - 1200Р/12$", callback_data="sub_scripts")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_payment_keyboard():
    keyboard = [
        [InlineKeyboardButton("💳CARD/КАРТА", callback_data="pay_card")],
        [InlineKeyboardButton("💳Я оплатил/оплатила", callback_data="payment_done")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_to_subs")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_payment_details_keyboard():
    keyboard = [
        [InlineKeyboardButton("💳Я оплатил/оплатила", callback_data="payment_done")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_to_payment")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_cancel_keyboard():
    keyboard = [
        [InlineKeyboardButton("❌ Отмена", callback_data="cancel_promo")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать!",
        reply_markup=get_main_keyboard()
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "botnetsn0s":
        await query.message.edit_text(
            "❌ У вас нет активной подписки. Пожалуйста, приобретите подписку:\n\n"
            "📱Выбираете тариф подписки на функционал бота:",
            reply_markup=get_subscription_keyboard()
        )
    
    elif query.data.startswith("sub_"):
        if query.data == "sub_1month":
            price = "650"
        elif query.data == "sub_3month":
            price = "1200"
        elif query.data == "sub_forever":
            price = "2800"
        elif query.data == "sub_scripts":
            price = "1200"
        
        context.user_data['selected_price'] = price
        await query.message.edit_text(
            "📲Выберите удобный способ оплаты:",
            reply_markup=get_payment_keyboard()
        )
    
    elif query.data == "pay_card":
        price = context.user_data.get('selected_price', '650')  # Default to 650 if not set
        await query.message.edit_text(
            f"🖥Реквизиты для оплаты:\n"
            f"📲Номер карты:\n\n"
            f"2200030550254883\n\n"
            f"📟Банк: ПСБ\n"
            f"🔋Сумма: {price} RUB",
            reply_markup=get_payment_details_keyboard()
        )
    
    elif query.data == "payment_done":
        await query.message.edit_text(
            "💳Если вы действительно оплатили данную услугу - отправьте чек об оплате\n\n"
            "-📲📲 @SN0SADMIN_BOT\n\n"
            "💎Ваш Id - будет добавлен в админку бота через БД после проверки платежа - "
            "🛡Время ожидания - максимум 3 часа.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main")]])
        )
    
    elif query.data == "profile":
        await query.message.edit_text(
            f"👤 Твой профиль:\n\n"
            f"👤 Твой юзернейм: @{update.effective_user.username}\n"
            f"🆔 ID: {update.effective_user.id}\n\n"
            f"❌ Подписки нет",
            reply_markup=get_main_keyboard()
        )
    
    elif query.data == "promo":
        await query.message.edit_text(
            "🔑 Введите промокод:",
            reply_markup=get_cancel_keyboard()
        )
        return ENTER_PROMO
    
    elif query.data == "cancel_promo":
        await query.message.edit_text(
            "❌ Активация промокода отменена",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END
    
    # Handle back buttons
    elif query.data == "back_to_main":
        await query.message.edit_text(
            "Главное меню",
            reply_markup=get_main_keyboard()
        )
    
    elif query.data == "back_to_subs":
        await query.message.edit_text(
            "❌ У вас нет активной подписки. Пожалуйста, приобретите подписку:\n\n"
            "📱Выбираете тариф подписки на функционал бота:",
            reply_markup=get_subscription_keyboard()
        )
    
    elif query.data == "back_to_payment":
        await query.message.edit_text(
            "📲Выберите удобный способ оплаты:",
            reply_markup=get_payment_keyboard()
        )

async def handle_promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    promo_code = update.message.text.strip().upper()
    
    if promo_code in VALID_PROMO_CODES:
        await update.message.reply_text(
            "✅ Промокод успешно активирован!",
            reply_markup=get_main_keyboard()
        )
    else:
        await update.message.reply_text(
            "❌ Такого промокода не существует",
            reply_markup=get_main_keyboard()
        )
    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

def main():
    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    # Создаем ConversationHandler для обработки промокодов
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="^promo$")],
        states={
            ENTER_PROMO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_promo)],
        },
        fallbacks=[CallbackQueryHandler(button_callback, pattern="^cancel_promo$")],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main() 