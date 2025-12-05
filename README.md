# Discord Status Detector & Activity Manager

A Python application that detects Discord and updates your playing status using `pypresence`. This tool allows you to dynamically set custom activities, game statuses, and more on your Discord profile.

## Features

- 🎮 **Rich Presence Support**: Display custom game status on Discord
- 🔄 **Continuous Updates**: Automatically keep your status active
- ⚙️ **Configuration File**: Easy JSON-based configuration
- 🎯 **Multiple Activity Types**: Gaming, watching, listening, and custom statuses
- 👥 **Multiplayer Support**: Show party information
- 🔗 **Button Support**: Add custom buttons to your status

## Prerequisites

- Python 3.7 or higher
- Discord application (running locally)
- Discord Developer Account

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install pypresence
```

### 2. Get Your Discord Client ID

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give it a name and click "Create"
4. Go to "General Information" and copy your **Client ID**
5. Replace `CLIENT_ID` in the scripts with your actual ID

## Usage

### Basic Usage

Edit `discord_status.py` and replace the `CLIENT_ID`:

```python
CLIENT_ID = "your_client_id_here"
```

Then run:

```bash
python discord_status.py
```

Security note: do NOT hardcode your Client ID in source if you plan to push the repo.
Create a local `.env` from `.env.template` and set `DISCORD_CLIENT_ID=` there, or add
`client_id` to `discord_config.json` (and keep that file out of git). The project already
ignores `.env` in `.gitignore`.

### Using Configuration File

Edit `discord_config.json` to customize:

```json
{
  "state": "🎮 Playing a game",
  "details": "Enjoying Discord",
  "large_image": "discord",
  "large_text": "Discord Rich Presence",
  "small_image": null,
  "small_text": null,
  "update_interval": 15,
  "auto_start": true
}
```

### Running Examples

```bash
python examples.py
```

This will demonstrate different activity types.

## Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `state` | string | Main status text (e.g., "Playing", "Watching") |
| `details` | string | Additional details |
| `large_image` | string | Large image asset name |
| `large_text` | string | Hover text for large image |
| `small_image` | string | Small image asset name |
| `small_text` | string | Hover text for small image |
| `update_interval` | integer | Seconds between updates (default: 15) |
| `auto_start` | boolean | Auto-start on launch |

## Advanced Usage

### Custom Status Update

```python
from discord_status import DiscordStatusManager

manager = DiscordStatusManager("your_client_id")
manager.connect()

manager.update_status(
    state="🎮 Playing Elden Ring",
    details="Exploring the Lands Between",
    large_image="discord",
    large_text="Elden Ring",
)

manager.run_continuous()
```

### Multiplayer Status

```python
manager.update_status(
    state="🎮 Playing Valorant",
    details="Competitive Match",
    party_size=(4, 5)  # 4 out of 5 members
)
```

### Custom Buttons

```python
manager.update_status(
    state="Check out my game",
    buttons=[
        {"label": "Play Now", "url": "https://example.com"},
        {"label": "Join Discord", "url": "https://discord.gg/example"}
    ]
)
```

## Class Reference

### DiscordStatusManager

Main class for managing Discord Rich Presence.

#### Methods

- `__init__(client_id, config_file="discord_config.json")`: Initialize manager
- `connect()`: Connect to Discord
- `disconnect()`: Disconnect from Discord
- `update_status(...)`: Update Discord status with custom parameters
- `load_config()`: Load configuration from file
- `save_config()`: Save configuration to file
- `run_continuous(duration=None)`: Run continuous status updates

## Troubleshooting

### "Failed to connect to Discord"

- Ensure Discord is running
- Check that your Client ID is correct
- Make sure you have Discord Developer permissions

### Status not updating

- Verify Discord is running
- Check that pypresence is installed correctly
- Look at console output for error messages

### Connection timeout

- Discord might be busy, try restarting Discord
- Check your internet connection
- Wait a few seconds and try again

## Requirements

- `pypresence>=4.3.0`

## License

MIT License - Feel free to use this project for personal or commercial use.

## References

- [pypresence Documentation](https://qwertyquerty.github.io/pypresence/html/index.html)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Original Repository](https://github.com/seregonwar/Custom-Discord-Activity)

## Notes

- Make sure Discord is running before executing the script
- The application will keep the status active while running
- Press Ctrl+C to stop the program
- The status will clear automatically when the program exits
