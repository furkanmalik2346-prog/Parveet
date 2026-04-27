import asyncio, json, os, random, time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# ---------------------------
# CONFIG
# ---------------------------
TOKENS = [
    "8766896904:AAEApB6L78dwohP7o9-ar8CLuJZKgCUCR6E",
    "8758889079:AAHtGgRik3wTSqFh31fVqgiNK7TZluV_scU",
    "8774587083:AAE156lL_gmQru8M8iEsldRJakMxOFpuFp8",
    "8472864056:AAFMM2OV-KdXOviLrkgD_vaLHtYdM5XepXo",
    "8600227885:AAEohY1eFioMdNA6ssSyMaRJBF4NFD9v4-Q",
    "8669769904:AAEnoObtBGuCx-IfsrLMZoLM0p6KqiYDbGo",
    "8614662345:AAFsKPW-F-5e-o3c28GEOefQC70dCJ86AY4",
    "8620102385:AAFLBIAVman-IfT0GYzqitJmG7IlqwSIj9U"
]

OWNER_ID = 8708136512  # Updated Owner ID

# ---------------------------
# DIVIDED SPAM TEXTS (5 Parts)
# ---------------------------
SPAM_1 = [
    "ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴜ ᴇᴋ ᴅɪɴ ʀᴀᴀᴛ ///////////////////////////////////",
    "ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴋᴇ ꜰᴀʀᴀʀʀ - ʀᴀyᴜɢᴀ ///////////////////////////////"
]

SPAM_2 = [
    "ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴜ ᴇᴋ ᴅɪɴ ʀᴀᴀᴛ ////////////////////////////////👻",
    "ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴋᴇ ꜰᴀʀᴀʀʀ ~ ʀᴀyᴜɢᴀ ///////////////////////////////👻"
]

SPAM_3 = [
    "ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴜ ᴇᴋ ᴅɪɴ ʀᴀᴀᴛ ////////////////////////////////🔥",
    "ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴋᴇ ꜰᴀʀᴀʀʀ > ʀᴀyᴜɢᴀ ///////////////////////////////🔥"
]

SPAM_4 = [
    "ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴜ ᴇᴋ ᴅɪɴ ʀᴀᴀᴛ ////////////////////////////////😋",
    "ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴋᴇ ꜰᴀʀᴀʀʀ <> ʀᴀyᴜɢᴀ ///////////////////////////////😋"
]

SPAM_5 = [
    "ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴜ ᴇᴋ ᴅɪɴ ʀᴀᴀᴛ ////////////////////////////////💗",
    "ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴋᴇ ꜰᴀʀᴀʀʀ < ʀᴀyᴜɢᴀ ///////////////////////////////💗"
]

ALL_SPAMS = [SPAM_1, SPAM_2, SPAM_3, SPAM_4, SPAM_5]

# Global tracking
raid_tasks = {}

async def raid_logic(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    target = job.data['target']
    chat_id = job.data['chat_id']
    
    # Har baar alag category se text uthayega
    category = random.choice(ALL_SPAMS)
    message_text = random.choice(category)
    
    try:
        await context.bot.send_message(chat_id=chat_id, text=f"{target} {message_text}")
    except Exception:
        pass

async def start_raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    args = context.args
    if not args:
        await update.message.reply_text("Usage: /raid <target>")
        return

    target = args[0]
    chat_id = update.effective_chat.id
    
    if chat_id in raid_tasks:
        await update.message.reply_text("Ek raid pehle se chal rahi hai!")
        return

    # Start repeating task
    job = context.job_queue.run_repeating(raid_logic, interval=0.5, first=0, 
                                        data={'target': target, 'chat_id': chat_id})
    raid_tasks[chat_id] = job
    await update.message.reply_text(f"🚀 Raid started on {target}!")

async def stop_raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    chat_id = update.effective_chat.id
    if chat_id in raid_tasks:
        raid_tasks[chat_id].schedule_removal()
        del raid_tasks[chat_id]
        await update.message.reply_text("🛑 Raid stopped!")
    else:
        await update.message.reply_text("Koi raid nahi chal rahi.")

# --- Main Bot Logic (Simplified for your use) ---
# Yahan se aage ka code aapki file ke setup ke mutabiq polling start karega.
