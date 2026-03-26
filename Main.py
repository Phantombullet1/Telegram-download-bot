import yt_dlp
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("اكتب اسم الأغنية 🎵")
        return

    query = " ".join(context.args)
    await update.message.reply_text("🔍 جاري البحث...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            video = info['entries'][0]
            filename = ydl.prepare_filename(video)

        await update.message.reply_audio(audio=open(filename, 'rb'))
        os.remove(filename)

    except:
        await update.message.reply_text("❌ صار خطأ")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("song", song))

app.run_polling()
