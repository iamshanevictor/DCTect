#!/usr/bin/env python3
"""
Discord Status Setup & Testing Utility
Helps with initial setup and testing of the Discord status manager.
"""

import sys
import json
import os
from pathlib import Path


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def get_client_id():
    """Get client ID from user input."""
    print_header("Discord Client ID Setup")
    print("\nTo get your Client ID:")
    print("1. Go to https://discord.com/developers/applications")
    print("2. Click 'New Application' and give it a name")
    print("3. Go to 'General Information'")
    print("4. Copy the 'Client ID' value")
    print("\n" + "-"*60)

    while True:
        client_id = input("\nEnter your Discord Client ID: ").strip()

        if not client_id:
            print("❌ Client ID cannot be empty!")
            continue

        if not client_id.isdigit() or len(client_id) < 15:
            print("❌ Invalid Client ID format! It should be a large number.")
            continue

        print(f"✓ Client ID accepted: {client_id}")
        return client_id


def update_script_client_id(client_id: str):
    """Update the CLIENT_ID in discord_status.py"""
    script_path = Path("discord_status.py")

    if not script_path.exists():
        print("❌ discord_status.py not found!")
        return False

    # Deprecated: we no longer write client IDs into source files.
    print("⚠ Skipping modification of source files. Writing Client ID to discord_config.json instead.")
    return set_client_id_in_config(client_id)


def update_examples_client_id(client_id: str):
    """Update the CLIENT_ID in examples.py"""
    script_path = Path("examples.py")

    if not script_path.exists():
        print("❌ examples.py not found!")
        return False

    # Deprecated: avoid putting secrets into source. Save to config instead.
    print("⚠ Skipping modification of examples.py. Writing Client ID to discord_config.json instead.")
    return set_client_id_in_config(client_id)


def set_client_id_in_config(client_id: str) -> bool:
    """Save the client id into a local `.env` file (which is ignored by git).

    Returns True on success.
    """
    env_path = Path(".env")
    try:
        # write or overwrite .env with the DISCORD_CLIENT_ID value
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f"DISCORD_CLIENT_ID={client_id}\n")
        print(f"✓ Saved Client ID to {env_path} (this file is ignored by git)")
        return True
    except Exception as e:
        print(f"❌ Failed to write .env: {e}")
        return False


def customize_config():
    """Customize the discord_config.json file."""
    print_header("Configuration Customization")

    config_path = Path("discord_config.json")

    if not config_path.exists():
        print("❌ discord_config.json not found!")
        return False

    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        print("\nCurrent configuration:")
        print(json.dumps(config, indent=2))

        print("\n" + "-"*60)
        print("Leave blank to keep current value.\n")

        # Get new values
        state = input(f"Enter state [{config['state']}]: ").strip()
        if state:
            config["state"] = state

        details = input(f"Enter details [{config['details']}]: ").strip()
        if details:
            config["details"] = details

        large_text = input(f"Enter large_text [{config['large_text']}]: ").strip()
        if large_text:
            config["large_text"] = large_text

        interval = input(f"Enter update_interval in seconds [{config['update_interval']}]: ").strip()
        if interval:
            try:
                config["update_interval"] = int(interval)
            except ValueError:
                print("⚠ Invalid number, keeping current value")

        # Save updated config
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print("\n✓ Configuration saved!")
        print("\nUpdated configuration:")
        print(json.dumps(config, indent=2))
        return True

    except Exception as e:
        print(f"❌ Error updating configuration: {e}")
        return False


def verify_installation():
    """Verify that all required files exist."""
    print_header("Verifying Installation")

    required_files = [
        "discord_status.py",
        "examples.py",
        "discord_config.json",
        "requirements.txt",
        "README.md",
    ]

    all_exist = True
    for file in required_files:
        path = Path(file)
        status = "✓" if path.exists() else "❌"
        print(f"{status} {file}")
        if not path.exists():
            all_exist = False

    if all_exist:
        print("\n✓ All required files found!")
    else:
        print("\n❌ Some files are missing!")

    return all_exist


def show_menu():
    """Show the main menu."""
    print_header("Discord Status Manager - Setup Utility")

    print("\nOptions:")
    print("1. Set Discord Client ID")
    print("2. Customize Configuration")
    print("3. Verify Installation")
    print("4. View README")
    print("5. Exit")

    return input("\nSelect an option (1-5): ").strip()


def view_readme():
    """Display the README file."""
    readme_path = Path("README.md")

    if not readme_path.exists():
        print("❌ README.md not found!")
        return

    try:
        with open(readme_path, "r") as f:
            print("\n" + f.read())
    except Exception as e:
        print(f"❌ Error reading README: {e}")


def main():
    """Main entry point."""
    print_header("Discord Status Manager Setup Utility")

    while True:
        choice = show_menu()

        if choice == "1":
            client_id = get_client_id()
            if update_script_client_id(client_id):
                update_examples_client_id(client_id)
                print("\n✓ Client ID setup complete!")

        elif choice == "2":
            customize_config()

        elif choice == "3":
            verify_installation()

        elif choice == "4":
            view_readme()

        elif choice == "5":
            print("\n👋 Goodbye!")
            break

        else:
            print("❌ Invalid option!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
