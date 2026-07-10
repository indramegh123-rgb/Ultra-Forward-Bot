# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# █ 🛡️ ꜱʏꜱᴛᴇᴍ ᴍᴏɴɪᴛᴏʀɪɴɢ & ᴜᴛɪʟɪᴛʏ ᴄᴏʀᴇ ᴠ3.0 [ᴇɴᴛᴇʀᴘʀɪꜱᴇ ᴇᴅɪᴛɪᴏɴ]
# █ 🎯 ᴏᴡɴᴇᴅ & ᴏᴘᴇʀᴀᴛᴇᴅ ʙʏ @IND_BOTZ 
# █ ⚠️ ᴀʟʟ ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ - ᴘʀɪᴠᴀᴛᴇ ɴᴇᴛᴡᴏʀᴋ ᴄᴏʀᴇ
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

import os
import sys
import asyncio
import time
import logging

from config import *
from database import *
from .utils import get_readable_time
from translation import *
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 

# ------------------------------------------------------------------------------------------------------------------------------------------------
# ⚙️ ɢʟᴏʙᴀʟ ꜱʏꜱᴛᴇᴍ ɪɴɪᴛɪᴀʟɪᴢᴀᴛɪᴏɴ & ʟᴏɢɢɪɴɢ ᴘʀᴏᴛᴏᴄᴏʟꜱ
# ------------------------------------------------------------------------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [IND_UTILITY_CORE] - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S"
)
utility_logger = logging.getLogger(__name__)

