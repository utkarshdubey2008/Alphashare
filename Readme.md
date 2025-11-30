<div align="center">

# αlphα Fílє Shαrє Ɓot

<img src="https://img.shields.io/badge/Version-2.1-purple?style=for-the-badge" alt="Version 2.1">

**A Revolutionary Telegram File Sharing Bot with Quality Upload Mode**

<img src="https://img.shields.io/badge/Python-3.11.6-blue?style=for-the-badge&logo=python" alt="Python Version">
<a href="https://github.com/utkarshdubey2008/AlphaShare/stargazers"><img src="https://img.shields.io/github/stars/utkarshdubey2008/AlphaShare?style=for-the-badge" alt="GitHub Stars"></a>
<a href="https://github.com/utkarshdubey2008/AlphaShare/fork"><img src="https://img.shields.io/github/forks/utkarshdubey2008/AlphaShare?style=for-the-badge" alt="GitHub Forks"></a>
<br>
<a href="https://github.com/utkarshdubey2008/AlphaShare/issues"><img src="https://img.shields.io/github/issues/utkarshdubey2008/AlphaShare?style=for-the-badge" alt="GitHub Issues"></a>
<a href="https://github.com/utkarshdubey2008/AlphaShare/network/members"><img src="https://img.shields.io/github/last-commit/utkarshdubey2008/AlphaShare?style=for-the-badge" alt="Last Commit"></a>
<a href="https://t.me/Thealphabotz"><img src="https://img.shields.io/badge/Updates-Channel-blue?style=for-the-badge&logo=telegram" alt="Updates Channel"></a>

</div>

---

## 🎯 What's New in V2.1

<div align="center">

### 🚀 MAJOR FEATURE: QUALITY UPLOAD MODE

<img src="https://raw.githubusercontent.com/utkarshdubey2008/AlphaShare/main/assets/quality_upload_banner.png" alt="Quality Upload Feature" width="600">

*Automatically organize your media files by quality and generate grouped, shareable links*

</div>

### 📌 Quality Upload Mode Overview

A revolutionary feature that **automatically organizes** your media files by quality (480p, 720p, 1080p, HDrip, WEBrip, etc.) and generates **grouped, shareable links**.

#### 🔧 Commands

| Command | Description |
|---------|-------------|
| `/qu` or `/qupload` | Start quality upload mode |
| `/qmode` | Toggle between filename/caption extraction |
| `/qdone` or `/qud` | Generate quality-grouped links |
| `/qcancel` | Cancel quality upload mode |

#### 📝 How It Works

1. **Activate** quality upload with `/qu`
2. **Send** your media files (videos/documents)
3. **Auto-detect** quality from filename or caption
4. **Generate** organized links with `/qdone`

#### 💡 Example Output

```
480p - https://t.me/bot?start=xxx | 720p - https://t.me/bot?start=xxx | 1080p - https://t.me/bot?start=xxx
HDrip - https://t.me/bot?start=xxx
WEBrip - https://t.me/bot?start=xxx
```

#### 🎨 Supported Quality Formats

- **Resolutions**: `240p`, `360p`, `480p`, `720p`, `1080p`, `1440p`, `2160p`, `4K`
- **Rip Types**: `BluRay`, `WEB-DL`, `WEBrip`, `HDrip`, `HDTV`, `DVDrip`, `TS`, `CAM`
- **Flexible Pattern**: Handles `HDrip`, `HD-rip`, `HD_rip`, `HD.rip`, `hdrip`

---

## 🎯 Quality Extraction Modes

<div align="center">
<img src="https://raw.githubusercontent.com/utkarshdubey2008/AlphaShare/main/assets/extraction_modes.png" alt="Extraction Modes" width="500">
</div>

### 📂 Filename Mode (Default)
- Extracts quality from file name
- **Example**: `Movie.Name.2024.1080p.WEBrip.mkv` → `1080p` & `WEBrip`

### 💬 Caption Mode
- Extracts quality from file caption/description
- Useful when quality is mentioned in caption
- Toggle via `/qmode` command

### 🔀 Smart Fallback
- If caption mode is active but no caption exists
- Automatically falls back to filename extraction
- Ensures quality is always detected

---

## 🚀 Batch Mode Enhancements

<div align="center">
<img src="https://raw.githubusercontent.com/utkarshdubey2008/AlphaShare/main/assets/batch_mode.png" alt="Batch Mode" width="500">
</div>

### 📦 Perfect Episode Sequencing
- Files now send in **exact sorted order**
- Episode numbers detected from multiple patterns
- Supports: `E01`, `Episode 01`, `Ep01`, `S01E01`, `[E01]`, `-E01-`

### ⚡ FloodWait Resume System
- Bot remembers **exact position** during FloodWait
- Resumes from where it stopped
- Real-time progress tracking
- No files skipped or duplicated

---

## 🔧 Technical Improvements

### ✅ Smart Link Formatting
- All links now in monospace format for easy copying
- Resolution qualities grouped on one line
- Rip qualities listed separately for clarity

### ✅ Retry Logic
- 3 automatic retries on failed uploads
- 2-second delay between retries
- Graceful error handling

### ✅ Command Aliases
- `/qdone` → `/qud` (quick done)
- Both work identically for user convenience

