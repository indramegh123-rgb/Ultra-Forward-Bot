# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# █ 🛡️ ᴀᴅᴠᴀɴᴄᴇᴅ ꜱʏꜱᴛᴇᴍ ᴄᴏʀᴇ ᴠ3.0
# █ 🎯 ᴏᴡɴᴇᴅ & ᴏᴘᴇʀᴀᴛᴇᴅ ʙʏ @IND_BOTZ 
# █ ⚠️ ᴀʟʟ ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ - ᴘʀɪᴠᴀᴛᴇ ᴇᴅɪᴛɪᴏɴ
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

import re
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import db
from config import temp
from .test import CLIENT as SYS_CLIENT, start_clone_bot
from translation import Translation

# ------------------------------------------------------------------------------------------------------------------------------------------------
# ⚙️ ɢʟᴏʙᴀʟ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴꜱ & ᴜɪ ᴇʟᴇᴍᴇɴᴛꜱ
# ------------------------------------------------------------------------------------------------------------------------------------------------

IND_CLIENT = SYS_CLIENT()

# Premium Inline Keyboards
COMPLETED_BTN = InlineKeyboardMarkup(
   [
      [InlineKeyboardButton('📢 ᴏꜰꜰɪᴄɪᴀʟ ᴜᴘᴅᴀᴛᴇꜱ', url='https://t.me/IND_BOTZ')],
      [InlineKeyboardButton('💬 ɴᴇᴛᴡᴏʀᴋ ꜱᴜᴘᴘᴏʀᴛ', url='https://t.me/IND_BOTZ')]
   ]
)

CANCEL_BTN = InlineKeyboardMarkup([[InlineKeyboardButton('✖️ ᴀʙᴏʀᴛ ᴏᴘᴇʀᴀᴛɪᴏɴ ✖️', 'terminate_frwd')]])

