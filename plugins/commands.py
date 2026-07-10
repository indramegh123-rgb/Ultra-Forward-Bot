# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# █ 🛡️ ꜱʏꜱᴛᴇᴍ ɪɴɪᴛɪᴀʟɪᴢᴀᴛɪᴏɴ & ᴜɪ ᴄᴏʀᴇ ᴠ3.0 [ᴇɴᴛᴇʀᴘʀɪꜱᴇ ᴇᴅɪᴛɪᴏɴ]
# █ 🎯 ᴏᴡɴᴇᴅ & ᴏᴘᴇʀᴀᴛᴇᴅ ʙʏ @IND_BOTZ 
# █ ⚠️ ᴀʟʟ ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ - ᴘʀɪᴠᴀᴛᴇ ɴᴇᴛᴡᴏʀᴋ ᴄᴏʀᴇ
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

import os
import sys
import asyncio 
import logging
from database import db, mongodb_version
from config import Config, temp
from platform import python_version
from translation import Translation
from pyrogram import Client, filters, enums, __version__ as pyrogram_version
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument

# ------------------------------------------------------------------------------------------------------------------------------------------------
# ⚙️ ɢʟᴏʙᴀʟ ꜱʏꜱᴛᴇᴍ ɪɴɪᴛɪᴀʟɪᴢᴀᴛɪᴏɴ & ʟᴏɢɢɪɴɢ ᴘʀᴏᴛᴏᴄᴏʟꜱ
# ------------------------------------------------------------------------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [IND_START_CORE] - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S"
)
start_logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🎨 ɢʟᴏʙᴀʟ ᴜɪ ᴍᴀᴛʀɪx (ᴍᴀɪɴ ᴍᴇɴᴜ ʙᴜᴛᴛᴏɴꜱ)
# ------------------------------------------------------------------------------------------------------------------------------------------------