# Boot Timer Initialization
SYSTEM_BOOT_TIME = time.time()

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🏓 ɴᴇᴛᴡᴏʀᴋ ʟᴀᴛᴇɴᴄʏ (ᴘɪɴɢ) ᴄᴏᴍᴍᴀɴᴅ
# ------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.private & filters.command(["ping", "p"]))
async def network_ping(client_bot, message_obj):
    """
    Checks the real-time server latency and response time of the bot.
    """
    start_timer = time.time()
    status_msg = await message_obj.reply_text("<blockquote><b>⏳ ᴘɪɴɢɪɴɢ ᴍᴀɪɴ ꜱᴇʀᴠᴇʀ...</b></blockquote>", quote=True)
    end_timer = time.time()
    
    latency_ms = (end_timer - start_timer) * 1000
    
    ping_layout = f"<blockquote><b><u>🏓 ɴᴇᴛᴡᴏʀᴋ ʟᴀᴛᴇɴᴄʏ</u></b></blockquote>\n\n<b>⚡ ʀᴇꜱᴘᴏɴꜱᴇ ᴛɪᴍᴇ :</b> <code>{latency_ms:.3f} ᴍꜱ</code>\n<b>🔥 ꜱᴛᴀᴛᴜꜱ :</b> <b>ᴏᴘᴛɪᴍᴀʟ & ꜱᴇᴄᴜʀᴇ</b>\n\n<b>🛡️ @IND_BOTZ</b>"
    
    await status_msg.edit(ping_layout)
    utility_logger.info(f"Ping requested by {message_obj.from_user.id}. Latency: {latency_ms:.3f} ms")
    return latency_ms

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 📊 ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ (ꜱᴛᴀᴛꜱ) ᴄᴏᴍᴍᴀɴᴅ [ᴀᴅᴍɪɴ ᴏɴʟʏ]
# ------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.command(["stats", "status", "s"]) & filters.user(Config.OWNER_ID))
async def system_statistics(client_bot, message_obj):
    """
    Fetches core system metrics, active userbot nodes, and database stats.
    Only accessible by the Network Owner.
    """
    utility_logger.info(f"Admin {message_obj.from_user.id} requested system statistics.")
    
    # Fetching Database Metrics
    users_count, bots_count = await db.total_users_bots_count()
    total_channels = await db.total_channels()
    sys_uptime = get_readable_time(time.time() - SYSTEM_BOOT_TIME)    
    
    start_timer = time.time()
    processing_msg = await message_obj.reply('<blockquote><b>⏳ ꜰᴇᴛᴄʜɪɴɢ ꜱʏꜱᴛᴇᴍ ᴍᴇᴛʀɪᴄꜱ ꜰʀᴏᴍ ᴅᴀᴛᴀʙᴀꜱᴇ...</b></blockquote>')    
    end_timer = time.time()
    
    latency = (end_timer - start_timer) * 1000
    
    stats_layout = f"""<blockquote><b><u>📊 ꜱʏꜱᴛᴇᴍ ᴏᴠᴇʀᴠɪᴇᴡ ᴘᴀɴᴇʟ</u></b></blockquote>

<b>⏱️ ꜱʏꜱᴛᴇᴍ ᴜᴘᴛɪᴍᴇ :</b> <code>{sys_uptime}</code>
<b>⚡ ᴄᴏʀᴇ ʟᴀᴛᴇɴᴄʏ :</b> <code>{latency:.3f} ᴍꜱ</code>

<b>👥 ᴀᴄᴛɪᴠᴇ ᴜꜱᴇʀꜱ :</b> <code>{users_count}</code>
<b>🤖 ᴀᴛᴛᴀᴄʜᴇᴅ ɴᴏᴅᴇꜱ :</b> <code>{bots_count}</code>
<b>📡 ᴛᴀʀɢᴇᴛ ᴢᴏɴᴇꜱ :</b> <code>{total_channels}</code>

<b>🔄 ᴀᴄᴛɪᴠᴇ ᴛʀᴀɴꜱᴍɪꜱꜱɪᴏɴꜱ :</b> <code>{temp.forwardings}</code>
<b>🚫 ʙʟᴏᴄᴋᴇᴅ ᴄʟɪᴇɴᴛꜱ :</b> <code>{temp.BANNED_USERS}</code>

<b>🛡️ ᴍᴀɴᴀɢᴇᴅ ʙʏ @IND_BOTZ</b>"""
    
    await processing_msg.edit(text=stats_layout)

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 💎 ꜱᴜᴘᴘᴏʀᴛ / ᴅᴏɴᴀᴛɪᴏɴ ᴄᴏᴍᴍᴀɴᴅ
# ------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.private & filters.command(["donate", "d"]))
async def support_developer(client_bot, message_obj):
    """
    Displays the donation panel with premium UI elements and inline buttons.
    """
    utility_logger.info(f"User {message_obj.from_user.id} opened the donation panel.")
    
    donate_text = """<blockquote><b><u>💎 ꜱᴜᴘᴘᴏʀᴛ ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ</u></b></blockquote>

<b>ɪꜰ ʏᴏᴜ ᴀᴘᴘʀᴇᴄɪᴀᴛᴇ ᴛʜᴇ ʜɪɢʜ-ꜱᴘᴇᴇᴅ ᴍᴏᴠɪᴇ ɪɴᴅᴇxɪɴɢ ᴀɴᴅ ꜱᴇᴀᴍʟᴇꜱꜱ ᴀᴜᴛᴏᴍᴀᴛɪᴏɴ ᴏꜰ ᴏᴜʀ ʙᴏᴛ ɴᴇᴛᴡᴏʀᴋ, ᴄᴏɴꜱɪᴅᴇʀ ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴜꜱ.</b>

<b>ʏᴏᴜʀ ᴄᴏɴᴛʀɪʙᴜᴛɪᴏɴꜱ ʜᴇʟᴘ ᴋᴇᴇᴘ ᴛʜᴇ ꜱᴇʀᴠᴇʀꜱ ᴀʟɪᴠᴇ ᴀɴᴅ ᴜᴘɢʀᴀᴅᴇꜱ ʀᴏʟʟɪɴɢ! 🚀</b>

<b>🛍 ᴜᴘɪ ɪᴅ :</b> <code>INDBOTZ@UPI</code>

<b>🛡️ @IND_BOTZ</b>"""
    
    donate_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🦋 ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ", url="https://t.me/IND_BOTZ"), 
         InlineKeyboardButton("✖️ ᴄʟᴏꜱᴇ", callback_data="close_btn")]
    ])
    
    await message_obj.reply_text(text=donate_text, reply_markup=donate_buttons)

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🏁 ᴇɴᴅ ᴏꜰ ꜰɪʟᴇ : ꜱʏꜱᴛᴇᴍ ᴍᴏɴɪᴛᴏʀɪɴɢ ᴄᴏʀᴇ
# ------------------------------------------------------------------------------------------------------------------------------------------------
