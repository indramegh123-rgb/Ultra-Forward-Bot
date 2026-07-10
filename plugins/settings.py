# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# █ 🛡️ ᴀᴅᴠᴀɴᴄᴇᴅ ꜱʏꜱᴛᴇᴍ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴ ᴇɴɢɪɴᴇ ᴠ3.0
# █ 🎯 ᴏᴡɴᴇᴅ & ᴏᴘᴇʀᴀᴛᴇᴅ ʙʏ @IND_BOTZ 
# █ ⚠️ ᴀʟʟ ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ - ᴘʀɪᴠᴀᴛᴇ ᴇᴅɪᴛɪᴏɴ
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

import asyncio 
import logging
from database import db
from config import Config
from translation import Translation
from pyrogram import Client, filters
from .test import get_configs, update_configs, CLIENT, parse_buttons
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ------------------------------------------------------------------------------------------------------------------------------------------------
# ⚙️ ɢʟᴏʙᴀʟ ɴᴇᴛᴡᴏʀᴋ ɪɴɪᴛɪᴀʟɪᴢᴀᴛɪᴏɴ
# ------------------------------------------------------------------------------------------------------------------------------------------------

IND_NETWORK_CLIENT = CLIENT()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("IND_SETTINGS_CORE")

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🚀 ᴍᴀɪɴ ꜱᴇᴛᴛɪɴɢꜱ ᴄᴏᴍᴍᴀɴᴅ ʜᴀɴᴅʟᴇʀ
# ------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.private & filters.command(['settings']))
async def system_settings_panel(client, message):
    """ Initializes the main configuration interface for the user. """
    display_text = "<blockquote><b><u>⚙️ ꜱʏꜱᴛᴇᴍ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴ ᴘᴀɴᴇʟ</u></b></blockquote>\n\n<b>ᴄᴜꜱᴛᴏᴍɪᴢᴇ ʏᴏᴜʀ ꜰᴏʀᴡᴀʀᴅ ᴇɴɢɪɴᴇ ᴘᴀʀᴀᴍᴇᴛᴇʀꜱ ʜᴇʀᴇ. ꜱᴇʟᴇᴄᴛ ᴀɴ ᴏᴘᴛɪᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴍᴏᴅɪꜰʏ.</b>\n\n<b>🛡️ @IND_BOTZ</b>"
    await message.reply_text(
        text=display_text,
        reply_markup=generate_main_buttons(),
        quote=True
    )
    
# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🎛️ ᴄᴏʀᴇ ᴄᴀʟʟʙᴀᴄᴋ ᴍᴀɴᴀɢᴇʀ (ʜᴀɴᴅʟᴇꜱ ᴀʟʟ ᴜɪ ɪɴᴛᴇʀᴀᴄᴛɪᴏɴꜱ)
# ------------------------------------------------------------------------------------------------------------------------------------------------
    
