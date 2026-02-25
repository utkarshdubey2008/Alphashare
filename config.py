from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "8599452472:AAFir1VzQ8jPFwuSCWYrjk81BOeCFHZh-48")
API_ID = int(os.getenv("API_ID", 36701545))
API_HASH = os.getenv("API_HASH", "92e8025812ade7acc47f9dc8057b34ad")

OWNER_ID = int(os.getenv("OWNER_ID", 5318110377))

# Database Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Alpha:001100@cluster0.mp2hbsi.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = os.getenv("DATABASE_NAME", "CodeXBot")

# Channel Configuration 
DB_CHANNEL_ID = int(os.getenv("DB_CHANNEL_ID", -1003820981442))
FORCE_SUB_CHANNEL = int(os.getenv("FORCE_SUB_CHANNEL", -1003814864297)) # First force sub channel
FORCE_SUB_CHANNEL_2 = int(os.getenv("FORCE_SUB_CHANNEL_2", 0)) # Second force sub channel, defaults to 0 if not set
FORCE_SUB_CHANNEL_3 = int(os.getenv("FORCE_SUB_CHANNEL_3", 0))
FORCE_SUB_CHANNEL_4 = int(os.getenv("FORCE_SUB_CHANNEL_4", 0))

# Add a second channel link
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/XpremiumB") # First channel link
CHANNEL_LINK_2 = os.getenv("CHANNEL_LINK_2", "") # Second channel link
CHANNEL_LINK_3 = os.getenv("CHANNEL_LINK_3", "") 
CHANNEL_LINK_4 = os.getenv("CHANNEL_LINK_4", "") 

#start photo 
START_PHOTO = os.getenv("START_PHOTO", "") #start photo for bot

# Bot Information
BOT_USERNAME = os.getenv("BOT_USERNAME", "TeamAlphaDriveBot")
BOT_NAME = os.getenv("BOT_NAME", "Team Alpha Drive Bot")
BOT_VERSION = "2.0"

# Privacy Mode Configuration and codexbotz delete time
PRIVACY_MODE = os.getenv("PRIVACY_MODE", "off").lower() == "on"
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", 600))

# Your Modiji Url Api Key Here
MODIJI_API_KEY = os.getenv("MODIJI_API_KEY", "")
if not MODIJI_API_KEY:
    print("⚠️ Warning: MODIJI_API_KEY not set in environment variables")

# Links
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/XpremiumB")
DEVELOPER_LINK = os.getenv("DEVELOPER_LINK", "https://t.me/masudr7iqbal")
SUPPORT_LINK = os.getenv("SUPPORT_LINK", "https://t.me/XpremiumB")

# For Koyeb/render 
WEB_SERVER = bool(os.getenv("WEB_SERVER", True)) # make it True if deploying on koyeb/render else False
PING_URL = os.getenv("PING_URL", "") # add your koyeb/render's public url
PING_TIME = int(os.getenv("PING_TIME", 600)) # Add time_out in seconds

# Admin IDs - Convert space-separated string to list of integers
ADMIN_IDS: List[int] = [
    int(admin_id.strip())
    for admin_id in os.getenv("ADMIN_IDS", "5318110377").split()
    if admin_id.strip().isdigit()
]

# File size limit (4GB in bytes)
MAX_FILE_SIZE = 4000 * 1024 * 1024

# Supported file types and extensions
SUPPORTED_TYPES = [
    "document",
    "video",
    "audio",
    "photo",
    "voice",
    "video_note",
    "animation"
]

SUPPORTED_EXTENSIONS = [
    # Documents
    "pdf", "txt", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    # Programming Files
    "py", "js", "html", "css", "json", "xml", "yaml", "yml",
    # Archives
    "zip", "rar", "7z", "tar", "gz", "bz2",
    # Media Files
    "mp4", "mp3", "m4a", "wav", "avi", "mkv", "flv", "mov",
    "webm", "3gp", "m4v", "ogg", "opus",
    # Images
    "jpg", "jpeg", "png", "gif", "webp", "bmp", "ico",
    # Applications
    "apk", "exe", "msi", "deb", "rpm",
    # Other
    "txt", "text", "log", "csv", "md", "srt", "sub"
]

SUPPORTED_MIME_TYPES = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/zip",
    "application/x-rar-compressed",
    "application/x-7z-compressed",
    "video/mp4",
    "audio/mpeg",
    "audio/mp4",
]
