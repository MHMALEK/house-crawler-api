# import logging
# from telegram import Update
# from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext
# from ..database import db





# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     await context.bot.send_message(chat_id=chat_id, text="Welcome! You can turn on reminders with /set_reminder command. We will send you about all available houses every day on this bot")
   

# async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     user = User.query.filter_by(chat_id=str(chat_id)).first()
#     if user is None:
#         new_user = User(chat_id=str(chat_id))
#         db.session.add(new_user)
#         db.session.commit()
#         await context.bot.send_message(chat_id=chat_id, text="You're now registered. You will receive reminders every day at 9:00 AM. You can turn off reminders with /unset_reminder command.")
#     else:
#         await context.bot.send_message(chat_id=chat_id, text="You're already registered!  You can turn off reminders with /unset_reminder command.")

# async def unset_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     user = User.query.filter_by(chat_id=str(chat_id)).first()
#     if user is not None:
#         db.session.delete(user)
#         db.session.commit()
#         await context.bot.send_message(chat_id=chat_id, text="You're now unregistered. You will not receive reminders anymore. You can turn on reminders with /set_reminder command.")
#     else: 
#         await context.bot.send_message(chat_id=chat_id, text="You're not registered yet!")
        
# def send_message_to_all_users(update: Update, context: CallbackContext) -> None:
#     users = User.query.all()
#     for user in users:
#         context.bot.send_message(chat_id=update.effective_chat.id, text=str(user.chat_id))
    
# def createBot():
#     application = ApplicationBuilder().token('6617346371:AAHVkYAvivNTPKNinfhO54aBn7xAtBSn8g4').build()
    
#     start_handler = CommandHandler('start', start)
#     set_reminder_handler = CommandHandler('set_reminder', set_reminder)
#     unset_reminder_handler = CommandHandler('unset_reminder', unset_reminder)

#     application.add_handler(start_handler)
#     application.add_handler(set_reminder_handler)
#     application.add_handler(unset_reminder_handler)
    
#     application.run_polling()
#     return application