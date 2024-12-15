import os
from pyrogram import Client, filters
from github import Github
from io import BytesIO

# Telegram Bot configuration
API_ID = 24972774  # Replace with your API ID
API_HASH = "188f227d40cdbfaa724f1f3cd059fd8b"  # Replace with your API Hash
BOT_TOKEN = "6401043461:AAH5GrnSCgbCldGRdLy-SDvhcK4JzgozI3Y"  # Replace with your bot token

# GitHub Configuration
GITHUB_TOKEN = "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"  # Replace with your GitHub token
REPO_NAME = "vcdeals24/F2L"  # Your GitHub repository
BRANCH_NAME = "main"  # The branch to upload files to

# Initialize GitHub client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Initialize Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def upload_file_to_github(file_name, file_content):
    """
    Upload file content to GitHub repository.
    """
    try:
        # Check if the file already exists in the repo
        try:
            file = repo.get_contents(file_name, ref=BRANCH_NAME)
            repo.update_file(file.path, f"Updating {file_name}", file_content, file.sha, branch=BRANCH_NAME)
            print(f"Updated {file_name}")
        except:
            repo.create_file(file_name, f"Adding {file_name}", file_content, branch=BRANCH_NAME)
            print(f"Uploaded {file_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")

@app.on_message(filters.document | filters.photo | filters.video)
async def handle_new_message(client, message):
    if message.media:
        # Determine the file type (image, video, document, etc.)
        file_name = None
        file_content = None

        # Handling image media
        if message.photo:
            file_name = "image.jpg"
            file_content = await message.download()

        # Handling document media
        elif message.document:
            file_name = message.document.file_name
            file_content = await message.download()

        # Handling video media
        elif message.video:
            file_name = "video.mp4"
            file_content = await message.download()

        if file_name and file_content:
            print(f"Received {file_name}, uploading to GitHub...")
            # Upload the file content to GitHub
            await upload_file_to_github(file_name, file_content)
        else:
            print("Unsupported media type.")

# Run the Pyrogram client
app.run()
