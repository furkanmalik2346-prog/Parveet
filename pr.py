# monster_hell_bot.py
import asyncio, json, os, random, time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from flask import Flask
from threading import Thread
import logging
from typing import Dict, List, Set

# ---------------------------
# KEEP ALIVE SERVER (For Render)
# ---------------------------
server = Flask('')

@server.route('/')
def home():
    return "Bot is Running 24/7!"

def run_flask():
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

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
    "8620102385:AAFLBIAVman-IfT0GYzqitJmG7IlqwSIj9U",
    "8076835970:AAGe1h_XO0tHz8kCooOJSEIOPLBvx0xrC70",
    "8583222400:AAGFbxKVQzG13Y-Hccs48bNSicPiRGv4PUM",
    "8780347145:AAHE-AJoXzvOwDVPcIqgYJiZd8Nyp6bmNnM",
    "8403315875:AAF_J0dTmTTz7d4CaFJ2AP-Xzz_EyCQRsnI",
    "8756884113:AAFwFuyDKjFJEQQdh2aChxG8QYfIrFzpozY",
    "8742553615:AAFb3NuCKF47JTuHurU9NqHv6NeljNRUkoE",
    "8689032338:AAGCiPDKxFUlx_tZLhkZmDY-biKh0xVhZgc"
]

OWNER_ID = 8708136512
SUDO_FILE = "0563.json"

# Speed Settings
delay = 0.1  
ncemo_delay = 0.1  

# ---------------------------
# RAID TEXTS (With Bully Variations)
# ---------------------------
RAID_TEXTS = [
    "@ashuowns ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴜ ᴇᴋ ᴅɪɴ ʀᴀᴀᴛ ///////////////////////////////////",
    "@ashuowns ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴋᴇ ꜰᴀʀᴀʀʀ - ʀᴀyᴜɢᴀ ///////////////////////////////",
    "@ashuowns ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴜ ᴇᴋ ᴅɪɴ ʀᴀᴀᴛ ////////////////////////////////👻",
    "@ashuowns ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴋᴇ ꜰᴀʀᴀʀʀ ~ ʀᴀyᴜɢᴀ ///////////////////////////////👻",
    "@ashuowns ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴜ ᴇᴋ ᴅɪɴ ʀᴀᴀᴛ ////////////////////////////////🔥",
    "@ashuowns ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴋᴇ ꜰᴀʀᴀʀʀ > ʀᴀyᴜɢᴀ ///////////////////////////////🔥",
    "@ashuowns ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴜ ᴇᴋ ᴅɪɴ ʀᴀᴀᴛ ////////////////////////////////😋",
    "@ashuowns ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴋᴇ ꜰᴀʀᴀʀʀ <> ʀᴀyᴜɢᴀ ///////////////////////////////😋",
    "@ashuowns ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴜ ᴇᴋ ᴅɪɴ ʀᴀᴀᴛ ////////////////////////////////💗",
    "@ashuowns ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴋᴇ ꜰᴀʀᴀʀʀ < ʀᴀyᴜɢᴀ ///////////////////////////////💗",
    "𝑮𝑪 𝑳𝑬𝑭𝑻 𝑳𝑬 लंगड़ी ᴍᴀᴀ ᴋᴇ ʙᴀᴄʜᴇ 🤮",
    "Tmkc pe chppl hi chppl marunga !! 🔥😂🩴 ",
    "Awaz neeche rndy k bacche 🤢🔥",
    "𝙎𝙐𝙋𝙋𝙊𝙍𝙏 𝙇𝘼 🤲🏿",
    "Bol Ｍｏｎｓｔｅｒ  ᴅꫝᴅᴅꪗ ❤‍🩹",
    "ΤΜΚΒ 😹🔥😹🔥"
]

# ---------------------------
# BOT LOGIC & HANDLERS
# ---------------------------
apps = []
bots = []
raid_tasks = {}
gcnc_tasks = {}

def build_app(token):
    app = Application.builder().token(token).build()
    # Basic Raid Handlers
    app.add_handler(CommandHandler("raid", start_raid))
    app.add_handler(CommandHandler("stop", stop_raid))
    app.add_handler(CommandHandler("gcnc", start_gcnc))
    app.add_handler(CommandHandler("stopgcnc", stop_gcnc))
    return app

async def start_raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    target = context.args[0] if context.args else ""
    chat_id = update.effective_chat.id
    
    async def raid_loop():
        while chat_id in raid_tasks:
            msg = random.choice(RAID_TEXTS)
            for bot in bots:
                try: await bot.send_message(chat_id, f"{target} {msg}")
                except: pass
            await asyncio.sleep(delay)

    raid_tasks[chat_id] = True
    asyncio.create_task(raid_loop())
    await update.message.reply_text("🚀 Raid Started!")

async def stop_raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in raid_tasks:
        del raid_tasks[chat_id]
        await update.message.reply_text("🛑 Raid Stopped!")

async def start_gcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    new_name = " ".join(context.args) if context.args else "Raid By Monster"
    chat_id = update.effective_chat.id
    
    async def gcnc_loop():
        while chat_id in gcnc_tasks:
            full_name = f"{new_name} {random.choice(RAID_TEXTS)[:10]}"
            for bot in bots:
                try: await bot.set_chat_title(chat_id, title=full_name)
                except: pass
            await asyncio.sleep(ncemo_delay)

    gcnc_tasks[chat_id] = True
    asyncio.create_task(gcnc_loop())
    await update.message.reply_text("🧨 GCNC Started!")

async def stop_gcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in gcnc_tasks:
        del gcnc_tasks[chat_id]
        await update.message.reply_text("🛑 GCNC Stopped!")

async def run_all_bots():
    keep_alive() # Start Flask server for Render
    for token in TOKENS:
        try:
            app = build_app(token)
            apps.append(app)
            await app.initialize()
            await app.start()
            await app.updater.start_polling()
            bots.append(app.bot)
        except: pass
    
    print("🔥 All Bots Active & Keep-Alive Running!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(run_all_bots())
    except KeyboardInterrupt:
        pass
