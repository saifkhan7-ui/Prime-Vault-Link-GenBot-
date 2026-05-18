from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, ADMINS
from utils import encode_id, decode_id

app = Client(
    "PrimeVaultBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- 1. START COMMAND & LINK DECODER (Sabke liye open) ---
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    text = message.text
    # Agar start ke sath koi link aayi hai (Link kholne aaya hai)
    if len(text.split()) > 1:
        payload = text.split()[1]
        msg_id = await decode_id(payload)
        
        if msg_id > 0:
            try:
                await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=LOG_CHANNEL,
                    message_id=msg_id
                )
            except Exception as e:
                await message.reply_text("❌ **File delete ho chuki hai ya link expire ho gayi hai!**")
        else:
            await message.reply_text("❌ **Ye link invalid ya corrupt hai!**")
        return
    
    # Normal Start Command
    await message.reply_text("👋 **Hello!**\n\nMain Prime Vault ka secure bot hoon. (Aap yahan valid link send karke file le sakte hain).")


# --- 2. FILE TO LINK GENERATOR (Sirf ADMINS ke liye) ---
@app.on_message(filters.private & filters.user(ADMINS) & (filters.document | filters.video | filters.audio | filters.photo))
async def generate_link(client: Client, message: Message):
    try:
        wait_msg = await message.reply_text("⏳ **Generating Link...**")
        
        # File ko Log Channel me safe karna
        copied_msg = await message.copy(LOG_CHANNEL)
        
        # Apne 'pv-' stamp wala encrypter call karna
        encoded_string = await encode_id(copied_msg.id)
        bot_info = await client.get_me()
        
        # Final Link
        link = f"https://t.me/{bot_info.username}?start={encoded_string}"
        
        await wait_msg.edit_text(
            f"✅ **File Indexed Successfully!**\n\n"
            f"📁 **Name:** `{message.document.file_name if message.document else 'Media File'}`\n\n"
            f"🔗 **Direct Link:**\n`{link}`",
            disable_web_page_preview=True
        )
    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{e}`")


# --- 3. ALERT FOR OTHER USERS (Jo Admin nahi hain) ---
@app.on_message(filters.private & ~filters.user(ADMINS))
async def unauthorized_user(client: Client, message: Message):
    # Agar message /start nahi hai, tabhi warning do (warna upar wala start trigger hoga)
    if not message.text or not message.text.startswith("/start"):
        await message.reply_text(
            "⛔ **Access Denied!**\n\n"
            "Main ek Private Bot hoon aur sirf apne Admin (Prime Vault) ke liye kaam karta hoon. "
            "Kripya mujhe message ya files na bhejein!"
        )

# --- 4. WEB SERVER (Hugging Face ko zinda rakhne ke liye) ---
from aiohttp import web
import pyrogram

async def handle_web(request):
    return web.Response(text="Prime Vault Bot is Alive & Running! 🚀")

async def main_engine():
    # Web Server Start karna (Port 7860)
    webapp = web.Application()
    webapp.router.add_get('/', handle_web)
    runner = web.AppRunner(webapp)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', 7860).start()
    print("🌐 Web Server Started!")

    # Bot Start karna
    print("🚀 Prime Vault Bot is Starting...")
    await app.start()
    await pyrogram.idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main_engine())

  
