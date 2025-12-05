"""
Discord Status Detector and Updater
This program detects Discord and updates your playing status using pypresence.
"""

import os
import sys
import time
import json
from pathlib import Path
from pypresence import Presence
from typing import Optional, Dict, Any


class DiscordStatusManager:
    """Manages Discord Rich Presence and status updates."""

    def __init__(self, client_id: str, config_file: str = "discord_config.json"):
        """
        Initialize the Discord Status Manager.

        Args:
            client_id: Your Discord Application Client ID
            config_file: Path to configuration file
        """
        self.client_id = client_id
        self.config_file = config_file
        self.rpc: Optional[Presence] = None
        self.is_connected = False
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")

        # Default configuration
        return {
            "state": "Playing a game",
            "details": "Enjoying Discord",
            "large_image": "discord",
            "large_text": "Discord Rich Presence",
            "small_image": None,
            "small_text": None,
            "update_interval": 15,  # seconds
            "auto_start": True,
        }

    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=4)
            print(f"Configuration saved to {self.config_file}")
        except Exception as e:
            print(f"Error saving config: {e}")

    def connect(self) -> bool:
        """
        Connect to Discord.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.is_connected = True
            print("✓ Successfully connected to Discord!")
            return True
        except Exception as e:
            print(f"✗ Failed to connect to Discord: {e}")
            self.is_connected = False
            return False

    def disconnect(self) -> None:
        """Disconnect from Discord."""
        if self.rpc and self.is_connected:
            try:
                self.rpc.close()
                self.is_connected = False
                print("✓ Disconnected from Discord")
            except Exception as e:
                print(f"Error disconnecting: {e}")

    def update_status(
        self,
        state: Optional[str] = None,
        details: Optional[str] = None,
        large_image: Optional[str] = None,
        large_text: Optional[str] = None,
        small_image: Optional[str] = None,
        small_text: Optional[str] = None,
        party_id: Optional[str] = None,
        party_size: Optional[tuple] = None,
        buttons: Optional[list] = None,
    ) -> bool:
        """
        Update Discord status.

        Args:
            state: The user's current state (e.g., "Playing", "Watching")
            details: Details about the current activity
            large_image: Large image asset name
            large_text: Hover text for large image
            small_image: Small image asset name
            small_text: Hover text for small image
            party_id: Party ID for multiplayer info
            party_size: Tuple of (current_size, max_size)
            buttons: List of button dicts with "label" and "url" keys

        Returns:
            True if update successful, False otherwise
        """
        if not self.is_connected or not self.rpc:
            print("Not connected to Discord. Call connect() first.")
            return False

        try:
            # Use provided values or fallback to config
            update_data = {
                "state": state or self.config.get("state"),
                "details": details or self.config.get("details"),
                "large_image": large_image or self.config.get("large_image"),
                "large_text": large_text or self.config.get("large_text"),
                "start": time.time(),
            }

            # Add optional parameters
            if small_image or self.config.get("small_image"):
                update_data["small_image"] = small_image or self.config.get("small_image")

            if small_text or self.config.get("small_text"):
                update_data["small_text"] = small_text or self.config.get("small_text")

            if party_id:
                update_data["party_id"] = party_id

            if party_size:
                update_data["party_size"] = party_size

            if buttons:
                update_data["buttons"] = buttons

            self.rpc.update(**update_data)
            print(f"✓ Status updated: {state or self.config.get('state')}")
            return True

        except Exception as e:
            print(f"✗ Error updating status: {e}")
            return False

    def run_continuous(self, duration: Optional[int] = None) -> None:
        """
        Run continuous status updates.

        Args:
            duration: How long to run in seconds (None = infinite)
        """
        if not self.connect():
            return

        start_time = time.time()
        update_interval = self.config.get("update_interval", 15)

        try:
            print(f"\n{'='*50}")
            print("Discord Status Manager Running")
            print(f"Update Interval: {update_interval} seconds")
            print(f"Duration: {'Infinite' if duration is None else f'{duration} seconds'}")
            print("Press Ctrl+C to stop...")
            print(f"{'='*50}\n")

            self.update_status()

            while True:
                if duration and (time.time() - start_time) > duration:
                    break

                time.sleep(update_interval)
                self.update_status()

        except KeyboardInterrupt:
            print("\n\nKeyboard interrupt received...")
        except Exception as e:
            print(f"Error during execution: {e}")
        finally:
            self.disconnect()


def main():
    """Main entry point."""
    # Get client id from environment first, then from config file
    CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
    if not CLIENT_ID:
        # try read from config file (discord_config.json)
        config_path = Path("discord_config.json")
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    CLIENT_ID = cfg.get("client_id")
            except Exception:
                CLIENT_ID = None

    if not CLIENT_ID:
        print("⚠ ERROR: No Discord Client ID found.")
        print("Set the environment variable DISCORD_CLIENT_ID or add 'client_id' to discord_config.json")
        print("To get your Client ID:")
        print("1. Go to https://discord.com/developers/applications")
        print("2. Create or open an Application")
        print("3. Copy the Application (Client) ID")
        sys.exit(1)

    # Initialize the manager
    manager = DiscordStatusManager(CLIENT_ID)

    # Save default config if it doesn't exist
    if not os.path.exists(manager.config_file):
        manager.save_config()

    # Example: Update with custom status
    if manager.connect():
        # Simple status update
        manager.update_status(
            state="🎮 Playing Elden Ring",
            details="Exploring the Lands Between",
            large_image="discord",
            large_text="Discord Rich Presence",
        )

        # Keep the status active
        manager.run_continuous()


if __name__ == "__main__":
    main()
