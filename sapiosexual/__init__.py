import logging
import time
import os
import sys
import spamwatch
from telethon import TelegramClient
from redis import StrictRedis
import telegram.ext as tg


# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

LOGGER.info("Starting sapiosexual...")

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)
try:
    os.remove("reboot")
except BaseException:
    pass

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)
    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        DEV_USERS = set(
            int(x) for x in os.environ.get(
                "DEV_USERS", "").split())
    except ValueError:
        raise Exception("Your dev users list does not contain valid integers.")

    try:
        SUDO_USERS = set(
            int(x) for x in os.environ.get(
                "SUDO_USERS", "").split())
    except ValueError:
        raise Exception(
            "Your sudo users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(
            int(x) for x in os.environ.get(
                "SUPPORT_USERS", "").split())
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(
            int(x) for x in os.environ.get("WHITELIST_USERS", "").split()
        )
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")
    try:
        WHITELIST_CHATS = set(
            int(x) for x in os.environ.get("WHITELIST_CHATS", "").split()
        )
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")
    try:
        BLACKLIST_CHATS = set(
            int(x) for x in os.environ.get("BLACKLIST_CHATS", "").split()
        )
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    since_time_start = time.time()
    
        
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    

    MESSAGE_DUMP = os.environ.get("MESSAGE_DUMP", None)
    GBAN_DUMP = os.environ.get("GBAN_LOGS", None)
    DB_URI = os.environ.get("DATABASE_URL")
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "").split()
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))
    WORKERS = int(os.environ.get("WORKERS", 8))
    CUSTOM_CMD = os.environ.get("CUSTOM_CMD", False)
    TELETHON_ID = int(os.environ.get("TL_APP_ID", None))
    TELETHON_HASH = os.environ.get("TL_HASH", None)
    SPAMWATCH = os.environ.get("SPAMWATCH_API", None)
    WALL_API = os.environ.get("WALL_API", None)
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    IBM_WATSON_CRED_URL = os.environ.get("IBM_WATSON_CRED_URL", None)
    IBM_WATSON_CRED_PASSWORD = os.environ.get("IBM_WATSON_CRED_PASSWORD", None)
    REDIS_URL = os.environ.get('REDIS_URL', None)
    LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY")
    SPT_CLIENT_SECRET = os.environ.get("SPT_CLIENT_SECRET")
    SPT_CLIENT_ID = os.environ.get("SPT_CLIENT_ID")
    APP_URL = os.environ.get("APP_URL")
    ARLTOKEN = os.environ.get("ARLTOKEN")
    #AI_API_KEY = os.environ.get('AI_API_KEY', "")

else:
from sapiosexual.config import Development as Config

TOKEN = Config.BOT_TOKEN
try:
    OWNER_ID = int(Config.OWNER_ID)
except ValueError:
    raise Exception("Your OWNER_ID variable is not a valid integer.")

    
OWNER_USERNAME = Config.OWNER_USERNAME

try:
    SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or [])
except ValueError:
    raise Exception("Your sudo users list does not contain valid integers.")

try:
    SUPPORT_USERS = set(int(x) for x in Config.SUPPORT_USERS or [])
except ValueError:
    raise Exception("Your support users list does not contain valid integers.")

try:
    WHITELIST_USERS = set(int(x) for x in Config.WHITELIST_USERS or [])
except ValueError:
    raise Exception("Your whitelisted users list does not contain valid integers.")
try:
    WHITELIST_CHATS = set(int(x) for x in Config.WHITELIST_CHATS or [])
except ValueError:
    raise Exception("Your whitelisted users list does not contain valid integers.")
try:
    BLACKLIST_CHATS = set(int(x) for x in Config.BLACKLIST_CHATS or [])
except ValueError:
    raise Exception("Your whitelisted users list does not contain valid integers.")

    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH

    MESSAGE_DUMP = Config.MESSAGE_DUMP
    GBAN_DUMP = Config.GBAN_DUMP
    ERROR_DUMP = Config.ERROR_DUMP
    DB_URI = Config.SQLALCHEMY_DATABASE_URI
    REDIS_URL = Config.REDIS_URL
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    CUSTOM_CMD = Config.CUSTOM_CMD
    API_WEATHER = Config.API_OPENWEATHER
    TELETHON_HASH = Config.TELETHON_HASH
    TELETHON_ID = Config.TELETHON_ID
    SPAMWATCH = Config.SPAMWATCH_API
    WALL_API = Config.WALL_API
    YOUTUBE_API_KEY = Config.YOUTUBE_API_KEY
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    IBM_WATSON_CRED_URL = Config.IBM_WATSON_CRED_URL
    IBM_WATSON_CRED_PASSWORD = Config.IBM_WATSON_CRED_PASSWORD
    LASTFM_API_KEY = Config.LASTFM_API_KEY
    SPT_CLIENT_SECRET = Config.SPT_CLIENT_SECRET
    SPT_CLIENT_ID = Config.SPT_CLIENT_ID
    APP_URL = Config.APP_URL
    ARLTOKEN = Config.ARLTOKEN

SUDO_USERS.add(OWNER_ID)

# Pass if SpamWatch token not set.
if SPAMWATCH == None:
    spamwtc = None
    LOGGER.warning("Invalid spamwatch api")
else:
    spamwtc = spamwatch.Client(SPAMWATCH)

REDIS_URL = Config.REDIS_URI
REDIS = StrictRedis.from_url(REDIS_URL,decode_responses=True)

try:
    REDIS.ping()
    LOGGER.info("Your redis server is now alive!")
    
except BaseException:
    raise Exception("Your redis server is not alive, please check again.")

 
# Telethon
api_id = TELETHON_ID
api_hash = TELETHON_HASH
client = TelegramClient("sapiosexual", api_id, api_hash)

updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)

dispatcher = updater.dispatcher

# init time
since_time_start = time.time()
SUDO_USERS = list(SUDO_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)

# Load at end to ensure all prev variables have been set
from sapiosexual.modules.helper_funcs.handlers import CustomCommandHandler

if CUSTOM_CMD and len(CUSTOM_CMD) >= 1:
    tg.CommandHandler = CustomCommandHandler
