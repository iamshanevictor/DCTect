"""
Discord Status Examples - Various activity types and scenarios
Run this file to see different Discord status examples.
"""

import time
import os
import json
from typing import Dict, Any

from discord_status import DiscordStatusManager

# Try to auto-load a local .env file so DISCORD_CLIENT_ID written by setup.py is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


# Path to configuration file (optional)
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "discord_config.json")


def load_config() -> Dict[str, Any]:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Failed to load config: {e}")
        return {}


CONFIG = load_config()


def example_gaming_status(manager: DiscordStatusManager):
    """Display a gaming status."""
    print("\n--- Gaming Status Example ---")
    manager.update_status(
        state="🎮 Playing Elden Ring",
        details="Exploring South Beach",
        large_image="discord",
        large_text="Elden Ring",
    )
    time.sleep(5)


def example_watching_status(manager: DiscordStatusManager):
    """Display a watching status."""
    print("\n--- Watching Status Example ---")
    manager.update_status(
        state="👀 Watching",
        details="Twitch Streamer123",
        large_image="discord",
        large_text="On Twitch",
    )
    time.sleep(5)


def example_listening_status(manager: DiscordStatusManager):
    """Display a listening status."""
    print("\n--- Listening Status Example ---")
    manager.update_status(
        state="🎵 Listening to",
        details="Lofi Hip Hop Beats",
        large_image="discord",
        large_text="Spotify",
    )
    time.sleep(5)


def example_custom_status(manager: DiscordStatusManager):
    """Display a custom status."""
    print("\n--- Custom Status Example ---")
    manager.update_status(
        state="💻 Working on a Project",
        details="Discord Bot Development",
        large_image="discord",
        large_text="Coding",
    )
    time.sleep(5)


def example_multiplayer_status(manager: DiscordStatusManager):
    """Display a multiplayer game status."""
    print("\n--- Multiplayer Status Example ---")
    manager.update_status(
        state="🎮 Playing Valorant",
        details="In Competitive Match",
        large_image="discord",
        large_text="Valorant - Competitive",
        party_size=(4, 5),  # 4 out of 5 party members
    )
    time.sleep(5)


def run_custom_section(manager: DiscordStatusManager, section: str) -> None:
    """Run a single section defined in `discord_config.json`.

    The config should contain objects like `gaming`, `watching`, etc.
    Each object may contain keys: state, details, large_image, large_text,
    small_image, small_text, party_size (list/tuple), buttons (list).
    """
    cfg = CONFIG.get(section, {})
    if not cfg:
        print(f"⚠ No '{section}' section in config; skipping.")
        return

    kwargs = {}
    for key in ("state", "details", "large_image", "large_text", "small_image", "small_text"):
        if key in cfg:
            kwargs[key] = cfg[key]

    if "party_size" in cfg:
        try:
            kwargs["party_size"] = tuple(cfg["party_size"])
        except Exception:
            pass

    if "buttons" in cfg:
        kwargs["buttons"] = cfg["buttons"]

    print(f"\n--- Running custom '{section}' status ---")
    manager.update_status(**kwargs)
    time.sleep(cfg.get("duration", 5))


def get_client_id_interactive() -> str:
    # Priority: ENV -> config -> prompt user
    cid = os.environ.get("DISCORD_CLIENT_ID") or CONFIG.get("client_id")
    if cid:
        return str(cid)

    print("\nNo Discord Client ID found in environment or config.")
    cid = input("Enter your Discord Application ID (Client ID): ").strip()
    if cid:
        save = input("Save this ID to a local .env file for next time? [y/N]: ").strip().lower()
        if save == "y":
            try:
                with open('.env', 'w', encoding='utf-8') as f:
                    f.write(f"DISCORD_CLIENT_ID={cid}\n")
                print("✓ Saved Client ID to .env (this file is git-ignored)")
            except Exception as e:
                print(f"Failed to save .env: {e}")
    return cid


def run_all_examples():
    """Interactive runner to pick presets or custom config-based statuses."""
    CLIENT_ID = get_client_id_interactive()

    if not CLIENT_ID:
        print("❌ No Client ID provided. Aborting.")
        return

    manager = DiscordStatusManager(CLIENT_ID)

    if not manager.connect():
        print("Failed to connect to Discord. Make sure Discord is running.")
        return

    try:
        print("\n" + "=" * 50)
        print("Discord Status - Choose Mode")
        print("=" * 50)
        print("1) Run built-in presets (hardcoded examples)")
        print("2) Run custom statuses from discord_config.json (if present)")
        print("3) Run a single custom section by name")
        print("4) Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            example_gaming_status(manager)
            example_watching_status(manager)
            example_listening_status(manager)
            example_custom_status(manager)
            example_multiplayer_status(manager)

        elif choice == "2":
            # Run known sections in a sensible order if present
            for section in ("gaming", "watching", "listening", "custom", "multiplayer"):
                run_custom_section(manager, section)

        elif choice == "3":
            section = input("Enter section name (e.g. gaming, watching): ").strip()
            if section:
                run_custom_section(manager, section)
            else:
                print("No section name provided.")

        else:
            print("Exiting without changes.")

        print("\n✓ Done.")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect()


if __name__ == "__main__":
    run_all_examples()
