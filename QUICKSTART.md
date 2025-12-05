# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Activate Virtual Environment

**Windows:**
```bash
.\.venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### Step 2: Set Your Discord Client ID

**Option A: Interactive Setup**
```bash
python setup.py
```
Then follow the prompts to enter your Client ID.

**Option B: Manual Setup**
1. Get your Client ID from https://discord.com/developers/applications
2. Open `discord_status.py`
3. Replace `CLIENT_ID = "1234567890123456789"` with your actual ID

Instead of editing source, run `python setup.py` and choose option 1 — the setup
will save your Client ID into a local `.env` file (ignored by git). You can also
copy `.env.template` to `.env` and fill it manually.

### Step 3: Run the Program

```bash
python discord_status.py
```

Your Discord status should now update!

---

## 📝 Common Examples

### Gaming Status
```python
manager.update_status(
    state="🎮 Playing Valorant",
    details="Competitive Match",
    large_image="discord",
    large_text="Valorant",
)
```

### Listening Status
```python
manager.update_status(
    state="🎵 Listening to",
    details="Lofi Hip Hop Beats",
    large_image="discord",
    large_text="Spotify",
)
```

### Custom Status
```python
manager.update_status(
    state="💻 Working on a Project",
    details="Discord Bot Development",
    large_image="discord",
    large_text="Coding",
)
```

---

## 🔧 Configuration

Edit `discord_config.json` to customize default settings:

```json
{
  "state": "🎮 Playing a game",
  "details": "Enjoying Discord",
  "large_image": "discord",
  "large_text": "Discord Rich Presence",
  "update_interval": 15
}
```

---

## ⚠️ Troubleshooting

**"Failed to connect to Discord"**
- Make sure Discord is running
- Check your Client ID is correct

**"ModuleNotFoundError: No module named 'pypresence'"**
```bash
pip install -r requirements.txt
```

**Status not appearing**
- Wait 10-15 seconds for Discord to update
- Make sure Discord is in focus or active

---

## 📚 Need Help?

See `README.md` for comprehensive documentation and advanced usage.
