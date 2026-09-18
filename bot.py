import os
import re
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]

LINK_PATTERN = re.compile(
    r"(https?://\S+|www\.\S+|t\.me/\S+|telegram\.me/\S+)",
    re.IGNORECASE
)


async def delete_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if not message or not message.text:
        return

    # Adminদের message delete করবে না
    member = await context.bot.get_chat_member(
        message.chat_id,
        message.from_user.id
    )

    if member.status in ("administrator", "creator"):
        return

    # Link থাকলে message delete
    if LINK_PATTERN.search(message.text):
        try:
            await message.delete()
        except Exception as e:
            print(f"Delete error: {e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            delete_link
        )
    )

    print("NOREX Auto Link Delete Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
