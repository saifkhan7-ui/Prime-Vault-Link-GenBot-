import os

# 🔐 API & Bot Tokens
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# 📁 Channels & Admins
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0")) 
ADMINS = [int(admin) for admin in os.environ.get("ADMINS", "").split()]

# 🌐 Web Server Details (Render ke liye)
URL = os.environ.get("URL", "") # Ye Render humein dega (jaise: https://my-bot.onrender.com)
PORT = int(os.environ.get("PORT", "8080"))
