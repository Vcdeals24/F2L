import os
from pyrogram import Client, filters
from github import Github
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Telegram Bot configuration
API_ID = os.getenv("API_ID")  # Telegram API ID
API_HASH = os.getenv("API_HASH")  # Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Telegram Bot Token

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub Personal Access Token
REPO_NAME = os.getenv("REPO_NAME")  # GitHub repository name (e.g., "username/repository")
BRANCH_NAME = os.getenv("BRANCH_NAME")  # Branch name (e.g., "main")

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
