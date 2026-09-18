import os
from telethon import TelegramClient, events

API_ID = int(os.environ.get("API_ID", 36051726))
API_HASH = os.environ.get("API_HASH", "254ae667db1074feae757c22af81523d")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = TelegramClient('osint_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("👋 ሰላም! የቴሌግራም OSINT ቦት ነኝ።\n\nየማንኛውንም ሰው መረጃ ለማግኘት `@username` ይላኩልኝ።")

@bot.on(events.NewMessage)
async def osint_lookup(event):
    text = event.raw_text.strip()
    if text.startswith('/'):
        return

    username = text.replace('@', '')
    try:
        user = await bot.get_entity(username)
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        user_id = user.id
        phone = user.phone if user.phone else "የተሸሸገ (Hidden)"
        
        full_user = await bot.get_entity(user_id)
        bio = getattr(full_user, 'about', 'የለም (None)')

        response = (
            f"🔍 **OSINT Result for @{username}**\n\n"
            f"👤 **Full Name:** {full_name}\n"
            f"🆔 **User ID:** `{user_id}`\n"
            f"📞 **Phone:** {phone}\n"
            f"📝 **Bio:** {bio}"
        )
        await event.respond(response)
    except Exception as e:
        await event.respond("❌ ተጠቃሚው አልተገኘም ወይም ስህተት ተፈጥሯል። Username በትክክል ማስገባትዎን ያረጋግጡ።")

print("Bot is running...")
bot.run_until_disconnected()
