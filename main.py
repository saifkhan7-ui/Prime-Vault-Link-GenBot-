import asyncio
from aiohttp import web
from pyrogram import Client, filters
from pyrogram.types import Message
import pyrogram

from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, ADMINS, URL, PORT
from utils import encode_id, decode_id

app = Client("StreamBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- 1. WEB SERVER ENGINE (Browser ko file bhejne ke liye) ---
async def stream_file(request):
    file_id = request.match_info.get('id')
    msg_id = decode_id(file_id)
    
    if msg_id == 0:
        return web.Response(text="❌ Invalid Link! Ye link galat hai.", status=400)
    
    try:
        # Telegram channel se file dhoondhna
        message = await app.get_messages(LOG_CHANNEL, msg_id)
        if not message or message.empty:
            return web.Response(text="❌ File delete ho chuki hai ya nahi mili!", status=404)
        
        # File ka naam aur size nikalna
        media = message.document or message.video or message.audio
        file_size = getattr(media, "file_size", 0)
        file_name = getattr(media, "file_name", "downloaded_file")

        # Browser ko batana ki file download karni hai
        response = web.StreamResponse(
            status=200,
            headers={
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': f'attachment; filename="{file_name}"',
                'Content-Length': str(file_size)
            }
        )
        await response.prepare(request)
        
        # Telegram se tukdo (chunks) me data nikal kar browser ko bhejna
        async for chunk in app.stream_media(message):
            await response.write(chunk)
        
        await response.write_eof()
        return response
    except Exception as e:
        print(f"Streaming Error: {e}")
        return web.Response(text="❌ Streaming Server Error!", status=500)

# Render ka Health Check Route
async def index(request):
    return web.Response(text="Prime Vault Stream Server is Alive! 🚀")


# --- 2. TELEGRAM BOT ENGINE (Direct Link Generate karne ke liye) ---
@app.on_message(filters.private & filters.user(ADMINS) & (filters.document | filters.video | filters.audio))
async def generate_stream_link(client: Client, message: Message):
    if not URL:
        await message.reply_text("❌ **URL Missing:** Pehle config me Render ka link set karo!")
        return
        
    wait_msg = await message.reply_text("⏳ **Uploading to Stream Server...**")
    try:
        # File ko LOG_CHANNEL me save karna
        copied_msg = await message.copy(LOG_CHANNEL)
        
        # ID ko encrypt karna
        file_id = encode_id(copied_msg.id)
        
        # Render wale base URL se download link banana
        base_url = URL.rstrip('/')
        download_link = f"{base_url}/download/{file_id}"
        
        await wait_msg.edit_text(
            f"✅ **Direct Download Link Generated!**\n\n"
            f"📁 **Name:** `{getattr(message.document or message.video or message.audio, 'file_name', 'Media File')}`\n\n"
            f"🔗 **Fast Download Link:**\n`{download_link}`\n\n"
            f"*(Ye link browser, IDM, aur ADM me direct chalegi!)*",
            disable_web_page_preview=True
        )
    except Exception as e:
        await wait_msg.edit_text(f"❌ **Error:** `{e}`")


# --- 3. DUAL STARTUP (Bot + Web Server dono ek sath chalana) ---
async def main():
    await app.start()
    print("🚀 Telegram Bot Started!")
    
    # Web Server setup
    server = web.Application()
    server.router.add_get('/', index)
    server.router.add_get('/download/{id}', stream_file)
    
    runner = web.AppRunner(server)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', PORT).start()
    print(f"🌐 Web Server Started on Port {PORT}!")
    
    await pyrogram.idle()
    
    await runner.cleanup()
    await app.stop()

if __name__ == "__main__":
    app.run(main())
