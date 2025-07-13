import os
from telethon import TelegramClient, events

# Ma'lumotlar Render'ning o'zidan, "Environment Variables" bo'limidan olinadi
# BU YERGA HECH NIMA YOZMANG!
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
SESSION_NAME = 'my_copier_session' # Sessiya nomi o'zgarmaydi

SOURCE_CHANNEL_USERNAME = os.environ.get('SOURCE_CHANNEL_USERNAME')
DESTINATION_CHANNEL_ID = int(os.environ.get('DESTINATION_CHANNEL_ID'))

TEXT_TO_REPLACE = os.environ.get('TEXT_TO_REPLACE')
REPLACEMENT_TEXT = os.environ.get('REPLACEMENT_TEXT')

# Manba kanalini aniqlash (username yoki ID bo'lishi mumkin)
try:
    source_channel = int(SOURCE_CHANNEL_USERNAME)
except ValueError:
    source_channel = SOURCE_CHANNEL_USERNAME

# Telegram klientini yaratish
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    message = event.message
    new_text = message.text

    try:
        if new_text and TEXT_TO_REPLACE in new_text:
            new_text = new_text.replace(TEXT_TO_REPLACE, REPLACEMENT_TEXT)
        elif new_text:
            new_text = f"{new_text}\n\n{REPLACEMENT_TEXT}"
        else:
            new_text = REPLACEMENT_TEXT

        await client.send_message(
            DESTINATION_CHANNEL_ID,
            message=new_text,
            file=message.media,
            link_preview=False
        )
        print(f"Yangi e'lon nusxalandi va kanalingizga joylandi.")
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

async def main():
    await client.start()
    print("Bot muvaffaqiyatli ishga tushdi va kanallarni kuzatmoqda...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