@Client.on_callback_query(filters.regex(r'^settings'))
async def settings_callback_router(bot, query):
  client_id = query.from_user.id
  callback_prefix, callback_action = query.data.split("#")
  
  # Default return button payload
  return_payload = [[InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ ᴛᴏ ᴍᴀɪɴ ᴍᴇɴᴜ', callback_data="settings#main")]]
  
  # --- [ ᴍᴀɪɴ ᴍᴇɴᴜ ʀᴏᴜᴛɪɴɢ ] ---
  if callback_action == "main":
     await query.message.edit_text(
       "<blockquote><b><u>⚙️ ꜱʏꜱᴛᴇᴍ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴ ᴘᴀɴᴇʟ</u></b></blockquote>\n\n<b>ᴄᴜꜱᴛᴏᴍɪᴢᴇ ʏᴏᴜʀ ꜰᴏʀᴡᴀʀᴅ ᴇɴɢɪɴᴇ ᴘᴀʀᴀᴍᴇᴛᴇʀꜱ ʜᴇʀᴇ.</b>\n\n<b>🛡️ @IND_BOTZ</b>",
       reply_markup=generate_main_buttons())
       
  # --- [ ʙᴏᴛ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ] ---
  elif callback_action == "bots":
     active_buttons = [] 
     active_node = await db.get_bot(client_id)
     if active_node is not None:
        active_buttons.append([InlineKeyboardButton(f"🤖 {active_node['name']}", callback_data=f"settings#editbot")])
     else:
        active_buttons.append([InlineKeyboardButton('✚ ᴀᴛᴛᴀᴄʜ ʙᴏᴛ ✚', callback_data="settings#addbot")])
        active_buttons.append([InlineKeyboardButton('✚ ᴀᴛᴛᴀᴄʜ ᴜꜱᴇʀʙᴏᴛ ✚', callback_data="settings#adduserbot")])
     active_buttons.append([InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ', callback_data="settings#main")])
     
     await query.message.edit_text(
       "<blockquote><b><u>🤖 ᴄᴏɴɴᴇᴄᴛᴇᴅ ɴᴏᴅᴇꜱ</u></b></blockquote>\n\n<b>ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ʙᴏᴛꜱ ᴀɴᴅ ᴜꜱᴇʀʙᴏᴛꜱ ʜᴇʀᴇ.</b>\n\n<b>🛡️ @IND_BOTZ</b>",
       reply_markup=InlineKeyboardMarkup(active_buttons))
  
  elif callback_action == "addbot":
     await query.message.delete()
     bot_auth = await IND_NETWORK_CLIENT.add_bot(bot, query)
     if bot_auth != True: return
     await query.message.reply_text(
        "<b>✅ ᴀᴘɪ ᴛᴏᴋᴇɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ɪɴᴊᴇᴄᴛᴇᴅ ɪɴᴛᴏ ᴅᴀᴛᴀʙᴀꜱᴇ.</b>\n\n<b>🛡️ @IND_BOTZ</b>",
        reply_markup=InlineKeyboardMarkup(return_payload))
  
  elif callback_action == "adduserbot":
     await query.message.delete()
     user_auth = await IND_NETWORK_CLIENT.add_session(bot, query)
     if user_auth != True: return
     await query.message.reply_text(
        "<b>✅ ꜱᴇꜱꜱɪᴏɴ ꜱᴛʀɪɴɢ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴠᴇʀɪꜰɪᴇᴅ & ᴀᴅᴅᴇᴅ.</b>\n\n<b>🛡️ @IND_BOTZ</b>",
        reply_markup=InlineKeyboardMarkup(return_payload))
      
  # --- [ ᴄʜᴀɴɴᴇʟ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ] ---
  elif callback_action == "channels":
     zone_buttons = []
     target_zones = await db.get_user_channels(client_id)
     for zone in target_zones:
        zone_buttons.append([InlineKeyboardButton(f"📡 {zone['title']}", callback_data=f"settings#editchannels_{zone['chat_id']}")])
        
     zone_buttons.append([InlineKeyboardButton('✚ ᴀᴅᴅ ɴᴇᴡ ᴢᴏɴᴇ ✚', callback_data="settings#addchannel")])
     zone_buttons.append([InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ', callback_data="settings#main")])
     
     await query.message.edit_text( 
       "<blockquote><b><u>📡 ᴛᴀʀɢᴇᴛ ᴢᴏɴᴇꜱ</u></b></blockquote>\n\n<b>ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴅᴇꜱᴛɪɴᴀᴛɪᴏɴ ᴄʜᴀɴɴᴇʟꜱ ʜᴇʀᴇ.</b>\n\n<b>🛡️ @IND_BOTZ</b>",
       reply_markup=InlineKeyboardMarkup(zone_buttons))
   
  elif callback_action == "addchannel":  
     await query.message.delete()
     try:
         prompt_msg = await bot.send_message(client_id, "<blockquote><b><u>🎯 ꜱᴇᴛ ᴛᴀʀɢᴇᴛ ᴢᴏɴᴇ</u></b></blockquote>\n\n<b>ꜰᴏʀᴡᴀʀᴅ ᴀɴʏ ᴍᴇꜱꜱᴀɢᴇ ꜰʀᴏᴍ ʏᴏᴜʀ ᴛᴀʀɢᴇᴛ ᴄʜᴀᴛ ᴛᴏ ᴠᴇʀɪꜰʏ.</b>\n<code>/cancel</code> - <b>ᴀʙᴏʀᴛ ᴏᴘᴇʀᴀᴛɪᴏɴ</b>\n\n<b>🛡️ @IND_BOTZ</b>")
         chat_response = await bot.listen(chat_id=client_id, timeout=300)
         
         if chat_response.text == "/cancel":
            await chat_response.delete()
            return await prompt_msg.edit_text("<b>❌ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴀʙᴏʀᴛᴇᴅ !</b>\n\n<b>♻️ @IND_BOTZ</b>", reply_markup=InlineKeyboardMarkup(return_payload))
         elif not chat_response.forward_date:
            await chat_response.delete()
            return await prompt_msg.edit_text("<b>🚫 ɪɴᴠᴀʟɪᴅ ɪɴᴘᴜᴛ. ᴍᴜꜱᴛ ʙᴇ ᴀ ꜰᴏʀᴡᴀʀᴅᴇᴅ ᴍᴇꜱꜱᴀɢᴇ.</b>")
         else:
            ext_chat_id = chat_response.forward_from_chat.id
            ext_title = chat_response.forward_from_chat.title
            ext_username = chat_response.forward_from_chat.username
            ext_username = "@" + ext_username if ext_username else "ᴘʀɪᴠᴀᴛᴇ ᴢᴏɴᴇ"
            
         zone_status = await db.add_channel(client_id, ext_chat_id, ext_title, ext_username)
         await chat_response.delete()
         await prompt_msg.edit_text(
            "<b>✅ ᴢᴏɴᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇɢɪꜱᴛᴇʀᴇᴅ !</b>" if zone_status else "<b>⚠️ ᴢᴏɴᴇ ᴀʟʀᴇᴀᴅʏ ᴇxɪꜱᴛꜱ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ.</b>",
            reply_markup=InlineKeyboardMarkup(return_payload))
            
     except asyncio.exceptions.TimeoutError:
         await prompt_msg.edit_text('<b>⏳ ꜱᴇꜱꜱɪᴏɴ ᴛɪᴍᴇᴅ ᴏᴜᴛ. ᴘʀᴏᴄᴇꜱꜱ ᴄᴀɴᴄᴇʟʟᴇᴅ.</b>', reply_markup=InlineKeyboardMarkup(return_payload))
  
  # --- [ ɴᴏᴅᴇ / ᴢᴏɴᴇ ᴇᴅɪᴛɪɴɢ ] ---
  elif callback_action == "editbot": 
     active_node = await db.get_bot(client_id)
     details_template = Translation.BOT_DETAILS if active_node['is_bot'] else Translation.USER_DETAILS
     ctrl_buttons = [
         [InlineKeyboardButton('❌ ᴅᴇꜱᴛʀᴏʏ ɴᴏᴅᴇ ❌', callback_data=f"settings#removebot")],
         [InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ', callback_data="settings#bots")]
     ]
     await query.message.edit_text(
        details_template.format(active_node['name'], active_node['id'], active_node['username']),
        reply_markup=InlineKeyboardMarkup(ctrl_buttons))
                                             
  elif callback_action == "removebot":
     await db.remove_bot(client_id)
     await query.message.edit_text("<b>✅ ɴᴏᴅᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇꜱᴛʀᴏʏᴇᴅ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
                                             
  elif callback_action.startswith("editchannels"): 
     target_id = callback_action.split('_')[1]
     zone_data = await db.get_channel_details(client_id, target_id)
     ctrl_buttons = [
         [InlineKeyboardButton('❌ ʀᴇᴍᴏᴠᴇ ᴢᴏɴᴇ ❌', callback_data=f"settings#removechannel_{target_id}")],
         [InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ', callback_data="settings#channels")]
     ]
     await query.message.edit_text(
        f"<blockquote><b><u>📄 ᴢᴏɴᴇ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ</u></b></blockquote>\n\n<b>➣ ᴛɪᴛʟᴇ :</b> <code>{zone_data['title']}</code>\n<b>➣ ᴢᴏɴᴇ ɪᴅ :</b> <code>{zone_data['chat_id']}</code>\n<b>➣ ᴜꜱᴇʀɴᴀᴍᴇ :</b> {zone_data['username']}\n\n<b>🛡️ @IND_BOTZ</b>",
        reply_markup=InlineKeyboardMarkup(ctrl_buttons))
                                             
  elif callback_action.startswith("removechannel"):
     target_id = callback_action.split('_')[1]
     await db.remove_channel(client_id, target_id)
     await query.message.edit_text("<b>✅ ᴢᴏɴᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ɴᴇᴛᴡᴏʀᴋ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
                               
  # --- [ ᴄᴀᴘᴛɪᴏɴ ɪɴᴊᴇᴄᴛɪᴏɴ ] ---
  elif callback_action == "caption":
     cap_buttons = []
     sys_data = await get_configs(client_id)
     current_caption = sys_data['caption']
     
     if current_caption is None:
        cap_buttons.append([InlineKeyboardButton('✚ ɪɴᴊᴇᴄᴛ ᴄᴀᴘᴛɪᴏɴ ✚', callback_data="settings#addcaption")])
     else:
        cap_buttons.append([InlineKeyboardButton('👀 ᴠɪᴇᴡ ᴄᴀᴘᴛɪᴏɴ', callback_data="settings#seecaption")])
        cap_buttons[-1].append(InlineKeyboardButton('🗑️ ᴡɪᴘᴇ ᴄᴀᴘᴛɪᴏɴ', callback_data="settings#deletecaption"))
        
     cap_buttons.append([InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ', callback_data="settings#main")])
     
     await query.message.edit_text(
        "<blockquote><b><u>📝 ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ɪɴᴊᴇᴄᴛɪᴏɴ</u></b></blockquote>\n\n<b>ꜱᴇᴛ ᴀᴜᴛᴏᴍᴀᴛᴇᴅ ᴄᴀᴘᴛɪᴏɴꜱ ꜰᴏʀ ʏᴏᴜʀ ᴍᴇᴅɪᴀ ꜰɪʟᴇꜱ.</b>\n\n<b><u>ᴀᴠᴀɪʟᴀʙʟᴇ ᴠᴀʀɪᴀʙʟᴇꜱ :</u></b>\n<code>{filename}</code> : ꜰɪʟᴇɴᴀᴍᴇ\n<code>{size}</code> : ꜰɪʟᴇ ꜱɪᴢᴇ\n<code>{caption}</code> : ᴏʀɪɢɪɴᴀʟ ᴄᴀᴘᴛɪᴏɴ\n\n<b>🛡️ @IND_BOTZ</b>",
        reply_markup=InlineKeyboardMarkup(cap_buttons))
                               
  elif callback_action == "seecaption":   
     sys_data = await get_configs(client_id)
     cap_buttons = [
         [InlineKeyboardButton('✏️ ᴍᴏᴅɪꜰʏ ᴄᴀᴘᴛɪᴏɴ', callback_data="settings#addcaption")],
         [InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ', callback_data="settings#caption")]
     ]
     await query.message.edit_text(
        f"<blockquote><b><u>📝 ᴀᴄᴛɪᴠᴇ ᴄᴀᴘᴛɪᴏɴ ᴘᴀʏʟᴏᴀᴅ</u></b></blockquote>\n\n<code>{sys_data['caption']}</code>\n\n<b>🛡️ @IND_BOTZ</b>",
        reply_markup=InlineKeyboardMarkup(cap_buttons))
    
  elif callback_action == "deletecaption":
     await update_configs(client_id, 'caption', None)
     await query.message.edit_text("<b>✅ ᴄᴀᴘᴛɪᴏɴ ᴘᴀʏʟᴏᴀᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴡɪᴘᴇᴅ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
                              
  elif callback_action == "addcaption":
     await query.message.delete()
     try:
         prompt_msg = await bot.send_message(query.message.chat.id, "<blockquote><b><u>🎯 ɪɴᴊᴇᴄᴛ ɴᴇᴡ ᴄᴀᴘᴛɪᴏɴ</u></b></blockquote>\n\n<b>ꜱᴇɴᴅ ʏᴏᴜʀ ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ꜰᴏʀᴍᴀᴛ ʜᴇʀᴇ.</b>\n<code>/cancel</code> - <b>ᴀʙᴏʀᴛ ᴏᴘᴇʀᴀᴛɪᴏɴ</b>\n\n<b>🛡️ @IND_BOTZ</b>")
         new_cap = await bot.listen(chat_id=client_id, timeout=300)
         
         if new_cap.text == "/cancel":
            await new_cap.delete()
            return await prompt_msg.edit_text("<b>❌ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴀʙᴏʀᴛᴇᴅ !</b>", reply_markup=InlineKeyboardMarkup(return_payload))
         try:
            new_cap.text.format(filename='', size='', caption='')
         except KeyError as err:
            await new_cap.delete()
            return await prompt_msg.edit_text(f"<b>🚫 ɪɴᴠᴀʟɪᴅ ᴠᴀʀɪᴀʙʟᴇ `{err}` ᴜꜱᴇᴅ. ᴘʟᴇᴀꜱᴇ ᴄᴏʀʀᴇᴄᴛ ɪᴛ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
            
         await update_configs(client_id, 'caption', new_cap.text)
         await new_cap.delete()
         await prompt_msg.edit_text("<b>✅ ᴄᴀᴘᴛɪᴏɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ɪɴᴊᴇᴄᴛᴇᴅ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
         
     except asyncio.exceptions.TimeoutError:
         await prompt_msg.edit_text('<b>⏳ ꜱᴇꜱꜱɪᴏɴ ᴛɪᴍᴇᴅ ᴏᴜᴛ.</b>', reply_markup=InlineKeyboardMarkup(return_payload))
  
  # --- [ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ] ---
  elif callback_action == "button":
     btn_matrix = []
     active_btn = (await get_configs(client_id))['button']
     
     if active_btn is None:
        btn_matrix.append([InlineKeyboardButton('✚ ɪɴᴊᴇᴄᴛ ʙᴜᴛᴛᴏɴ ✚', callback_data="settings#addbutton")])
     else:
        btn_matrix.append([InlineKeyboardButton('👀 ᴠɪᴇᴡ ʙᴜᴛᴛᴏɴ', callback_data="settings#seebutton")])
        btn_matrix[-1].append(InlineKeyboardButton('🗑️ ᴡɪᴘᴇ ʙᴜᴛᴛᴏɴ ', callback_data="settings#deletebutton"))
        
     btn_matrix.append([InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ', callback_data="settings#main")])
     await query.message.edit_text(
        "<blockquote><b><u>🎛️ ᴄᴜꜱᴛᴏᴍ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴꜱ</u></b></blockquote>\n\n<b>ᴀᴛᴛᴀᴄʜ ʙᴜᴛᴛᴏɴꜱ ᴛᴏ ʏᴏᴜʀ ꜰᴏʀᴡᴀʀᴅᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ.</b>\n\n<b><u>ꜰᴏʀᴍᴀᴛ ꜱʏɴᴛᴀx :</u></b>\n<code>[IND BOTZ][buttonurl:https://t.me/IND_BOTZ]</code>\n\n<b>🛡️ @IND_BOTZ</b>",
        reply_markup=InlineKeyboardMarkup(btn_matrix))
  
  elif callback_action == "addbutton":
     await query.message.delete()
     try:
         prompt_msg = await bot.send_message(client_id, text="<blockquote><b><u>🎯 ɪɴᴊᴇᴄᴛ ʙᴜᴛᴛᴏɴ ꜱʏɴᴛᴀx</u></b></blockquote>\n\n<b>ꜱᴇɴᴅ ʏᴏᴜʀ ʙᴜᴛᴛᴏɴ ᴄᴏᴅᴇ.</b>\n<b>ᴇxᴀᴍᴘʟᴇ:</b>\n<code>[ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ][buttonurl:https://t.me/IND_BOTZ]</code>\n\n<b>🛡️ @IND_BOTZ</b>")
         btn_response = await bot.listen(chat_id=client_id, timeout=300)
         parsed_btn = parse_buttons(btn_response.text.html)
         
         if not parsed_btn:
            await btn_response.delete()
            return await prompt_msg.edit_text("<b>🚫 ɪɴᴠᴀʟɪᴅ ʙᴜᴛᴛᴏɴ ꜱʏɴᴛᴀx.</b>")
            
         await update_configs(client_id, 'button', btn_response.text.html)
         await btn_response.delete()
         await prompt_msg.edit_text("<b>✅ ʙᴜᴛᴛᴏɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴛᴛᴀᴄʜᴇᴅ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
         
     except asyncio.exceptions.TimeoutError:
         await prompt_msg.edit_text('<b>⏳ ꜱᴇꜱꜱɪᴏɴ ᴛɪᴍᴇᴅ ᴏᴜᴛ.</b>', reply_markup=InlineKeyboardMarkup(return_payload))
  
  elif callback_action == "seebutton":
      active_btn = (await get_configs(client_id))['button']
      parsed_matrix = parse_buttons(active_btn, markup=False)
      parsed_matrix.append([InlineKeyboardButton("🔙 ʀᴇᴛᴜʀɴ", "settings#button")])
      await query.message.edit_text("<blockquote><b><u>🎛️ ᴀᴄᴛɪᴠᴇ ʙᴜᴛᴛᴏɴ ᴘʀᴇᴠɪᴇᴡ</u></b></blockquote>\n\n<b>🛡️ @IND_BOTZ</b>", reply_markup=InlineKeyboardMarkup(parsed_matrix))
      
  elif callback_action == "deletebutton":
     await update_configs(client_id, 'button', None)
     await query.message.edit_text("<b>✅ ʙᴜᴛᴛᴏɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴡɪᴘᴇᴅ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
   
  # --- [ ᴅᴀᴛᴀʙᴀꜱᴇ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴ ] ---
  elif callback_action == "database":
     db_buttons = []
     mongo_uri = (await get_configs(client_id))['db_uri']
     
     if mongo_uri is None:
        db_buttons.append([InlineKeyboardButton('✚ ɪɴᴊᴇᴄᴛ ᴍᴏɴɢᴏ ᴜʀʟ ✚', callback_data="settings#addurl")])
     else:
        db_buttons.append([InlineKeyboardButton('👀 ᴠɪᴇᴡ ᴍᴏɴɢᴏ ᴜʀʟ', callback_data="settings#seeurl")])
        db_buttons[-1].append(InlineKeyboardButton('🗑️ ᴡɪᴘᴇ ᴍᴏɴɢᴏ ᴜʀʟ', callback_data="settings#deleteurl"))
        
     db_buttons.append([InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ', callback_data="settings#main")])
     await query.message.edit_text(
        "<blockquote><b><u>🗃️ ᴅᴀᴛᴀʙᴀꜱᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ</u></b></blockquote>\n\n<b>ᴄᴏɴɴᴇᴄᴛ ᴍᴏɴɢᴏᴅʙ ᴛᴏ ꜱᴛᴏʀᴇ ᴅᴜᴘʟɪᴄᴀᴛᴇ ꜰɪʟᴇ ʜᴀꜱʜᴇꜱ ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ. ᴘʀᴇᴠᴇɴᴛꜱ ᴅᴀᴛᴀ ʟᴏꜱꜱ ᴅᴜʀɪɴɢ ꜱʏꜱᴛᴇᴍ ʀᴇʙᴏᴏᴛꜱ.</b>\n\n<b>🛡️ @IND_BOTZ</b>",
        reply_markup=InlineKeyboardMarkup(db_buttons))

  elif callback_action == "addurl":
     await query.message.delete()
     prompt_msg = await bot.ask(client_id, "<blockquote><b><u>🔗 ᴍᴏɴɢᴏ ᴜʀʟ ɪɴᴊᴇᴄᴛɪᴏɴ</u></b></blockquote>\n\n<b>ꜱᴇɴᴅ ʏᴏᴜʀ ᴍᴏɴɢᴏᴅʙ ᴄʟᴜꜱᴛᴇʀ ᴜʀʟ ʜᴇʀᴇ.</b>\n\n<b>🛡️ @IND_BOTZ</b>", disable_web_page_preview=True)
     
     if prompt_msg.text == "/cancel":
        return await prompt_msg.reply_text("<b>❌ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴀʙᴏʀᴛᴇᴅ !</b>", reply_markup=InlineKeyboardMarkup(return_payload))
     if not prompt_msg.text.startswith("mongodb+srv://") and not prompt_msg.text.endswith("majority"):
        return await prompt_msg.reply("<b>🚫 ɪɴᴠᴀʟɪᴅ ᴍᴏɴɢᴏᴅʙ ᴜʀʟ ꜰᴏʀᴍᴀᴛ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
        
     await update_configs(client_id, 'db_uri', prompt_msg.text)
     await prompt_msg.reply("<b>✅ ᴅᴀᴛᴀʙᴀꜱᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇꜱᴛᴀʙʟɪꜱʜᴇᴅ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
  
  elif callback_action == "seeurl":
     mongo_uri = (await get_configs(client_id))['db_uri']
     await query.answer(f"🔒 MONGODB URL: {mongo_uri}", show_alert=True)
  
  elif callback_action == "deleteurl":
     await update_configs(client_id, 'db_uri', None)
     await query.message.edit_text("<b>✅ ᴅᴀᴛᴀʙᴀꜱᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ꜱᴇᴠᴇʀᴇᴅ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
      
  # --- [ ᴀᴅᴠᴀɴᴄᴇᴅ ꜰɪʟᴛᴇʀ ꜱʏꜱᴛᴇᴍ ] ---
  elif callback_action == "filters":
     await query.message.edit_text(
        "<blockquote><b><u>🕵️ ᴀᴅᴠᴀɴᴄᴇᴅ ꜰɪʟᴛᴇʀ ᴇɴɢɪɴᴇ</u></b></blockquote>\n\n<b>ᴛᴏɢɢʟᴇ ᴛʜᴇ ᴛʏᴘᴇꜱ ᴏꜰ ᴍᴇᴅɪᴀ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʀᴏᴄᴇꜱꜱ ᴏʀ ɪɢɴᴏʀᴇ.</b>\n\n<b>🛡️ @IND_BOTZ</b>",
        reply_markup=await generate_filters_buttons(client_id))
  
  elif callback_action == "nextfilters":
     await query.edit_message_reply_markup(reply_markup=await generate_next_filters_buttons(client_id))
   
  elif callback_action.startswith("updatefilter"):
     filter_prefix, filter_key, filter_val = callback_action.split('-')
     
     if filter_val == "True":
        await update_configs(client_id, filter_key, False)
     else:
        await update_configs(client_id, filter_key, True)
        
     if filter_key in ['poll', 'protect']:
        return await query.edit_message_reply_markup(reply_markup=await generate_next_filters_buttons(client_id)) 
        
     await query.edit_message_reply_markup(reply_markup=await generate_filters_buttons(client_id))
   
  # --- [ ꜱɪᴢᴇ ʟɪᴍɪᴛꜱ & ᴇxᴛᴇɴꜱɪᴏɴꜱ ] ---
  elif callback_action.startswith("file_size"):
    sys_settings = await get_configs(client_id)
    current_size = sys_settings.get('file_size', 0)
    logic_prefix, limit_txt = analyze_size_limit(sys_settings['size_limit'])
    
    await query.message.edit_text(
       f"<blockquote><b><u>🛑 ꜱɪᴢᴇ ʟɪᴍɪᴛ ᴄᴏɴᴛʀᴏʟ</u></b></blockquote>\n\n<b>ꜰɪʟᴛᴇʀ ꜰɪʟᴇꜱ ʙᴀꜱᴇᴅ ᴏɴ ᴛʜᴇɪʀ ꜱɪᴢᴇ (ɪɴ ᴍʙ).</b>\n\n<b>📊 ꜱᴛᴀᴛᴜꜱ :</b> ꜰɪʟᴇꜱ {limit_txt} <code>{current_size} ᴍʙ</code> ᴡɪʟʟ ʙᴇ ꜰᴏʀᴡᴀʀᴅᴇᴅ.\n\n<b>🛡️ @IND_BOTZ</b>",
       reply_markup=generate_size_buttons(current_size))
  
  elif callback_action.startswith("update_size"):
    new_size = int(query.data.split('-')[1])
    if 0 < new_size > 2000:
      return await query.answer("⚠️ ᴍᴀxɪᴍᴜᴍ ꜱɪᴢᴇ ʟɪᴍɪᴛ ɪꜱ 2000 ᴍʙ", show_alert=True)
      
    await update_configs(client_id, 'file_size', new_size)
    logic_prefix, limit_txt = analyze_size_limit((await get_configs(client_id))['size_limit'])
    
    await query.message.edit_text(
       f"<blockquote><b><u>🛑 ꜱɪᴢᴇ ʟɪᴍɪᴛ ᴄᴏɴᴛʀᴏʟ</u></b></blockquote>\n\n<b>ꜰɪʟᴛᴇʀ ꜰɪʟᴇꜱ ʙᴀꜱᴇᴅ ᴏɴ ᴛʜᴇɪʀ ꜱɪᴢᴇ (ɪɴ ᴍʙ).</b>\n\n<b>📊 ꜱᴛᴀᴛᴜꜱ :</b> ꜰɪʟᴇꜱ {limit_txt} <code>{new_size} ᴍʙ</code> ᴡɪʟʟ ʙᴇ ꜰᴏʀᴡᴀʀᴅᴇᴅ.\n\n<b>🛡️ @IND_BOTZ</b>",
       reply_markup=generate_size_buttons(new_size))
  
  elif callback_action.startswith('update_limit'):
    logic_prefix, limit_logic, size_val = callback_action.split('-')
    limit_logic, status_txt = analyze_size_limit(limit_logic)
    
    await update_configs(client_id, 'size_limit', limit_logic) 
    await query.message.edit_text(
       f"<blockquote><b><u>🛑 ꜱɪᴢᴇ ʟɪᴍɪᴛ ᴄᴏɴᴛʀᴏʟ</u></b></blockquote>\n\n<b>ꜰɪʟᴛᴇʀ ꜰɪʟᴇꜱ ʙᴀꜱᴇᴅ ᴏɴ ᴛʜᴇɪʀ ꜱɪᴢᴇ (ɪɴ ᴍʙ).</b>\n\n<b>📊 ꜱᴛᴀᴛᴜꜱ :</b> ꜰɪʟᴇꜱ {status_txt} <code>{size_val} ᴍʙ</code> ᴡɪʟʟ ʙᴇ ꜰᴏʀᴡᴀʀᴅᴇᴅ.\n\n<b>🛡️ @IND_BOTZ</b>",
       reply_markup=generate_size_buttons(int(size_val)))
      
  # --- [ ᴇxᴛᴇɴꜱɪᴏɴ ꜰɪʟᴛᴇʀꜱ ] ---
  elif callback_action == "add_extension":
    await query.message.delete() 
    prompt_ext = await bot.ask(client_id, text="<blockquote><b><u>💾 ʙʟᴏᴄᴋ ᴇxᴛᴇɴꜱɪᴏɴꜱ</u></b></blockquote>\n\n<b>ꜱᴇɴᴅ ᴇxᴛᴇɴꜱɪᴏɴꜱ (ꜱᴇᴘᴀʀᴀᴛᴇᴅ ʙʏ ꜱᴘᴀᴄᴇ). ᴇx: ᴍᴋᴠ ᴍᴘ4 ᴢɪᴘ</b>\n\n<b>🛡️ @IND_BOTZ</b>")
    
    if prompt_ext.text == '/cancel':
       return await prompt_ext.reply_text("<b>❌ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴀʙᴏʀᴛᴇᴅ !</b>", reply_markup=InlineKeyboardMarkup(return_payload))
       
    ext_list = prompt_ext.text.split(" ")
    current_exts = (await get_configs(client_id))['extension']
    
    if current_exts:
        for ext_itm in ext_list:
            current_exts.append(ext_itm)
    else:
        current_exts = ext_list
        
    await update_configs(client_id, 'extension', current_exts)
    await prompt_ext.reply_text("<b>✅ ᴇxᴛᴇɴꜱɪᴏɴꜱ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʙʟᴏᴄᴋᴇᴅ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
      
  elif callback_action == "get_extension":
    current_exts = (await get_configs(client_id))['extension']
    ext_btn_matrix = extract_dynamic_buttons(current_exts)
    
    ext_btn_matrix.append([InlineKeyboardButton('✚ ᴀᴅᴅ ᴇxᴛᴇɴꜱɪᴏɴ ✚', 'settings#add_extension')])
    ext_btn_matrix.append([InlineKeyboardButton('🗑️ ᴡɪᴘᴇ ᴀʟʟ', 'settings#rmve_all_extension')])
    ext_btn_matrix.append([InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ', 'settings#main')])
    
    await query.message.edit_text(
        text="<blockquote><b><u>💾 ʙʟᴏᴄᴋᴇᴅ ᴇxᴛᴇɴꜱɪᴏɴꜱ</u></b></blockquote>\n\n<b>ꜰɪʟᴇꜱ ᴡɪᴛʜ ᴛʜᴇꜱᴇ ᴇxᴛᴇɴꜱɪᴏɴꜱ ᴡɪʟʟ ʙᴇ ɪɢɴᴏʀᴇᴅ ʙʏ ᴛʜᴇ ᴇɴɢɪɴᴇ.</b>\n\n<b>🛡️ @IND_BOTZ</b>",
        reply_markup=InlineKeyboardMarkup(ext_btn_matrix))
  
  elif callback_action == "rmve_all_extension":
    await update_configs(client_id, 'extension', None)
    await query.message.edit_text(text="<b>✅ ᴀʟʟ ᴇxᴛᴇɴꜱɪᴏɴꜱ ᴡɪᴘᴇᴅ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
    
  # --- [ ᴋᴇʏᴡᴏʀᴅ ꜰɪʟᴛᴇʀꜱ ] ---
  elif callback_action == "add_keyword":
    await query.message.delete()
    prompt_kw = await bot.ask(client_id, text="<blockquote><b><u>📌 ᴀʟʟᴏᴡ ᴋᴇʏᴡᴏʀᴅꜱ</u></b></blockquote>\n\n<b>ꜱᴇɴᴅ ᴋᴇʏᴡᴏʀᴅꜱ (ꜱᴇᴘᴀʀᴀᴛᴇᴅ ʙʏ ꜱᴘᴀᴄᴇ).</b>\n\n<b>🛡️ @IND_BOTZ</b>")
    
    if prompt_kw.text == '/cancel':
       return await prompt_kw.reply_text("<b>❌ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴀʙᴏʀᴛᴇᴅ !</b>", reply_markup=InlineKeyboardMarkup(return_payload))
       
    kw_list = prompt_kw.text.split(" ")
    current_kws = (await get_configs(client_id))['keywords']
    
    if current_kws:
        for word in kw_list:
            current_kws.append(word)
    else:
        current_kws = kw_list
        
    await update_configs(client_id, 'keywords', current_kws)
    await prompt_kw.reply_text("<b>✅ ᴋᴇʏᴡᴏʀᴅꜱ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
  
  elif callback_action == "get_keyword":
    current_kws = (await get_configs(client_id))['keywords']
    kw_btn_matrix = extract_dynamic_buttons(current_kws)
    
    kw_btn_matrix.append([InlineKeyboardButton('✚ ᴀᴅᴅ ᴋᴇʏᴡᴏʀᴅ ✚', 'settings#add_keyword')])
    kw_btn_matrix.append([InlineKeyboardButton('🗑️ ᴡɪᴘᴇ ᴀʟʟ', 'settings#rmve_all_keyword')])
    kw_btn_matrix.append([InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ', 'settings#main')])
    
    await query.message.edit_text(
        text="<blockquote><b><u>📌 ᴀʟʟᴏᴡᴇᴅ ᴋᴇʏᴡᴏʀᴅꜱ</u></b></blockquote>\n\n<b>ᴏɴʟʏ ꜰɪʟᴇꜱ ᴄᴏɴᴛᴀɪɴɪɴɢ ᴛʜᴇꜱᴇ ᴋᴇʏᴡᴏʀᴅꜱ ᴡɪʟʟ ʙᴇ ꜰᴏʀᴡᴀʀᴅᴇᴅ.</b>\n\n<b>🛡️ @IND_BOTZ</b>",
        reply_markup=InlineKeyboardMarkup(kw_btn_matrix))
      
  elif callback_action == "rmve_all_keyword":
    await update_configs(client_id, 'keywords', None)
    await query.message.edit_text(text="<b>✅ ᴀʟʟ ᴋᴇʏᴡᴏʀᴅꜱ ᴡɪᴘᴇᴅ.</b>", reply_markup=InlineKeyboardMarkup(return_payload))
    
  # --- [ ᴀʟᴇʀᴛ ʜᴀɴᴅʟᴇʀ ] ---
  elif callback_action.startswith("alert"):
    alert_txt = callback_action.split('_')[1]
    await query.answer(alert_txt, show_alert=True)
      
# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🎨 ᴜɪ ʙᴜᴛᴛᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀꜱ (ꜱᴍᴀʟʟ ᴄᴀᴘꜱ & ᴇᴍᴏᴊɪꜱ)
# ------------------------------------------------------------------------------------------------------------------------------------------------

def generate_main_buttons():
  core_layout = [[
       InlineKeyboardButton('🤖 ᴄᴏɴɴᴇᴄᴛᴇᴅ ɴᴏᴅᴇꜱ', callback_data=f'settings#bots'),
       InlineKeyboardButton('📡 ᴛᴀʀɢᴇᴛ ᴢᴏɴᴇꜱ', callback_data=f'settings#channels')
       ],[
       InlineKeyboardButton('📝 ᴄᴀᴘᴛɪᴏɴ ɪɴᴊᴇᴄᴛ', callback_data=f'settings#caption'),
       InlineKeyboardButton('🗃️ ᴅᴀᴛᴀʙᴀꜱᴇ ʟɪɴᴋ', callback_data=f'settings#database')
       ],[
       InlineKeyboardButton('🕵️ ꜰɪʟᴛᴇʀ ᴇɴɢɪɴᴇ', callback_data=f'settings#filters'),
       InlineKeyboardButton('🎛️ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴꜱ', callback_data=f'settings#button')
       ],[
       InlineKeyboardButton('⚙️ ᴀᴅᴠᴀɴᴄᴇᴅ ᴘᴀʀᴀᴍᴇᴛᴇʀꜱ', callback_data='settings#nextfilters')
       ],[      
       InlineKeyboardButton('✖️ ᴄʟᴏꜱᴇ ᴘᴀɴᴇʟ ✖️', callback_data='back')
       ]]
  return InlineKeyboardMarkup(core_layout)

def analyze_size_limit(limit_val):
   if str(limit_val) == "None":
      return None, "ᴇxᴀᴄᴛʟʏ"
   elif str(limit_val) == "True":
      return True, "ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ"
   else:
      return False, "ʟᴇꜱꜱ ᴛʜᴀɴ"

def extract_dynamic_buttons(data_array):
    idx = 0
    matrix = []
    if data_array:
       for item in data_array:
         if idx >= 5:
            idx = 0
         if idx == 0:
            matrix.append([InlineKeyboardButton(item, f'settings#alert_{item}')])
            idx += 1
            continue
         elif idx > 0:
            matrix[-1].append(InlineKeyboardButton(item, f'settings#alert_{item}'))
            idx += 1
    return matrix 

def generate_size_buttons(current_sz):
  sz_layout = [[
       InlineKeyboardButton('➕ ɢʀᴇᴀᴛᴇʀ', callback_data=f'settings#update_limit-True-{current_sz}'),
       InlineKeyboardButton('🟰 ᴇQᴜᴀʟ', callback_data=f'settings#update_limit-None-{current_sz}'),
       InlineKeyboardButton('➖ ʟᴇꜱꜱ', callback_data=f'settings#update_limit-False-{current_sz}')
       ],[
       InlineKeyboardButton('+1 ᴍʙ', callback_data=f'settings#update_size-{current_sz + 1}'),
       InlineKeyboardButton('-1 ᴍʙ', callback_data=f'settings#update_size_-{current_sz - 1}')
       ],[
       InlineKeyboardButton('+5 ᴍʙ', callback_data=f'settings#update_size-{current_sz + 5}'),
       InlineKeyboardButton('-5 ᴍʙ', callback_data=f'settings#update_size_-{current_sz - 5}')
       ],[
       InlineKeyboardButton('+10 ᴍʙ', callback_data=f'settings#update_size-{current_sz + 10}'),
       InlineKeyboardButton('-10 ᴍʙ', callback_data=f'settings#update_size_-{current_sz - 10}')
       ],[
       InlineKeyboardButton('+50 ᴍʙ', callback_data=f'settings#update_size-{current_sz + 50}'),
       InlineKeyboardButton('-50 ᴍʙ', callback_data=f'settings#update_size_-{current_sz - 50}')
       ],[
       InlineKeyboardButton('+100 ᴍʙ', callback_data=f'settings#update_size-{current_sz + 100}'),
       InlineKeyboardButton('-100 ᴍʙ', callback_data=f'settings#update_size_-{current_sz - 100}')
       ],[
       InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ ᴛᴏ ᴍᴀɪɴ ᴍᴇɴᴜ', callback_data="settings#main")
     ]]
  return InlineKeyboardMarkup(sz_layout)
       
async def generate_filters_buttons(client_id):
  raw_config = await get_configs(client_id)
  sys_filters = raw_config['filters']
  
  flt_layout = [[
       InlineKeyboardButton('🏷️ ꜰᴏʀᴡᴀʀᴅ ᴛᴀɢ', callback_data=f'settings_#updatefilter-forward_tag-{raw_config["forward_tag"]}'),
       InlineKeyboardButton('🟢 ᴏɴ' if raw_config['forward_tag'] else '🔴 ᴏꜰꜰ', callback_data=f'settings#updatefilter-forward_tag-{raw_config["forward_tag"]}')
       ],[
       InlineKeyboardButton('🖍️ ᴛᴇxᴛ ᴍᴇꜱꜱᴀɢᴇꜱ', callback_data=f'settings_#updatefilter-text-{sys_filters["text"]}'),
       InlineKeyboardButton('🟢 ᴏɴ' if sys_filters['text'] else '🔴 ᴏꜰꜰ', callback_data=f'settings#updatefilter-text-{sys_filters["text"]}')
       ],[
       InlineKeyboardButton('📁 ᴅᴏᴄᴜᴍᴇɴᴛꜱ', callback_data=f'settings_#updatefilter-document-{sys_filters["document"]}'),
       InlineKeyboardButton('🟢 ᴏɴ' if sys_filters['document'] else '🔴 ᴏꜰꜰ', callback_data=f'settings#updatefilter-document-{sys_filters["document"]}')
       ],[
       InlineKeyboardButton('🎞️ ᴠɪᴅᴇᴏ ꜰɪʟᴇꜱ', callback_data=f'settings_#updatefilter-video-{sys_filters["video"]}'),
       InlineKeyboardButton('🟢 ᴏɴ' if sys_filters['video'] else '🔴 ᴏꜰꜰ', callback_data=f'settings#updatefilter-video-{sys_filters["video"]}')
       ],[
       InlineKeyboardButton('📷 ᴘʜᴏᴛᴏɢʀᴀᴘʜꜱ', callback_data=f'settings_#updatefilter-photo-{sys_filters["photo"]}'),
       InlineKeyboardButton('🟢 ᴏɴ' if sys_filters['photo'] else '🔴 ᴏꜰꜰ', callback_data=f'settings#updatefilter-photo-{sys_filters["photo"]}')
       ],[
       InlineKeyboardButton('🎧 ᴀᴜᴅɪᴏ ᴛʀᴀᴄᴋꜱ', callback_data=f'settings_#updatefilter-audio-{sys_filters["audio"]}'),
       InlineKeyboardButton('🟢 ᴏɴ' if sys_filters['audio'] else '🔴 ᴏꜰꜰ', callback_data=f'settings#updatefilter-audio-{sys_filters["audio"]}')
       ],[
       InlineKeyboardButton('🎤 ᴠᴏɪᴄᴇ ɴᴏᴛᴇꜱ', callback_data=f'settings_#updatefilter-voice-{sys_filters["voice"]}'),
       InlineKeyboardButton('🟢 ᴏɴ' if sys_filters['voice'] else '🔴 ᴏꜰꜰ', callback_data=f'settings#updatefilter-voice-{sys_filters["voice"]}')
       ],[
       InlineKeyboardButton('🎭 ᴀɴɪᴍᴀᴛɪᴏɴꜱ / ɢɪꜰ', callback_data=f'settings_#updatefilter-animation-{sys_filters["animation"]}'),
       InlineKeyboardButton('🟢 ᴏɴ' if sys_filters['animation'] else '🔴 ᴏꜰꜰ', callback_data=f'settings#updatefilter-animation-{sys_filters["animation"]}')
       ],[
       InlineKeyboardButton('🃏 ꜱᴛɪᴄᴋᴇʀꜱ', callback_data=f'settings_#updatefilter-sticker-{sys_filters["sticker"]}'),
       InlineKeyboardButton('🟢 ᴏɴ' if sys_filters['sticker'] else '🔴 ᴏꜰꜰ', callback_data=f'settings#updatefilter-sticker-{sys_filters["sticker"]}')
       ],[
       InlineKeyboardButton('▶️ ʙʏᴘᴀꜱꜱ ᴅᴜᴘʟɪᴄᴀᴛᴇꜱ', callback_data=f'settings_#updatefilter-duplicate-{raw_config["duplicate"]}'),
       InlineKeyboardButton('🟢 ᴏɴ' if raw_config['duplicate'] else '🔴 ᴏꜰꜰ', callback_data=f'settings#updatefilter-duplicate-{raw_config["duplicate"]}')
       ],[
       InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ ᴛᴏ ᴍᴀɪɴ ᴍᴇɴᴜ', callback_data="settings#main")
       ]]
  return InlineKeyboardMarkup(flt_layout) 

async def generate_next_filters_buttons(client_id):
  raw_config = await get_configs(client_id)
  sys_filters = raw_config['filters']
  
  adv_layout = [[
       InlineKeyboardButton('📊 ᴘᴏʟʟꜱ & Qᴜɪᴢ', callback_data=f'settings_#updatefilter-poll-{sys_filters["poll"]}'),
       InlineKeyboardButton('🟢 ᴏɴ' if sys_filters['poll'] else '🔴 ᴏꜰꜰ', callback_data=f'settings#updatefilter-poll-{sys_filters["poll"]}')
       ],[
       InlineKeyboardButton('🔒 ꜱᴇᴄᴜʀᴇ / ʀᴇꜱᴛʀɪᴄᴛᴇᴅ ᴄʜᴀᴛꜱ', callback_data=f'settings_#updatefilter-protect-{raw_config["protect"]}'),
       InlineKeyboardButton('🟢 ᴏɴ' if raw_config['protect'] else '🔴 ᴏꜰꜰ', callback_data=f'settings#updatefilter-protect-{raw_config["protect"]}')
       ],[
       InlineKeyboardButton('🛑 ᴄᴏɴꜰɪɢᴜʀᴇ ꜱɪᴢᴇ ʟɪᴍɪᴛ', callback_data='settings#file_size')
       ],[
       InlineKeyboardButton('💾 ʙʟᴏᴄᴋ ᴇxᴛᴇɴꜱɪᴏɴꜱ', callback_data='settings#get_extension')
       ],[
       InlineKeyboardButton('📌 ᴀʟʟᴏᴡ ᴋᴇʏᴡᴏʀᴅꜱ', callback_data='settings#get_keyword')
       ],[
       InlineKeyboardButton('🔙 ʀᴇᴛᴜʀɴ ᴛᴏ ᴍᴀɪɴ ᴍᴇɴᴜ', callback_data="settings#main")
       ]]
  return InlineKeyboardMarkup(adv_layout) 
   
# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🏁 ᴇɴᴅ ᴏꜰ ꜰɪʟᴇ : ꜱʏꜱᴛᴇᴍ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴ ᴇɴɢɪɴᴇ
# ------------------------------------------------------------------------------------------------------------------------------------------------
