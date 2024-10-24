from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from models import db, Event

# Определяем этапы разговора
TITLE, DATE, TIME, DESCRIPTION = range(4)

# Токен вашего бота
TELEGRAM_TOKEN = '7766662878:AAHskV8pepErFRc5nFV8RqvQROWR6TCKmME'

# Команда /start
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я бот для управления расписанием. Используйте команду /add для добавления события."
    )

# Команда /add
async def add_event(update: Update, context: CallbackContext):
    await update.message.reply_text("Введите название события:")
    return TITLE

# Получение названия события
async def get_title(update: Update, context: CallbackContext):
    context.user_data['title'] = update.message.text  # Сохраняем название в user_data
    await update.message.reply_text("Введите дату (ГГГГ-ММ-ДД):")
    return DATE

# Получение даты события
async def get_date(update: Update, context: CallbackContext):
    context.user_data['date'] = update.message.text  # Сохраняем дату в user_data
    await update.message.reply_text("Введите время (ЧЧ:ММ):")
    return TIME

# Получение времени события
async def get_time(update: Update, context: CallbackContext):
    context.user_data['time'] = update.message.text  # Сохраняем время в user_data
    await update.message.reply_text("Введите описание (необязательно):")
    return DESCRIPTION

# Получение описания события и сохранение в базе данных
async def get_description(update: Update, context: CallbackContext):
    context.user_data['description'] = update.message.text  # Сохраняем описание
    event = Event(
        title=context.user_data['title'],
        date=context.user_data['date'],
        time=context.user_data['time'],
        description=context.user_data['description']
    )
    db.session.add(event)
    db.session.commit()
    await update.message.reply_text("Событие добавлено!")
    return ConversationHandler.END

# Настройка обработчиков
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add_event)],
    states={
        TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
        DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
        TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
        DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_description)],
    },
    fallbacks=[],
)

# Запуск бота
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
application.add_handler(CommandHandler('start', start))
application.add_handler(conv_handler)

application.run_polling()

