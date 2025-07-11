import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load .env file
load_dotenv()

# Get token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send me a TikTok link and I'll download the video without watermark.")

async def handle_tiktok_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "tiktok.com" in url:
        await update.message.reply_text("🔄 Processing...")

        try:
            api_url = f"https://tikwm.com/api/?url={url}"
            response = requests.get(api_url).json()

            if response.get("data") and response["data"].get("play"):
                video_url = response["data"]["play"]
                title = response["data"].get("title", "TikTok Video")
                await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url, caption=f"🎬 {title}")
            else:
                await update.message.reply_text("❌ Failed to download video. Try another link.")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
    else:
        await update.message.reply_text("⚠️ Please send a valid TikTok video link.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tiktok_link))
    print("Bot is running...")
    app.run_polling()
