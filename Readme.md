<h1 align="center">🎬 Alpha Share Bot</h1>

<p align="center">
  <a href="https://github.com/utkarshdubey2008/AlphaShare">
    <img src="" alt="Alpha Share Bot" width="500">
  </a>
  <br>
  <b>Advanced Telegram File Sharing Bot</b>
</p>

<p align="center">
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3.11.6-blue?style=for-the-badge&logo=python" alt="Python Version">
  </a>
  <a href="https://github.com/utkarshdubey2008/AlphaShare/stargazers">
    <img src="https://img.shields.io/github/stars/utkarshdubey2008/AlphaShare?style=for-the-badge" alt="GitHub Stars">
  </a>
  <a href="https://github.com/utkarshdubey2008/AlphaShare/fork">
    <img src="https://img.shields.io/github/forks/utkarshdubey2008/AlphaShare?style=for-the-badge" alt="GitHub Forks">
  </a>
  <br>
  <a href="https://github.com/utkarshdubey2008/AlphaShare/issues">
    <img src="https://img.shields.io/github/issues/utkarshdubey2008/AlphaShareBot?style=for-the-badge" alt="GitHub Issues">
  </a>
  <a href="https://github.com/utkarshdubey2008/AlphaShare/network/members">
    <img src="https://img.shields.io/github/last-commit/utkarshdubey2008/AlphaShare?style=for-the-badge" alt="Last Commit">
  </a>
  <a href="https://t.me/Thealphabotz">
    <img src="https://img.shields.io/badge/Updates-Channel-blue?style=for-the-badge&logo=telegram" alt="Updates Channel">
  </a>
</p>


## 🚀 Latest Updates - Version 2.1

### 🎯 **NEW: Quality Upload Mode**
Revolutionary feature that automatically organizes media files by quality and generates grouped shareable links.

**What's New:**
- 📊 **Automatic Quality Detection** - Extracts quality from filenames or captions (480p, 720p, 1080p, HDrip, WEBrip, etc.)
- 🎨 **Smart Grouping** - Organizes files by resolution and rip type automatically
- 🔄 **Dual Extraction Modes** - Choose between filename or caption-based quality detection
- 💾 **Clean Link Generation** - Creates organized, monospace-formatted links for easy sharing
- 🎬 **Wide Format Support** - Handles all standard qualities from 240p to 4K

**Quality Upload Commands:**
```
/qu or /qupload   → Start quality upload mode
/qmode            → Toggle filename/caption extraction
/qdone or /qud    → Generate quality-grouped links
/qcancel          → Cancel quality upload session
```

**Example Output:**
```
480p - https://t.me/bot?start=xxx | 720p - https://t.me/bot?start=xxx
1080p - https://t.me/bot?start=xxx
HDrip - https://t.me/bot?start=xxx | WEBrip - https://t.me/bot?start=xxx
```

**Supported Quality Formats:**
- **Resolutions:** 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p, 4K
- **Rip Types:** BluRay, WEB-DL, WEBrip, HDrip, HDTV, DVDrip, TS, CAM
- **Flexible Patterns:** HDrip, HD-rip, HD_rip, HD.rip, hdrip

### ⚡ **Enhanced Batch Mode**

**Perfect Episode Sequencing:**
- Files now send in exact sorted order
- Smart episode number detection (E01, Episode 01, Ep01, S01E01, [E01], -E01-)
- Maintains proper sequence even with irregular naming

**FloodWait Resume System:**
- Bot remembers exact position during Telegram FloodWait
- Automatic resume from interruption point
- Real-time progress tracking
- Zero file skipping or duplication

### 🔧 **Technical Improvements**

**Smart Link Formatting:**
- Monospace format for easy copying
- Resolution qualities grouped on single lines
- Rip qualities listed separately for clarity

**Enhanced Reliability:**
- 3 automatic retries on failed uploads
- 2-second intelligent delay between retries
- Graceful error handling and user notifications

**Command Aliases:**
- `/qdone` → `/qud` (quick done)
- Multiple command options for user convenience


## ✨ Core Features

### 🔐 Security & Administration
- **Multi-Admin System** - Dynamic admin management via MongoDB
- **Owner Controls** - Add/remove admins with `/addadmin` and `/rmadmin`
- **Admin Verification** - Secure file upload access control
- **Privacy Mode** - Prevent file forwarding and copying

### 📁 File Management
- **Universal File Support** - All Telegram file types (videos, documents, audio, images)
- **Batch Uploads** - Upload multiple files with a single shareable link
- **Quality Organization** - Automatic quality-based file grouping
- **UUID-Based Links** - Unique, secure sharing links with download tracking
- **Auto-Delete** - Configurable auto-deletion to prevent copyright issues

### 📊 Analytics & Tracking
- **Real-Time Statistics** - Monitor downloads and storage usage
- **Download Tracking** - Per-file download counts
- **User Analytics** - Track bot usage and engagement
- **Admin Dashboard** - Comprehensive bot statistics