SYSTEM_MAIN_BUTTONS = [
    [
        InlineKeyboardButton('📢 ᴏꜰꜰɪᴄɪᴀʟ ᴜᴘᴅᴀᴛᴇꜱ', url='https://t.me/IND_BOTZ'),
        InlineKeyboardButton('💬 ɴᴇᴛᴡᴏʀᴋ ꜱᴜᴘᴘᴏʀᴛ', url='https://t.me/IND_BOTZ')
    ],[
        InlineKeyboardButton('🛠️ ꜱʏꜱᴛᴇᴍ ʜᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('🤖 ᴀʙᴏᴜᴛ ᴇɴɢɪɴᴇ', callback_data='about')
    ],[
        InlineKeyboardButton('🧑‍💻 ᴄᴏʀᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ 🧑‍💻', url='https://t.me/IND_BOTZ')
    ]
]

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🚀 ᴍᴀɪɴ ᴇxᴇᴄᴜᴛɪᴏɴ ʙʟᴏᴄᴋ: ꜱᴛᴀʀᴛ ᴘʀᴏᴛᴏᴄᴏʟ
# ------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.private & filters.command(['start']))
async def initialize_start_sequence(client_bot, message_obj):
    """
    Core Entry Point for users.
    Registers new clients to the database and deploys the welcome interface.
    """
    client_info = message_obj.from_user
    
    # Database Registration Check
    if not await db.is_user_exist(client_info.id):
        await db.add_user(client_info.id, client_info.first_name)
        start_logger.info(f"New client registered to network: {client_info.id} ({client_info.first_name})")
        
    layout_markup = InlineKeyboardMarkup(SYSTEM_MAIN_BUTTONS)
    
    # Premium Welcome Animation (Sticker)
    try:
        welcome_sticker = await message_obj.reply_sticker("CAACAgUAAxkBAAECEEBlLA-nYcsWmsNWgE8-xqIkriCWAgACJwEAAsiUZBTiPWKAkUSmmh4E")
        await asyncio.sleep(2)
        await welcome_sticker.delete()
    except Exception as e:
        start_logger.warning(f"Failed to send welcome sticker: {e}")
        pass
        
    formatted_text = Translation.START_TXT.format(client_info.mention)
    
    await message_obj.reply_text(
        text=formatted_text,
        reply_markup=layout_markup,
        quote=True
    )

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🔄 ꜱʏꜱᴛᴇᴍ ʀᴇʙᴏᴏᴛ ᴘʀᴏᴛᴏᴄᴏʟ [ᴀᴅᴍɪɴ ᴏɴʟʏ]
# ------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.private & filters.command(['restart', "r"]) & filters.user(Config.OWNER_ID))
async def trigger_system_reboot(client_bot, message_obj):
    """
    Safely shuts down current processes and restarts the Python execution environment.
    """
    start_logger.info(f"System reboot triggered by Admin {message_obj.from_user.id}")
    
    status_ui = await message_obj.reply_text(
        text="<blockquote><b>⏳ ɪɴɪᴛɪᴀᴛɪɴɢ ꜱʏꜱᴛᴇᴍ ʀᴇʙᴏᴏᴛ...</b></blockquote>\n\n<b>ᴛᴇʀᴍɪɴᴀᴛɪɴɢ ᴀᴄᴛɪᴠᴇ ɴᴏᴅᴇꜱ ᴀɴᴅ ᴄʟᴇᴀʀɪɴɢ ᴄᴀᴄʜᴇ...</b>",
        quote=True
    )
    
    await asyncio.sleep(5)
    await status_ui.edit("<blockquote><b>✅ ꜱᴇʀᴠᴇʀ ʀᴇꜱᴛᴀʀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!</b></blockquote>\n\n<b>🛡️ ɴᴇᴛᴡᴏʀᴋ ɪꜱ ɴᴏᴡ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴏᴘᴇʀᴀᴛɪᴏɴᴀʟ.</b>")
    
    # Execute OS level restart
    os.execl(sys.executable, sys.executable, *sys.argv)
    
# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🎛️ ᴜɪ ɴᴀᴠɪɢᴀᴛɪᴏɴ ʀᴏᴜᴛᴇʀꜱ (ᴄᴀʟʟʙᴀᴄᴋ ʜᴀɴᴅʟᴇʀꜱ)
# ------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_callback_query(filters.regex(r'^help'))
async def route_help_menu(bot, query):
    """ Routes the user to the Network Help Panel. """
    help_layout = InlineKeyboardMarkup([
        [InlineKeyboardButton('🛠️ ᴏᴘᴇʀᴀᴛɪᴏɴ ɢᴜɪᴅᴇ 🛠️', callback_data='how_to_use')],
        [
            InlineKeyboardButton('⚙️ ꜱᴇᴛᴛɪɴɢꜱ ⚙️', callback_data='settings#main'),
            InlineKeyboardButton('📊 ɴᴇᴛᴡᴏʀᴋ ꜱᴛᴀᴛꜱ 📊', callback_data='status')
        ],
        [InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ ᴛᴏ ᴍᴀɪɴ ᴍᴇɴᴜ', callback_data='back')]
    ])
    
    await query.message.edit_text(
        text=Translation.HELP_TXT,
        reply_markup=help_layout
    )

@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def route_guide_menu(bot, query):
    """ Routes the user to the Operational Guidelines. """
    guide_layout = InlineKeyboardMarkup([
        [InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ', callback_data='help')]
    ])
    
    await query.message.edit_text(
        text=Translation.HOW_USE_TXT,
        reply_markup=guide_layout,
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r'^back'))
async def route_main_menu(bot, query):
    """ Returns the user to the Core Initialization Panel. """
    await query.message.edit_text(
       text=Translation.START_TXT.format(query.from_user.first_name),
       reply_markup=InlineKeyboardMarkup(SYSTEM_MAIN_BUTTONS)
    )

@Client.on_callback_query(filters.regex(r'^about'))
async def route_about_menu(bot, query):
    """ Routes the user to the System Information Panel. """
    about_layout = InlineKeyboardMarkup([
        [InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ ᴛᴏ ᴍᴀɪɴ ᴍᴇɴᴜ', callback_data='back')]
    ])
    
    await query.message.edit_text(
        text=Translation.ABOUT_TXT.format(bot.me.mention),
        reply_markup=about_layout,
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.HTML,
    )

@Client.on_callback_query(filters.regex(r'^status'))
async def route_system_status(bot, query):
    """ Routes the user to the Network Statistics Dashboard. """
    users_count, bots_count = await db.total_users_bots_count()
    total_channels = await db.total_channels()
    
    status_layout = InlineKeyboardMarkup([
        [InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ', callback_data='help')]
    ])
    
    await query.message.edit_text(
        text=Translation.STATUS_TXT.format(users_count, bots_count, temp.forwardings),
        reply_markup=status_layout,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )
    
# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🏁 ᴇɴᴅ ᴏꜰ ꜰɪʟᴇ : ꜱʏꜱᴛᴇᴍ ɪɴɪᴛɪᴀʟɪᴢᴀᴛɪᴏɴ ᴄᴏʀᴇ
# ------------------------------------------------------------------------------------------------------------------------------------------------
