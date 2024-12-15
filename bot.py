import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackContext
from telegram.ext.filters import Command, Document, Photo, Video

# Telegram Bot API Credentials
API_ID = 24972774  # Replace with your API ID
API_HASH = "188f227d40cdbfaa724f1f3cd059fd8b"  # Replace with your API Hash
BOT_TOKEN = "6401043461:AAH5GrnSCgbCldGRdLy-SDvhcK4JzgozI3Y"  # Replace with your bot token

# GitHub API Token and Repo Information
GITHUB_TOKEN = "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"  # Replace with your GitHub token
REPO_OWNER = "vcdeals24"
REPO_NAME = "F2L"
BRANCH_NAME = "main"  # or any other branch you're working with

# Telegram Bot to handle incoming messages and media
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Send a file (image/video/document) to upload it to GitHub.")

async def handle_media(update: Update, context: CallbackContext):
    file = update.message.document or update.message.photo[-1] or update.message.video
    file_id = file.file_id if file else None
    
    if file_id:
        # Download the file
        file = await update.message.bot.get_file(file_id)
        file_path = await file.download()

        # Upload to GitHub
        upload_to_github(file_path)

        # Notify the user
        await update.message.reply_text(f"File '{file.file_name}' uploaded to GitHub successfully!")

def upload_to_github(file_path):
    # GitHub API upload URL
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{os.path.basename(file_path)}"

    # Get the file content
    with open(file_path, 'rb') as f:
        content = f.read()

    # Encode the file content to base64
    content_base64 = requests.utils.to_native_string(content).encode('utf-8').encode('base64')

    # GitHub API headers
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # GitHub API request payload
    payload = {
        "message": f"Upload {os.path.basename(file_path)}",
        "content": content_base64,
        "branch": BRANCH_NAME
    }

    # Send the request to upload the file to GitHub
    response = requests.put(url, json=payload, headers=headers)

    # Handle the response from GitHub
    if response.status_code == 201:
        print(f"File uploaded successfully to {REPO_OWNER}/{REPO_NAME}!")
    else:
        print(f"Failed to upload file: {response.text}")

async def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(Photo | Document | Video, handle_media))

    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