### 🎨 User Experience
- **Professional UI** - Clean interface with progress bars
- **Interactive Buttons** - Easy navigation with inline keyboards
- **Welcome Photo** - Custom start image on `/start`
- **URL Shortening** - Built-in shortener with `/short` command
- **Force Subscription** - Multi-channel force sub support

### ⚙️ Performance
- **24/7 Uptime** - Koyeb keep-alive mechanism
- **Optimized Queries** - Reduced database load
- **Efficient File Handling** - Fast upload and download processing
- **Broadcast System** - Fixed bugs with message broadcasting

---

## 📋 Command Reference

### 👨‍💼 Admin Commands

**Admin Management (Owner Only):**
```
/addadmin <user_id>   → Add new admin
/rmadmin <user_id>    → Remove admin privileges
/adminlist            → View all admins
```

**File Sharing:**
```
/batch                → Start batch upload mode
/done                 → Generate batch link
/cancel               → Cancel batch session
```

**Quality Upload:**
```
/qu, /qupload         → Start quality upload mode
/qmode                → Toggle extraction mode
/qdone, /qud          → Generate quality links
/qcancel              → Cancel quality upload
```

**Broadcasting:**
```
/broadcast            → Send message to all users
```

### 👤 User Commands
```
/start                → Start the bot
/help                 → Get help information
/about                → About the bot
/stats                → View bot statistics
/short <url>          → Shorten a URL
```


## 🛠️ Installation & Deployment

### Quick Deploy

<p align="center">
  <a href="https://heroku.com/deploy?template=https://github.com/utkarshdubey2008/AlphaShare">
    <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy on Heroku">
  </a>
  <br>
  <a href="https://youtu.be/2EKt3nVcY6E?si=NKMlRw3qx6eaWjNU">
    <img src="https://www.koyeb.com/static/images/deploy/button.svg" alt="Deploy on Koyeb">
  </a>
</p>

### Manual Installation

**1. Clone the Repository:**
```bash
git clone https://github.com/utkarshdubey2008/AlphaShare.git
cd AlphaShare
```

**2. Create Virtual Environment:**
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables:**
Create a `.env` file with the following:
```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
MONGO_URI=your_mongodb_uri
OWNER_ID=your_user_id
FORCE_SUB_CHANNEL=@your_channel
```

**5. Run the Bot:**
```bash
python main.py
```


## 🔄 Updating to V2.1

If you're upgrading from V2.0, follow these steps:

**1. Sync Your Fork:**
- Go to your GitHub repository
- Click "Sync fork" → "Update branch"

**2. Pull Latest Changes:**
```bash
git pull origin main
```

**3. Update Dependencies:**
```bash
pip install -r requirements.txt --upgrade
```

**4. Restart Your Bot:**
- Redeploy on your hosting platform (Heroku/Koyeb)
- Or restart locally: `python main.py`


## 📖 How to Use Quality Upload Mode

**Step 1:** Start quality upload mode
```
/qu
```

**Step 2:** Send your media files
- Bot auto-detects quality from filename by default
- Use `/qmode` to switch to caption-based detection

**Step 3:** Complete the upload
```
/qdone
```

**Step 4:** Share the organized links!
```
480p - https://t.me/bot?start=abc123
720p - https://t.me/bot?start=def456
1080p - https://t.me/bot?start=ghi789
```

---

## 🎓 How It Works

**Quality Detection Modes:**

**Filename Mode (Default):**
- Extracts quality from file name
- Example: `Movie.2024.1080p.WEBrip.mkv` → detects 1080p & WEBrip

**Caption Mode:**
- Extracts quality from file caption/description
- Useful when quality is in caption instead of filename
- Smart fallback to filename if no caption exists

**Supported Patterns:**
- Episode numbers: E01, Ep01, Episode 01, S01E01, [E01], -E01-
- Quality formats: 1080p, 1080P, 1080-p, 1080.p
- Rip types: HDrip, HD-rip, HD_rip, hdrip (case insensitive)

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 📜 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/utkarshdubey2008/Alphashare/blob/main/License) file for details.


## 🙏 Credits

- **[Utkarsh Dubey](https://github.com/utkarshdubey2008)** - Main Developer & Creator
- **[Pyrogram](https://github.com/pyrogram/pyrogram)** - Telegram MTProto API Framework


**Special Thanks:**
- All contributors and testers
- The Alpha Bots Community
- Everyone who reported bugs and suggested features


## 📞 Support & Community

<p align="center">
  <a href="https://t.me/Thealphabotz">
    <img src="https://img.shields.io/badge/Telegram-Channel-blue?style=for-the-badge&logo=telegram" alt="Telegram Channel">
  </a>
  <br>
  <b>Join our channel for updates, support, and announcements!</b>
</p>


## ⭐ Star History

If you find this project useful, please consider giving it a star! It helps others discover the project.


<p align="center">Made with ❤️ by <a href="https://t.me/TheAlphaBotz">Team Alpha</a></p>
<p align="center">© 2024 Alpha Share Bot. All rights reserved.</p>