### ✅ Admin-Only Access
- All batch and quality upload features restricted to admins
- Unauthorized users receive clear denial messages

---

## 📋 Complete Command Reference

### 🎬 Quality Upload Commands

```
/qu, /qupload    → Start quality upload mode
/qmode           → Toggle extraction mode (filename/caption)
/qdone, /qud     → Generate quality links
/qcancel         → Cancel quality upload
```

### 📦 Batch Upload Commands

```
/batch           → Start batch mode
/done            → Generate batch link (episode sorted)
/cancel          → Cancel batch mode
```

### 👑 Admin Commands

```
/addadmin <user_id>  → Add a new admin (Owner only)
/rmadmin <user_id>   → Remove admin privileges (Owner only)
/adminlist           → View current admin list (Owner only)
```

### 🛠️ Utility Commands

```
/start           → Start the bot
/help            → Get help information
/stats           → View bot statistics
/short <url>     → Shorten a URL
```

---

## ✨ Core Features

<table>
<tr>
<td width="50%">

### 🎯 Quality Upload Mode
- Auto-organize by quality
- Grouped shareable links
- Smart quality detection
- Multiple extraction modes

### 📦 Advanced Batch Mode
- Perfect episode sorting
- FloodWait resume system
- Real-time progress tracking
- No duplicates or skips

</td>
<td width="50%">

### 🔐 Security & Admin
- Multi-admin system
- MongoDB admin management
- Admin-only uploads
- File access control

### 📊 Analytics & Tracking
- Real-time download stats
- Storage analytics
- User tracking
- Performance metrics

</td>
</tr>
</table>

### 🌟 Additional Features

- ✅ **Universal File Support** — All Telegram-supported file types
- ✅ **UUID-based Links** — Unique sharing with download tracking
- ✅ **Professional UI** — Clean interface with progress bars
- ✅ **Auto-Delete** — Configurable auto-deletion for copyright
- ✅ **URL Shortening** — Built-in URL shortener
- ✅ **Privacy Mode** — Prevent file forwarding/copying
- ✅ **24/7 Uptime** — Koyeb keep-alive mechanism
- ✅ **Force Subscribe** — Multiple force sub channels support
- ✅ **Broadcast System** — Message broadcasting with inline buttons

---

## 🛠️ Installation & Deployment

### 🚀 Quick Deploy

<div align="center">

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/utkarshdubey2008/AlphaShare)
[![Deploy on Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://youtu.be/2EKt3nVcY6E?si=NKMlRw3qx6eaWjNU)

</div>

### 💻 Manual Installation

```bash
# Clone the repository
git clone https://github.com/utkarshdubey2008/AlphaShare.git
cd AlphaShare

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

### 🔄 How to Update to V2.1

> [!IMPORTANT]
> **Sync Your Fork** to get the latest V2.1 features!

1. Go to your forked repository on GitHub
2. Click on **"Sync fork"** button
3. Click **"Update branch"** to sync with the latest changes
4. Redeploy your bot to apply the updates

---

## 🎓 Usage Examples

### Example 1: Quality Upload Mode

```
User: /qu
Bot: ✅ Quality Upload Mode activated!

User: [Sends Movie.2024.1080p.WEBrip.mkv]
Bot: ✅ Detected: 1080p, WEBrip

User: [Sends Movie.2024.720p.HDrip.mkv]
Bot: ✅ Detected: 720p, HDrip

User: /qdone
Bot: 
📊 Quality Upload Complete!

1080p - https://t.me/bot?start=xxx
720p - https://t.me/bot?start=xxx
WEBrip - https://t.me/bot?start=xxx
HDrip - https://t.me/bot?start=xxx
```

### Example 2: Batch Mode with Episodes

```
User: /batch
Bot: ✅ Batch Mode activated!

User: [Sends Series.S01E03.mkv]
User: [Sends Series.S01E01.mkv]
User: [Sends Series.S01E02.mkv]

User: /done
Bot: 
📦 Batch Upload Complete!
Files sorted: E01, E02, E03

Batch Link: https://t.me/bot?start=batch_xxx
```

---

## 📜 License

This project is licensed under the **[MIT LICENSE](https://github.com/utkarshdubey2008/Alphashare/blob/main/License)**.

---

## 🙏 Credits & Acknowledgments

<div align="center">

### 👨‍💻 Developer

**[Utkarsh Dubey](https://github.com/utkarshdubey2008)**  
*Main Developer of Alpha Share Bot*

### 🛠️ Technologies

- **[Pyrogram](https://github.com/pyrogram/pyrogram)** — Telegram MTProto API Framework
- **[MongoDB](https://www.mongodb.com/)** — Database for admin and file management
- **[Koyeb](https://www.koyeb.com/)** — Seamless 24/7 hosting

### 🌟 Special Thanks

- Contributors, testers, and community members
- Alpha Bots Community for continuous support
- All users who provided valuable feedback

</div>

---

<div align="center">

### 💬 Join Our Community

<a href="https://t.me/Thealphabotz">
<img src="https://img.shields.io/badge/Telegram-Channel-blue?style=for-the-badge&logo=telegram" alt="Telegram Channel">
</a>

**Stay updated with the latest features and announcements!**

---

Made with ❤️ by [Utkarsh Dubey](https://github.com/utkarshdubey2008)

**⭐ Star this repo if you find it useful!**

</div>
