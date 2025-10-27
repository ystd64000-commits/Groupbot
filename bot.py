import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8282083267:AAENF1hlggsOZ6G_u6C8x2l8afw-Dt18-xI")
GROUP_ID = -8463257986  # Put your group chat ID here

USERS_FILE = "users.txt"


# Save user ID when they type /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    with open(USERS_FILE, "a+") as f:
        f.seek(0)
        if str(user_id) not in f.read():
            f.write(str(user_id) + "\n")

    await update.message.reply_text("✅ Bot Activated!\nពេល Group មាន Video/Photo ខ្ញុំនឹងផ្ញើទៅអ្នកដោយ Auto")


# Auto forward media from group to users who joined bot
async def group_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != GROUP_ID:
        return

    message = update.message

    try:
        with open(USERS_FILE, "r") as f:
            user_ids = [int(uid.strip()) for uid in f.readlines()]
    except:
        user_ids = []

    if not user_ids:
        return

    for uid in user_ids:
        try:
            await message.forward(chat_id=uid)
        except:
            pass


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    
    app.add_handler(MessageHandler(
        filters.Chat(GROUP_ID) &
        (filters.VIDEO | filters.PHOTO),
        group_forward
    ))

    print("✅ Bot Running...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