# System Logger Initialization
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🚀 ᴍᴀɪɴ ᴇxᴇᴄᴜᴛɪᴏɴ ʙʟᴏᴄᴋ: ᴜɴᴇQᴜɪꜰʏ ᴇɴɢɪɴᴇ (ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴄʟᴇᴀɴᴇʀ)
# ------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.command("unequify") & filters.private)
async def unequify_system_engine(client, message):
   """
   Advanced Duplicate Removal Protocol by @IND_BOTZ.
   Scans the target zone, hashes the file IDs, and wipes out identical clones.
   """
   client_id = message.from_user.id
   temp.CANCEL[client_id] = False
   
   # Task Lock Security Check
   if temp.lock.get(client_id) and str(temp.lock.get(client_id)) == "True":
      return await message.reply("<b>⚠️ ᴀɴᴏᴛʜᴇʀ ᴛᴀꜱᴋ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴜɴɴɪɴɢ. ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>\n\n<b>🛡️ @IND_BOTZ</b>")
      
   # Fetch Active Node (Userbot) Data
   active_node = await db.get_bot(client_id)
   if not active_node or active_node['is_bot']:
      return await message.reply("<b>🚫 ᴜꜱᴇʀʙᴏᴛ ɴᴏᴛ ꜰᴏᴜɴᴅ!\n\nʏᴏᴜ ᴍᴜꜱᴛ ᴀᴛᴛᴀᴄʜ ᴀ ᴜꜱᴇʀʙᴏᴛ ᴠɪᴀ <code>/settings</code> ᴛᴏ ᴇxᴇᴄᴜᴛᴇ ᴛʜɪꜱ ᴘʀᴏᴛᴏᴄᴏʟ.</b>\n\n<b>🛡️ @IND_BOTZ</b>")
      
   # Destination Input Phase
   destination_input = await client.ask(
       client_id, 
       text="<blockquote><b><u>🎯 ᴛᴀʀɢᴇᴛ ᴢᴏɴᴇ ɪɴᴘᴜᴛ</u></b></blockquote>\n\n<b>ꜰᴏʀᴡᴀʀᴅ ᴛʜᴇ ʟᴀꜱᴛ ᴍᴇꜱꜱᴀɢᴇ ꜰʀᴏᴍ ᴛʜᴇ ᴛᴀʀɢᴇᴛ ᴄʜᴀᴛ ᴏʀ ᴘᴀꜱᴛᴇ ᴛʜᴇ ʟɪɴᴋ.</b>\n<code>/cancel</code> - <b>ᴀʙᴏʀᴛ ᴛʜɪꜱ ᴏᴘᴇʀᴀᴛɪᴏɴ</b>\n\n<b>🛡️ @IND_BOTZ</b>"
   )
   
   if destination_input.text.startswith("/"):
      return await message.reply("<b>❌ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴀʙᴏʀᴛᴇᴅ !</b>\n\n<b>♻️ @IND_BOTZ</b>")
      
   elif destination_input.text:
      link_pattern = re.compile(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
      url_match = link_pattern.match(destination_input.text.replace("?single", ""))
      if not url_match:
         return await message.reply('<b>🚫 ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ ᴅᴇᴛᴇᴄᴛᴇᴅ. ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ.</b>')
      zone_id = url_match.group(4)
      last_msg_idx = int(url_match.group(5))
      if zone_id.isnumeric():
         zone_id  = int(("-100" + zone_id))
         
   elif destination_input.forward_from_chat.type in ['channel', 'supergroup']:
        last_msg_idx = destination_input.forward_from_message_id
        zone_id = destination_input.forward_from_chat.username or destination_input.forward_from_chat.id
   else:
        return await message.reply_text("<b>🚫 ᴜɴᴋɴᴏᴡɴ ɪɴᴘᴜᴛ ꜰᴏʀᴍᴀᴛ.</b>")
        
   # Execution Confirmation
   execute_confirmation = await client.ask(
       client_id, 
       text="<blockquote><b><u>⚠️ ꜰɪɴᴀʟ ᴄᴏɴꜰɪʀᴍᴀᴛɪᴏɴ</u></b></blockquote>\n\n<b>ꜱᴇɴᴅ <code>/yes</code> ᴛᴏ ɪɢɴɪᴛᴇ ᴛʜᴇ ᴇɴɢɪɴᴇ ᴏʀ <code>/no</code> ᴛᴏ ᴀʙᴏʀᴛ.</b>\n\n<b>⚡ @IND_BOTZ</b>"
   )
   
   if execute_confirmation.text.lower() == '/no':
      return await execute_confirmation.reply("<b>🚫 ᴘʀᴏᴄᴇꜱꜱ ᴛᴇʀᴍɪɴᴀᴛᴇᴅ !</b>\n\n<b>♻️ @IND_BOTZ</b>")
      
   status_msg = await execute_confirmation.reply("<b>⏳ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ꜱʏꜱᴛᴇᴍ ᴄᴏʀᴇ...</b>")
   
   # Booting up Userbot Clones
   try:
      cloned_bot = await start_clone_bot(IND_CLIENT.client(active_node))
   except Exception as core_error:
      logger.error(f"Failed to start node: {core_error}")
      return await status_msg.edit(f"<b>❌ ᴄᴏʀᴇ ᴇʀʀᴏʀ:</b>\n`{core_error}`")
      
   # Admin Rights & Network Verification
   try:
       ping_msg = await cloned_bot.send_message(zone_id, text="<i>⚡ Checking Admin Privileges...</i>")
       await ping_msg.delete()
   except:
       await status_msg.edit(f"<b>🚫 ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ:</b>\n\n<b>ᴘʟᴇᴀꜱᴇ ᴍᴀᴋᴇ ʏᴏᴜʀ ᴜꜱᴇʀʙᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴛᴀʀɢᴇᴛ ᴢᴏɴᴇ ᴡɪᴛʜ ꜰᴜʟʟ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ ʙᴇꜰᴏʀᴇ ᴘʀᴏᴄᴇᴇᴅɪɴɢ.</b>\n\n<b>🛡️ @IND_BOTZ</b>")
       return await cloned_bot.stop()
       
   # Data Arrays & Counters Setup
   SCANNED_HASHES = []
   CLONE_TRASH = []
   total_scanned = 0
   total_wiped = 0
   temp.lock[client_id] = True
   
   # The Core Scanning Loop
   try:
     await status_msg.edit(Translation.DUPLICATE_TEXT.format(total_scanned, total_wiped, "⏳ ᴇxᴇᴄᴜᴛɪɴɢ..."), reply_markup=CANCEL_BTN)
     
     async for msg in cloned_bot.search_messages(chat_id=zone_id, filter="document"):
        if temp.CANCEL.get(client_id) == True:
           await status_msg.edit(Translation.DUPLICATE_TEXT.format(total_scanned, total_wiped, "🚫 ᴀʙᴏʀᴛᴇᴅ"), reply_markup=COMPLETED_BTN)
           return await cloned_bot.stop()
           
        file_obj = msg.document
        
        # Advanced hashing logic
        try:
            from pyropatch.utils import unpack_new_file_id
            unique_hash = unpack_new_file_id(file_obj.file_id)
        except ImportError:
            unique_hash = file_obj.file_unique_id 
            
        if unique_hash in SCANNED_HASHES:
           CLONE_TRASH.append(msg.id)
        else:
           SCANNED_HASHES.append(unique_hash)
           
        total_scanned += 1
        
        # UI Updater (Throttle to avoid flood waits)
        if total_scanned % 10000 == 0:
           await status_msg.edit(Translation.DUPLICATE_TEXT.format(total_scanned, total_wiped, "⏳ ꜱᴄᴀɴɴɪɴɢ ᴢᴏɴᴇ..."), reply_markup=CANCEL_BTN)
           
        # Batch Deletion Trigger (Deletes 100 duplicates at once)
        if len(CLONE_TRASH) >= 100:
           await cloned_bot.delete_messages(zone_id, CLONE_TRASH)
           total_wiped += 100
           await status_msg.edit(Translation.DUPLICATE_TEXT.format(total_scanned, total_wiped, "🧹 ᴡɪᴘɪɴɢ ᴄʟᴏɴᴇꜱ..."), reply_markup=CANCEL_BTN)
           CLONE_TRASH = []
           
     # Final Sweep for leftovers
     if CLONE_TRASH:
        await cloned_bot.delete_messages(zone_id, CLONE_TRASH)
        total_wiped += len(CLONE_TRASH)
        
   except Exception as runtime_err:
       temp.lock[client_id] = False 
       logger.error(f"Runtime Exception: {runtime_err}")
       await status_msg.edit(f"<b>❌ ꜰᴀᴛᴀʟ ᴇʀʀᴏʀ ᴇɴᴄᴏᴜɴᴛᴇʀᴇᴅ</b>\n\n`{runtime_err}`\n\n<b>🛡️ @IND_BOTZ</b>")
       return await cloned_bot.stop()
       
   # Cleanup & Unlock System
   temp.lock[client_id] = False
   await status_msg.edit(Translation.DUPLICATE_TEXT.format(total_scanned, total_wiped, "✅ ᴏᴘᴇʀᴀᴛɪᴏɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ"), reply_markup=COMPLETED_BTN)
   await cloned_bot.stop()

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🏁 ᴇɴᴅ ᴏꜰ ꜰɪʟᴇ : ᴜɴᴇQᴜɪꜰʏ ᴇɴɢɪɴᴇ
# ------------------------------------------------------------------------------------------------------------------------------------------------
