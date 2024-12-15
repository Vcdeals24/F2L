import os
import requests
from pyrogram import Client, filters

# Telegram Bot API and GitHub Configurations
API_ID = 24972774  # Replace with your API ID
API_HASH = "188f227d40cdbfaa724f1f3cd059fd8b"  # Replace with your API Hash
BOT_TOKEN = "6401043461:AAH5GrnSCgbCldGRdLy-SDvhcK4JzgozI3Y"  # Replace with your bot token

GITHUB_TOKEN = "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"  # Replace with your GitHub token
REPO_OWNER = "vcdeals24"
REPO_NAME = "F2L"
BRANCH_NAME = "main"  # or another branch you are working with

# Initialize Pyrogram Client with API ID and Hash
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# GitHub upload function
def upload_to_github(file_path):
    # GitHub API URL to upload file
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{os.path.basename(file_path)}"
    
    # Open and read file content
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # Base64 encode file content
    content_base64 = requests.utils.to_native_string(content).encode('utf-8').encode('base64')

    # GitHub API request headers
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # GitHub API payload for creating/updating the file
    payload = {
        "message": f"Upload {os.path.basename(file_path)}",
        "content": content_base64,
        "branch": BRANCH_NAME
    }
    
    # Send PUT request to GitHub API
    response = requests.put(url, json=payload, headers=headers)

    return response.status_code == 201

@app.on_message(filters.document | filters.photo | filters.video)
async def handle_media(client, message):
    # Determine which type of media is received
    if message.document:
        file = message.document
    elif message.photo:
        file = message.photo.file_id
    elif message.video:
        file = message.video.file_id

    # Download the file
    downloaded_file = await app.download_media(file)

    # Upload the file to GitHub
    if upload_to_github(downloaded_file):
        await message.reply(f"File '{file.file_name}' uploaded to GitHub successfully!")
    else:
        await message.reply("Failed to upload the file to GitHub.")

# Start the bot
app.run()
