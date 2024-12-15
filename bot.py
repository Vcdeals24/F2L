from pyrogram import Client, filters
from github import Github
import os

# Telegram Bot Configuration
API_ID = 24972774  # Replace with your API ID
API_HASH = "188f227d40cdbfaa724f1f3cd059fd8b"  # Replace with your API Hash
BOT_TOKEN = "6401043461:AAH5GrnSCgbCldGRdLy-SDvhcK4JzgozI3Y"  # Replace with your bot token

# GitHub Configuration
GITHUB_TOKEN = "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"  # Replace with your GitHub token
REPO_NAME = "Vcdeals24/F2L"  # Your repository name
REPO_PATH = "DL/"  # Path in the repository where files will be uploaded

# Initialize Pyrogram Client
app = Client("uploader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize GitHub API
github = Github(GITHUB_TOKEN)
repo = github.get_repo(REPO_NAME)


@app.on_message(filters.document | filters.photo | filters.video)
async def upload_to_github(client, message):
    try:
        # Determine file name
        if message.document:
            file_name = message.document.file_name
        elif message.photo:
            file_name = f"{message.photo.file_id}.jpg"
        elif message.video:
            file_name = f"{message.video.file_id}.mp4"
        else:
            await message.reply_text("Unsupported file type!")
            return

        file_path = f"downloads/{file_name}"

        # Download file from Telegram
        await message.download(file_path)

        # Read the file's content
        with open(file_path, "rb") as file:
            content = file.read()

        # Check if the file already exists in the repo
        try:
            repo.get_contents(f"{REPO_PATH}{file_name}")
            repo.delete_file(
                path=f"{REPO_PATH}{file_name}",
                message=f"Remove old version of {file_name}",
                sha=repo.get_contents(f"{REPO_PATH}{file_name}").sha,
            )
        except Exception:
            pass  # File does not exist, continue with upload

        # GitHub: Upload file
        repo.create_file(
            path=f"{REPO_PATH}{file_name}",  # File path in the repository
            message=f"Add {file_name}",  # Commit message
            content=content,  # File content
        )
        await message.reply_text(f"✅ Uploaded `{file_name}` to GitHub repo successfully!")

    except Exception as e:
        await message.reply_text(f"❌ Failed to upload file: {e}")
    finally:
        # Clean up the downloaded file
        if os.path.exists(file_path):
            os.remove(file_path)


# Run the bot
if __name__ == "__main__":
    print("Telegram to GitHub Bot is running...")
    app.run()