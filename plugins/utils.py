# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# █ 🛡️ ɴᴇᴛᴡᴏʀᴋ ꜱᴛᴀᴛᴇ ᴍᴀɴᴀɢᴇʀ ᴠ3.0
# █ 🎯 ᴏᴡɴᴇᴅ & ᴏᴘᴇʀᴀᴛᴇᴅ ʙʏ @IND_BOTZ 
# █ ⚠️ ᴀʟʟ ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ - ᴘʀɪᴠᴀᴛᴇ ᴇᴅɪᴛɪᴏɴ
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

import time as sys_time
import logging
from database import db 
from .test import parse_buttons as extract_inline_payload

# ------------------------------------------------------------------------------------------------------------------------------------------------
# ⚙️ ɢʟᴏʙᴀʟ ꜱᴇꜱꜱɪᴏɴ ᴄᴀᴄʜᴇ & ʟᴏɢɢɪɴɢ
# ------------------------------------------------------------------------------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("IND_STATE_CORE")

ACTIVE_NETWORK_SESSIONS = {}

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🚀 ᴄᴏʀᴇ ᴄʟᴀꜱꜱ: ꜱᴛᴀᴛᴜꜱ ᴛʀᴀᴄᴋɪɴɢ ꜱʏꜱᴛᴇᴍ (ꜱᴛꜱ)
# ------------------------------------------------------------------------------------------------------------------------------------------------

class STS:
    """
    Advanced Session & Transmission State Manager by @IND_BOTZ.
    Handles cache memory, forwarding parameters, and real-time status dynamically.
    """
    
    def __init__(self, client_id):
        self.id = client_id
        self.session_data = ACTIVE_NETWORK_SESSIONS
    
    def verify(self):
        """ Checks if a session is currently active for the given client ID. """
        return self.session_data.get(self.id)
    
    def store(self, source_zone, target_zone, bypass_count, max_threshold):
        """ Initializes and stores the default parameters for a new forwarding task. """
        self.session_data[self.id] = {
            'FROM': source_zone, 
            'TO': target_zone, 
            'total_files': 0, 
            'skip': bypass_count, 
            'limit': max_threshold,
            'fetched': bypass_count, 
            'filtered': 0, 
            'deleted': 0, 
            'duplicate': 0, 
            'total': max_threshold, 
            'start': 0
        }
        self.get(full=True)
        return STS(self.id)
        
    def get(self, value=None, full=False):
        """ Retrieves specific data points or loads the full session state into memory. """
        session_vals = self.session_data.get(self.id)
        if not full:
           return session_vals.get(value)
           
        for state_key, state_val in session_vals.items():
            setattr(self, state_key, state_val)
        return self

    def add(self, key=None, value=1, time_flag=False):
        """ Increments specific metrics or updates the process start timer. """
        if time_flag:
          return self.session_data[self.id].update({'start': sys_time.time()})
        self.session_data[self.id].update({key: self.get(key) + value}) 
    
    def divide(self, base_val, divisor):
       """ Safe division algorithm to calculate percentages and ETA. """
       safe_divisor = 1 if int(divisor) == 0 else divisor 
       return int(base_val) / safe_divisor 
    
    async def get_data(self, client_id):
        """ 
        Extracts comprehensive database configurations, filters, and userbot 
        details required for executing the forwarding protocol.
        """
        node_bot = await db.get_bot(client_id)
        current_state = self
        
        active_filters = await db.get_filters(client_id)
        media_size_params = None
        node_configs = await db.get_configs(client_id)
        
        # Clone verification setup
        if node_configs['duplicate']:
           clone_check_params = [node_configs['db_uri'], self.TO]
        else:
           clone_check_params = False
           
        # Premium Inline Button Extraction
        inline_markup = extract_inline_payload(node_configs['button'] if node_configs['button'] else '')
        
        # Media size limits handling
        if node_configs['file_size'] != 0:
            media_size_params = [node_configs['file_size'], node_configs['size_limit']]
            
        # Compile execution payload
        execution_payload = {
            'chat_id': current_state.FROM, 
            'limit': current_state.limit, 
            'offset': current_state.skip, 
            'filters': active_filters,
            'keywords': node_configs['keywords'], 
            'media_size': media_size_params, 
            'extensions': node_configs['extension'], 
            'skip_duplicate': clone_check_params
        }
        
        return node_bot, node_configs['caption'], node_configs['forward_tag'], execution_payload, node_configs['protect'], inline_markup
        
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ⏱️ ᴛɪᴍᴇ ꜰᴏʀᴍᴀᴛᴛɪɴɢ ᴇɴɢɪɴᴇ
# ------------------------------------------------------------------------------------------------------------------------------------------------

def get_readable_time(seconds: int) -> str:
    """ 
    Converts raw seconds into a highly readable ETA format (Days, Hours, Minutes, Seconds).
    Powered by @IND_BOTZ logic.
    """
    formatted_result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    
    if days != 0:
        formatted_result += f"{days}d "
        
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    
    if hours != 0:
        formatted_result += f"{hours}h "
        
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    
    if minutes != 0:
        formatted_result += f"{minutes}m "
        
    seconds = int(seconds)
    formatted_result += f"{seconds}s"
    
    return formatted_result.strip()

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 🏁 ᴇɴᴅ ᴏꜰ ꜰɪʟᴇ : ꜱᴛᴀᴛᴜꜱ ᴛʀᴀᴄᴋɪɴɢ ꜱʏꜱᴛᴇᴍ
# ------------------------------------------------------------------------------------------------------------------------------------------------
