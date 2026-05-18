import os

# 🔐 API & Bot Tokens
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# 📁 Database & Channels
MONGO_URI = os.environ.get("MONGO_URI", "")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0")) # Yahan saari files store hongi
ADMINS = [int(admin) for admin in os.environ.get("ADMINS", "").split()]

# 🛡️ Force Sub Channel (Optional)
FORCE_SUB = os.environ.get("FORCE_SUB", "") # Channel ID with -100
