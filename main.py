# Импортируем необходимые классы.
# @literator_by_coding_lover_bot --> ник в тг
import logging
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
BOT_TOKEN = '7677856238:AAEN_kpqzFmjFCmEF30TQ9Lke-Ts4HJLtZs'

A = ['Ещё в полях белеет снег,',
     'А воды уж весной шумят',
     'Бегут и будят сонный брег,',
     'Бегут, и блещут, и гласят…',
     'Они гласят во все концы:',
     '«Весна идёт, весна идёт!»'
     ]


async def start(update, context):
    context.user_data['index'] = 0
    await update.message.reply_text(f'''👋 Привет! Давай прочитаем вместе красивое стихотворение 🌷
Постарайся повторять каждую строчку точно — с большой буквы и знаками препинания.

Начинаем! 🎬
✍️{A[context.user_data['index']]}''')
    context.user_data['index'] += 1
    return 1


async def get_next_string(update, context):
    text = update.message.text
    if text == A[context.user_data['index']]:
        if context.user_data['index'] < len(A) - 1:
            context.user_data['index'] += 1
            await update.message.reply_text(f'''✅ Отлично! Продолжаем:
✍️{A[context.user_data['index']]}''')
            context.user_data['index'] += 1
            if context.user_data['index'] > len(A) - 1:
                await update.message.reply_text('''🎉 Браво! Ты прочитал всё стихотворение до конца!
Хочешь пройти его ещё раз? Напиши 👉 /start
Или отдохни — просто введи 👉 /stop''')
                return 1
        else:
            await update.message.reply_text('''🎉 Браво! Ты прочитал всё стихотворение до конца!
Хочешь пройти его ещё раз? Напиши 👉 /start
Или отдохни — просто введи 👉 /stop''')
            return 1
    else:
        await update.message.reply_text(f'''❌ Ой, нет, не так…
Набери команду /suphler, если нужна подсказка 👀''')


async def stop(update, context):
    await update.message.reply_text('''👋 До встречи! Возвращайся, когда захочешь снова почитать стихи 📚✨ 
Если захочешь продолжить — просто напиши /start.''')
    return ConversationHandler.END


async def suphler(update, context):
    await update.message.reply_text(f'''📝 Подсказка:
✍️{A[context.user_data['index']]}''')


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_next_string),
                CommandHandler('suphler', suphler),
                CommandHandler('stop', stop)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
