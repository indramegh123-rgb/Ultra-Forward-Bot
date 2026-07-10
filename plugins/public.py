# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# █ 🛡️ ᴛʀᴀɴꜱᴍɪꜱꜱɪᴏɴ ɪɴɪᴛɪᴀʟɪᴢᴀᴛɪᴏɴ ᴇɴɢɪɴᴇ ᴠ3.0 [ᴇɴᴛᴇʀᴘʀɪꜱᴇ ᴇᴅɪᴛɪᴏɴ]
# █ 🎯 ᴏᴡɴᴇᴅ & ᴏᴘᴇʀᴀᴛᴇᴅ ʙʏ @IND_BOTZ 
# █ ⚠️ ᴀʟʟ ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ - ᴘʀɪᴠᴀᴛᴇ ɴᴇᴛᴡᴏʀᴋ ᴄᴏʀᴇ
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

import re
import asyncio 
import logging
from .utils import STS
from database import db
from config import temp 
from translation import Translation
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait 
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate as PrivateChat
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified, ChannelPrivate
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# ------------------------------------------------------------------------------------------------------------------------------------------------
# ⚙️ ɢʟᴏʙᴀʟ ɴᴇᴛᴡᴏʀᴋ ɪɴɪᴛɪᴀʟɪᴢᴀᴛɪᴏɴ & ʟᴏɢɢɪɴɢ
# ------------------------------------------------------------------------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [IND_INIT_CORE] - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S"
)
init_logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🚀 ᴄᴏʀᴇ ᴇɴɢɪɴᴇ: ꜰᴏʀᴡᴀʀᴅ ᴘʀᴏᴛᴏᴄᴏʟ ɪɴɪᴛɪᴀʟɪᴢᴇʀ 
# ------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.private & filters.command(["fwd", "forward"]))
async def initialize_forward_protocol(client_bot, message_obj):
    """
    Advanced Forwarding Setup Protocol.
    Collects parameters (Source, Target, Skip) interactively and hashes them into STS.
    """
    target_zone_buttons = []
    zone_mapping_cache = {}
    client_id = message_obj.from_user.id
    
    init_logger.info(f"Client {client_id} initiated the /forward protocol.")
    
    # 1. Active Node Verification
    active_node = await db.get_bot(client_id)
    if not active_node:
      init_logger.warning(f"Client {client_id} attempted forwarding without an active node.")
      return await message_obj.reply("<blockquote><b><u>🚫 ɴᴏᴅᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ</u></b></blockquote>\n\n<b>ʏᴏᴜ ᴍᴜꜱᴛ ᴀᴛᴛᴀᴄʜ ᴀ ʙᴏᴛ ᴏʀ ᴜꜱᴇʀʙᴏᴛ ᴠɪᴀ <code>/settings</code> ʙᴇꜰᴏʀᴇ ᴇxᴇᴄᴜᴛɪɴɢ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.</b>\n\n<b>🛡️ @IND_BOTZ</b>")
      
    # 2. Target Zone Verification
    registered_zones = await db.get_user_channels(client_id)
    if not registered_zones:
       return await message_obj.reply_text("<blockquote><b><u>🚫 ᴛᴀʀɢᴇᴛ ᴢᴏɴᴇ ᴍɪꜱꜱɪɴɢ</u></b></blockquote>\n\n<b>ᴘʟᴇᴀꜱᴇ ᴄᴏɴꜰɪɢᴜʀᴇ ᴀ ᴅᴇꜱᴛɪɴᴀᴛɪᴏɴ ᴄʜᴀɴɴᴇʟ ɪɴ <code>/settings</code> ꜰɪʀꜱᴛ.</b>\n\n<b>🛡️ @IND_BOTZ</b>")
       
    # 3. Target Zone Selection (If Multiple)
    if len(registered_zones) > 1:
       for zone in registered_zones:
          target_zone_buttons.append([KeyboardButton(f"📡 {zone['title']}")])
          zone_mapping_cache[f"📡 {zone['title']}"] = zone['chat_id']
          
       target_zone_buttons.append([KeyboardButton("✖️ ᴀʙᴏʀᴛ")]) 
       
       target_prompt_response = await client_bot.ask(
           message_obj.chat.id, 
           Translation.TO_MSG.format(active_node['name'], active_node['username']), 
           reply_markup=ReplyKeyboardMarkup(target_zone_buttons, one_time_keyboard=True, resize_keyboard=True)
       )
       
       if target_prompt_response.text.startswith(('/', '✖️ ᴀʙᴏʀᴛ', 'cancel')):
          return await message_obj.reply_text(Translation.CANCEL, reply_markup=ReplyKeyboardRemove())
          
       target_zone_name = target_prompt_response.text
       target_zone_id = zone_mapping_cache.get(target_zone_name)
       
       if not target_zone_id:
          return await message_obj.reply_text("<b>🚫 ɪɴᴠᴀʟɪᴅ ᴢᴏɴᴇ ꜱᴇʟᴇᴄᴛᴇᴅ. ᴘʀᴏᴄᴇꜱꜱ ᴛᴇʀᴍɪɴᴀᴛᴇᴅ!</b>", reply_markup=ReplyKeyboardRemove())
    else:
       target_zone_id = registered_zones[0]['chat_id']
       target_zone_name = registered_zones[0]['title']
       
    # 4. Source Zone Selection & Parsing
    source_prompt_response = await client_bot.ask(message_obj.chat.id, Translation.FROM_MSG, reply_markup=ReplyKeyboardRemove())
    
    if source_prompt_response.text and source_prompt_response.text.startswith('/cancel'):
        await message_obj.reply(Translation.CANCEL)
        return 
        
    # Regex Link Parsing Logic
    if source_prompt_response.text and not source_prompt_response.forward_date:
        regex_pattern = re.compile(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        url_match = regex_pattern.match(source_prompt_response.text.replace("?single", ""))
        
        if not url_match:
            return await message_obj.reply('<b>🚫 ɪɴᴠᴀʟɪᴅ ꜱᴏᴜʀᴄᴇ ʟɪɴᴋ ᴅᴇᴛᴇᴄᴛᴇᴅ.</b>')
            
        source_zone_id = url_match.group(4)
        latest_msg_index = int(url_match.group(5))
        
        if source_zone_id.isnumeric():
            source_zone_id  = int(("-100" + source_zone_id))
            
    # Direct Forward Parsing Logic
    elif source_prompt_response.forward_from_chat.type in [enums.ChatType.CHANNEL]:
        latest_msg_index = source_prompt_response.forward_from_message_id
        source_zone_id = source_prompt_response.forward_from_chat.username or source_prompt_response.forward_from_chat.id
        
        if latest_msg_index == None:
           return await message_obj.reply_text("<b>⚠️ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ ᴅᴇᴛᴇᴄᴛᴇᴅ.</b>\n\n<i>ᴛʜɪꜱ ᴀᴘᴘᴇᴀʀꜱ ᴛᴏ ʙᴇ ꜰʀᴏᴍ ᴀ ɢʀᴏᴜᴘ. ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴅɪʀᴇᴄᴛ ʟɪɴᴋ ᴛᴏ ᴛʜᴇ ʟᴀꜱᴛ ᴍᴇꜱꜱᴀɢᴇ ɪɴꜱᴛᴇᴀᴅ ᴏꜰ ꜰᴏʀᴡᴀʀᴅɪɴɢ ɪᴛ.</i>")
    else:
        await message_obj.reply_text("<b>🚫 ᴜɴᴋɴᴏᴡɴ ɪɴᴘᴜᴛ ꜰᴏʀᴍᴀᴛ !</b>")
        return 
        
    # 5. Advanced Security & Access Check
    try:
        source_zone_name = (await client_bot.get_chat(source_zone_id)).title
    except (PrivateChat, ChannelPrivate, ChannelInvalid) as access_err:
        init_logger.warning(f"Source chat access limited for {source_zone_id}: {access_err}")
        source_zone_name = "🔒 ᴘʀɪᴠᴀᴛᴇ ᴢᴏɴᴇ" if source_prompt_response.text else source_prompt_response.forward_from_chat.title
    except (UsernameInvalid, UsernameNotModified):
        return await message_obj.reply('<b>🚫 ɪɴᴠᴀʟɪᴅ ᴜꜱᴇʀɴᴀᴍᴇ / ʟɪɴᴋ ꜱᴘᴇᴄɪꜰɪᴇᴅ.</b>')
    except Exception as runtime_err:
        init_logger.error(f"Runtime Exception in Fetching Source: {runtime_err}")
        return await message_obj.reply(f'<b>❌ ꜱʏꜱᴛᴇᴍ ᴇʀʀᴏʀ:</b> - <code>{runtime_err}</code>')
        
    # 6. Bypass/Skip Parameter Configuration
    bypass_count_response = await client_bot.ask(message_obj.chat.id, Translation.SKIP_MSG)
    if bypass_count_response.text.startswith('/'):
        await message_obj.reply(Translation.CANCEL)
        return
        
    # 7. Payload Hashing & Final Confirmation
    transmission_id = f"{client_id}-{bypass_count_response.id}"
    
    confirmation_layout = [[
        InlineKeyboardButton('✅ ʏᴇꜱ, ɪɢɴɪᴛᴇ ᴇɴɢɪɴᴇ', callback_data=f"start_public_{transmission_id}"),
        InlineKeyboardButton('❌ ᴀʙᴏʀᴛ', callback_data="close_btn")
    ]]
    
    await message_obj.reply_text(
        text=Translation.DOUBLE_CHECK.format(
            botname=active_node['name'], 
            botuname=active_node['username'], 
            from_chat=source_zone_name, 
            to_chat=target_zone_name, 
            skip=bypass_count_response.text
        ),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(confirmation_layout)
    )
    
    # Store session payload in memory
    STS(transmission_id).store(source_zone_id, target_zone_id, int(bypass_count_response.text), int(latest_msg_index))
    init_logger.info(f"Transmission Payload {transmission_id} generated successfully.")

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🏁 ᴇɴᴅ ᴏꜰ ꜰɪʟᴇ : ᴛʀᴀɴꜱᴍɪꜱꜱɪᴏɴ ɪɴɪᴛɪᴀʟɪᴢᴀᴛɪᴏɴ ᴇɴɢɪɴᴇ
# ------------------------------------------------------------------------------------------------------------------------------------------------
