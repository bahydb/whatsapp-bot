from WPP_Whatsapp import Create
import time
import os

# 1. Start the client session
creator = Create(session="orders_bot")
client = creator.start()

# Let's define the bot's username or number so we know when it's mentioned
BOT_MENTION = "@bot"


def on_message(msg):
    sender = msg.get('from')
    msg_type = msg.get('type')

    # Safely get the text body and caption (if media is sent)
    text = msg.get('body', '').lower() if msg.get('body') else ''
    caption = msg.get('caption', '').lower() if msg.get('caption') else ''

    # ==========================================
    # JOB 1: SEND STORED LINKS AND FILES
    # ==========================================
    if msg_type == 'chat':
        # Send the site link
        if text == '!site':
            print(f"🔗 Sending site link to {sender}")
            client.sendText(sender, "Here is the link to my site: https://www.yoursite.com")

        # Send a stored file
        elif text == '!file':
            print(f"📄 Sending file to {sender}")
            # Ensure 'sample.pdf' is in the same folder as this Python script
            file_path = "./sample.pdf"
            if os.path.exists(file_path):
                client.sendFile(sender, file_path, "sample.pdf")
            else:
                client.sendText(sender, "Sorry, the requested file is currently unavailable.")

    # ==========================================
    # JOB 2: STICKER MAKER (Image & GIF)
    # ==========================================
    # Check if the message is media AND the bot is mentioned in the caption
    elif msg_type in ['image', 'video'] and BOT_MENTION in caption:
        print(f"🎨 Sticker request received from {sender}")

        try:
            # Step A: Download the incoming media
            # downloadMedia returns the decrypted media buffer
            media_buffer = client.downloadMedia(msg)

            # Step B: Save it temporarily to the disk
            # GIFs are categorized as 'video' (mp4) by WhatsApp
            extension = "mp4" if msg_type == 'video' else "jpg"
            temp_path = f"./temp_media_{msg.get('id')}.{extension}"

            with open(temp_path, "wb") as f:
                f.write(media_buffer)

            # Step C: Convert and send as a sticker
            if msg_type == 'image':
                # Static sticker
                client.sendImageAsSticker(sender, temp_path)
            elif msg_type == 'video':
                # Animated sticker (Requires FFmpeg installed on your system)
                client.sendImageAsStickerGif(sender, temp_path)

            # Step D: Clean up the temporary file so your hard drive doesn't fill up
            if os.path.exists(temp_path):
                os.remove(temp_path)

        except Exception as e:
            print(f"❌ Error creating sticker: {e}")
            client.sendText(sender, "Oops! Something went wrong while making your sticker.")


# Register the message listener
client.on_message(on_message)

print("🚀 Orders Bot is running! Waiting for messages...")

# Keep script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Bot shut down.")