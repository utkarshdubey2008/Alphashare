<div align="center">

# αlphα Fílє Shαrє Ɓot

[![Version](https://img.shields.io/badge/Version-2.1-purple?style=for-the-badge)](https://github.com/utkarshdubey2008/AlphaShare)
[![Python](https://img.shields.io/badge/Python-3.11.6-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](https://github.com/utkarshdubey2008/Alphashare/blob/main/License)
[![Stars](https://img.shields.io/github/stars/utkarshdubey2008/AlphaShare?style=for-the-badge&logo=github)](https://github.com/utkarshdubey2008/AlphaShare/stargazers)
[![Forks](https://img.shields.io/github/forks/utkarshdubey2008/AlphaShare?style=for-the-badge&logo=github)](https://github.com/utkarshdubey2008/AlphaShare/fork)
[![Issues](https://img.shields.io/github/issues/utkarshdubey2008/AlphaShare?style=for-the-badge)](https://github.com/utkarshdubey2008/AlphaShare/issues)
[![Last Commit](https://img.shields.io/github/last-commit/utkarshdubey2008/AlphaShare?style=for-the-badge)](https://github.com/utkarshdubey2008/AlphaShare)
[![Telegram](https://img.shields.io/badge/Updates-Channel-blue?style=for-the-badge&logo=telegram)](https://t.me/Thealphabotz)

**A Revolutionary Telegram File Sharing Bot with Quality Upload Mode**

</div>

---

## 📋 Table of Contents

- [What's New in V2.1](#-whats-new-in-v21)
- [Feature Overview](#-feature-overview)
- [Quality Upload Mode](#-quality-upload-mode)
- [Batch Mode](#-batch-mode-enhancements)
- [Technical Improvements](#-technical-improvements)
- [Command Reference](#-complete-command-reference)
- [Installation & Deployment](#️-installation--deployment)
- [Usage Examples](#-usage-examples)
- [Tech Stack](#-tech-stack)
- [Credits](#-credits--acknowledgments)

---

## 🎯 What's New in V2.1

```mermaid
timeline
    title Alpha File Share Bot — Version History
    V1.0 : Basic file sharing
         : UUID-based links
         : Force subscribe
    V2.0 : Batch upload mode
         : Admin management
         : MongoDB integration
         : FloodWait handling
    V2.1 : Quality Upload Mode
         : Smart quality detection
         : Episode auto-sorting
         : FloodWait resume system
         : Retry logic (3x)
```

The headline addition in V2.1 is **Quality Upload Mode** — a system that automatically detects and organizes media files by quality tag (resolution or rip type) and produces clean, grouped shareable links with a single command.

---

## 📊 Feature Overview

```mermaid
mindmap
  root((Alpha Share Bot))
    Quality Upload
      Auto quality detection
      Filename & caption modes
      Smart fallback
      Grouped links output
    Batch Mode
      Episode auto-sorting
      FloodWait resume
      Real-time progress
      No duplicates
    Security
      Multi-admin system
      MongoDB management
      Admin-only uploads
      File access control
    Utilities
      URL shortener
      Auto-delete
      Privacy mode
      Broadcast system
      Force subscribe
    Analytics
      Download stats
      Storage tracking
      User metrics
      Performance data
```

---

## 🚀 Quality Upload Mode

### How It Works

```mermaid
flowchart TD
    A["User sends /qu"] --> B["Quality Upload Mode Activated"]
    B --> C["User sends media file"]
    C --> D{Extraction Mode?}
    D -->|Filename Mode| E["Parse filename for quality tags"]
    D -->|Caption Mode| F["Parse caption for quality tags"]
    F --> G{Caption found?}
    G -->|No| E
    G -->|Yes| H["Quality detected"]
    E --> H
    H --> I["File stored with quality label"]
    I --> J{More files?}
    J -->|Yes| C
    J -->|No| K["User sends /qdone"]
    K --> L["Generate grouped quality links"]
    L --> M["📊 Quality Upload Complete!"]
```

### Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `/qu` | `/qupload` | Start quality upload mode |
| `/qmode` | — | Toggle filename / caption extraction |
| `/qdone` | `/qud` | Generate quality-grouped links |
| `/qcancel` | — | Cancel quality upload mode |

### Supported Quality Formats

| Category | Supported Values |
|----------|-----------------|
| **Resolutions** | `240p` `360p` `480p` `720p` `1080p` `1440p` `2160p` `4K` |
| **Web Rips** | `WEB-DL` `WEBrip` |
| **HD Rips** | `HDrip` `HD-rip` `HD_rip` `HD.rip` `hdrip` |
| **Disc / Broadcast** | `BluRay` `HDTV` `DVDrip` `TS` `CAM` |

### Example Output

```
1080p  → https://t.me/bot?start=xxx
720p   → https://t.me/bot?start=xxx
480p   → https://t.me/bot?start=xxx
WEBrip → https://t.me/bot?start=xxx
HDrip  → https://t.me/bot?start=xxx
```

---

## 📦 Batch Mode Enhancements

### Episode Sorting Pipeline

```mermaid
flowchart LR
    A["Files uploaded\nin any order"] --> B["Pattern detection\nE01 / S01E01 / Ep01 etc."]
    B --> C["Sorted\nascending"]
    C --> D["Sequential\ndelivery"]
    D --> E["Batch link\ngenerated"]
```

**Supported episode patterns:** `E01` · `Episode 01` · `Ep01` · `S01E01` · `[E01]` · `-E01-`

### FloodWait Resume System

When Telegram's FloodWait restriction is triggered mid-batch, the bot saves its exact position in the queue, waits out the restriction, and resumes from the same file — no duplicates, no skipped files, real-time progress displayed throughout.

---

## 🔧 Technical Improvements

```mermaid
graph LR
    A["Upload Request"] --> B{Success?}
    B -->|Yes| C["✅ File Stored"]
    B -->|No - Attempt 1| D["Wait 2s → Retry"]
    D --> E{Success?}
    E -->|Yes| C
    E -->|No - Attempt 2| F["Wait 2s → Retry"]
    F --> G{Success?}
    G -->|Yes| C
    G -->|No - Attempt 3| H["❌ Graceful Error"]
```

| Improvement | Detail |
|-------------|--------|
| **Smart Link Formatting** | All links rendered in monospace; resolutions grouped, rip types listed separately |
| **Retry Logic** | 3 automatic retries with 2-second delays on failed uploads |
| **Command Aliases** | `/qdone` ↔ `/qud` — both work identically |
| **Admin-Only Access** | All batch and quality upload features restricted; unauthorised users receive clear denial messages |

---

## 📋 Complete Command Reference

### 🎬 Quality Upload

```
/qu, /qupload    → Start quality upload mode
/qmode           → Toggle extraction mode (filename / caption)
/qdone, /qud     → Generate quality-grouped links
/qcancel         → Cancel quality upload mode
```

### 📦 Batch Upload

```
/batch           → Start batch mode
/done            → Generate batch link (episode-sorted)
/cancel          → Cancel batch mode
```

### 👑 Admin (Owner Only)

```
/addadmin <user_id>   → Add a new admin
/rmadmin  <user_id>   → Remove admin privileges
/adminlist            → View current admin list
```

### 🛠️ Utility

```
/start           → Start the bot
/help            → Get help information
/stats           → View bot statistics
/short <url>     → Shorten a URL
```

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🎯 **Quality Upload Mode** | Auto-organizes media by quality with grouped shareable links |
| 📦 **Advanced Batch Mode** | Perfect episode sorting, FloodWait resume, real-time progress |
| 🔐 **Multi-Admin System** | MongoDB-backed admin management with owner-only controls |
| 📊 **Analytics & Tracking** | Real-time download stats, storage analytics, user metrics |
| 🔗 **UUID-based Links** | Unique per-file sharing with download tracking |
| 🗑️ **Auto-Delete** | Configurable automatic deletion for copyright compliance |
| 🔒 **Privacy Mode** | Prevent file forwarding and copying |
| 📡 **Force Subscribe** | Multi-channel force subscription support |
| 📢 **Broadcast System** | Message broadcasting with inline button support |
| 🔗 **URL Shortener** | Built-in URL shortening via `/short` |
| ♾️ **24/7 Uptime** | Koyeb keep-alive mechanism for zero-downtime hosting |
| 📁 **Universal File Support** | All Telegram-supported file types accepted |

---

## 🛠️ Installation & Deployment

### Quick Deploy

<div align="center">

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/utkarshdubey2008/AlphaShare)
[![Deploy on Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://youtu.be/2EKt3nVcY6E?si=NKMlRw3qx6eaWjNU)

</div>

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/utkarshdubey2008/AlphaShare.git
cd AlphaShare

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
.\venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

### Updating to V2.1

> [!IMPORTANT]
> **Sync your fork** before redeploying to receive all V2.1 features.

1. Open your forked repository on GitHub.
2. Click **"Sync fork"** → **"Update branch"**.
3. Redeploy your bot to apply the changes.

---

## 🎓 Usage Examples

### Quality Upload Mode

```
User:  /qu
Bot:   ✅ Quality Upload Mode activated!

User:  [Sends Movie.2024.1080p.WEBrip.mkv]
Bot:   ✅ Detected: 1080p, WEBrip

User:  [Sends Movie.2024.720p.HDrip.mkv]
Bot:   ✅ Detected: 720p, HDrip

User:  /qdone
Bot:   📊 Quality Upload Complete!

       1080p  → https://t.me/bot?start=xxx
       720p   → https://t.me/bot?start=xxx
       WEBrip → https://t.me/bot?start=xxx
       HDrip  → https://t.me/bot?start=xxx
```

### Batch Mode with Episodes

```
User:  /batch
Bot:   ✅ Batch Mode activated!

User:  [Sends Series.S01E03.mkv]
User:  [Sends Series.S01E01.mkv]
User:  [Sends Series.S01E02.mkv]

User:  /done
Bot:   📦 Batch Upload Complete!
       Files sorted: E01 → E02 → E03

       Batch Link: https://t.me/bot?start=batch_xxx
```

---

## 💻 Tech Stack

[![Python](https://img.shields.io/badge/Python-3.11.6-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-MTProto-2CA5E0?style=flat-square&logo=telegram&logoColor=white)](https://github.com/pyrogram/pyrogram)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-13AA52?style=flat-square&logo=mongodb&logoColor=white)](https://www.mongodb.com)
[![Koyeb](https://img.shields.io/badge/Koyeb-Hosting-6c47ff?style=flat-square)](https://www.koyeb.com)

| Technology | Role |
|------------|------|
| **Python 3.11.6** | Core runtime |
| **Pyrogram** | Telegram MTProto API framework |
| **MongoDB** | Admin management and file metadata storage |
| **Koyeb** | 24/7 serverless hosting with keep-alive |

---

## 📜 License

This project is licensed under the **[MIT License](https://github.com/utkarshdubey2008/Alphashare/blob/main/License)**.

---

## 🙏 Credits & Acknowledgments

<div align="center">

### 👨‍💻 Developer

**[Utkarsh Dubey](https://github.com/utkarshdubey2008)**
*Main Developer — Alpha Share Bot*

### 🌟 Special Thanks

Contributors, testers, and the Alpha Bots community for continuous support and valuable feedback.

---

### 💬 Join the Community

[![Telegram Channel](https://img.shields.io/badge/Telegram-Join_Channel-blue?style=for-the-badge&logo=telegram)](https://t.me/Thealphabotz)

**Stay updated with the latest features and announcements!**

---

Made with ❤️ by [Utkarsh Dubey](https://github.com/utkarshdubey2008)

**⭐ Star this repo if you find it useful!**

</div>
