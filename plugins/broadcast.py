# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# █ 🛡️ ɢʟᴏʙᴀʟ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴇɴɢɪɴᴇ ᴠ3.0 [ᴇɴᴛᴇʀᴘʀɪꜱᴇ ᴇᴅɪᴛɪᴏɴ]
# █ 🎯 ᴏᴡɴᴇᴅ & ᴏᴘᴇʀᴀᴛᴇᴅ ʙʏ @IND_BOTZ 
# █ ⚠️ ᴀʟʟ ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ - ᴘʀɪᴠᴀᴛᴇ ɴᴇᴛᴡᴏʀᴋ ᴄᴏʀᴇ
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

import asyncio 
import time
import datetime 
import logging
from database import db 
from config import Config
from pyrogram import Client, filters 
from pyrogram.errors import InputUserDeactivated, FloodWait, UserIsBlocked

# ------------------------------------------------------------------------------------------------------------------------------------------------
# ⚙️ ɢʟᴏʙᴀʟ ꜱʏꜱᴛᴇᴍ ɪɴɪᴛɪᴀʟɪᴢᴀᴛɪᴏɴ & ʟᴏɢɢɪɴɢ ᴘʀᴏᴛᴏᴄᴏʟꜱ
# ------------------------------------------------------------------------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [IND_BROADCAST_CORE] - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S"
)
bc_logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🚀 ᴍᴀɪɴ ᴇxᴇᴄᴜᴛɪᴏɴ ʙʟᴏᴄᴋ: ɢʟᴏʙᴀʟ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴛᴏᴄᴏʟ
# ------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.command(["broadcast", "b"]) & filters.user(Config.OWNER_ID) & filters.reply)
async def execute_global_broadcast(client_bot, message_obj):
    """
    Enterprise Broadcast Protocol.
    Dispatches a payload (replied message) to all users in the network database securely.
    """
    all_clients = await db.get_all_users()
    payload_msg = message_obj.reply_to_message
    
    status_ui = await message_obj.reply_text("<blockquote><b>⏳ ɪɴɪᴛɪᴀᴛɪɴɢ ɢʟᴏʙᴀʟ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴛᴏᴄᴏʟ...</b></blockquote>\n\n<b>🛡️ @IND_BOTZ</b>")
    
    start_timer = time.time()
    total_clients, _ = await db.total_users_bots_count()
    
    # Execution Counters
    processed_count = 0
    blocked_count = 0
    deleted_count = 0
    failed_count = 0 
    success_count = 0
    
    bc_logger.info(f"Broadcast initiated by Admin {message_obj.from_user.id} for {total_clients} clients.")
    
    async for client_data in all_clients:
        delivery_status, status_reason = await dispatch_payload(int(client_data['id']), payload_msg)
        
        if delivery_status:
            success_count += 1
            # Throttling to prevent Telegram server overload
            await asyncio.sleep(2) 
        else:
            if status_reason == "Blocked":
                blocked_count += 1
            elif status_reason == "Deleted":
                deleted_count += 1
            elif status_reason == "Error":
                failed_count += 1
                
        processed_count += 1
        
        # UI Dynamic Progress Update (Throttled per 20 nodes)
        if processed_count % 20 == 0:
            ui_text = f"""<blockquote><b><u>📡 ʙʀᴏᴀᴅᴄᴀꜱᴛ ɪɴ ᴘʀᴏɢʀᴇꜱꜱ</u></b></blockquote>

<b>👥 ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ :</b> <code>{total_clients}</code>
<b>⏳ ᴘʀᴏᴄᴇꜱꜱᴇᴅ :</b> <code>{processed_count} / {total_clients}</code>

<b>✅ ꜱᴜᴄᴄᴇꜱꜱ :</b> <code>{success_count}</code>
<b>🚫 ʙʟᴏᴄᴋᴇᴅ :</b> <code>{blocked_count}</code>
<b>🗑️ ᴅᴇʟᴇᴛᴇᴅ :</b> <code>{deleted_count}</code>
<b>❌ ꜰᴀɪʟᴇᴅ :</b> <code>{failed_count}</code>

<b>🛡️ @IND_BOTZ</b>"""
            await status_ui.edit(ui_text)    
            
    # Finalizing Operation
    time_elapsed = datetime.timedelta(seconds=int(time.time() - start_timer))
    
    final_ui_text = f"""<blockquote><b><u>✅ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</u></b></blockquote>

<b>⏱️ ᴛɪᴍᴇ ᴛᴀᴋᴇɴ :</b> <code>{time_elapsed}</code>
<b>👥 ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ :</b> <code>{total_clients}</code>

<b>✅ ꜱᴜᴄᴄᴇꜱꜱ :</b> <code>{success_count}</code>
<b>🚫 ʙʟᴏᴄᴋᴇᴅ :</b> <code>{blocked_count}</code>
<b>🗑️ ᴅᴇʟᴇᴛᴇᴅ :</b> <code>{deleted_count}</code>
<b>❌ ꜰᴀɪʟᴇᴅ :</b> <code>{failed_count}</code>

<b>🛡️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ @IND_BOTZ</b>"""
    
    await status_ui.edit(final_ui_text)
    bc_logger.info(f"Broadcast completed in {time_elapsed}. Success: {success_count}, Failed: {failed_count}")

# ------------------------------------------------------------------------------------------------------------------------------------------------
# ⚙️ ᴘᴀʏʟᴏᴀᴅ ᴅɪꜱᴘᴀᴛᴄʜᴇʀ & ᴇʀʀᴏʀ ʜᴀɴᴅʟɪɴɢ
# ------------------------------------------------------------------------------------------------------------------------------------------------

async def dispatch_payload(target_id, payload_obj):
    """
    Secure message delivery function.
    Safely bypasses FloodWaits and automatically cleans up dead accounts from the DB.
    """
    try:
        await payload_obj.copy(chat_id=target_id)
        return True, "Success"
        
    except FloodWait as flood_err:
        bc_logger.warning(f"FloodWait triggered during broadcast: Sleeping for {flood_err.value} seconds.")
        await asyncio.sleep(flood_err.value)
        # Retry sending after cooldown
        return await dispatch_payload(target_id, payload_obj)
        
    except InputUserDeactivated:
        # Auto-remove deactivated Telegram accounts to keep DB clean and fast
        await db.delete_user(int(target_id))
        bc_logger.info(f"Node {target_id} deleted their account. Wiped from Database.")
        return False, "Deleted"
        
    except UserIsBlocked:
        bc_logger.info(f"Node {target_id} blocked the network.")
        return False, "Blocked"
        
    except Exception as generic_err:
        bc_logger.error(f"Payload delivery failed for {target_id}: {generic_err}")
        return False, "Error"

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🏁 ᴇɴᴅ ᴏꜰ ꜰɪʟᴇ : ɢʟᴏʙᴀʟ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴇɴɢɪɴᴇ
# ------------------------------------------------------------------------------------------------------------------------------------------------
