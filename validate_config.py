"""
Configuration Validator for Info Aziende Bot
Checks if the bot is properly configured before running
"""
import os
import sys
from pathlib import Path


def check_env_file():
    """Check if .env file exists"""
    if not Path('.env').exists():
        print("❌ .env file not found!")
        print("   Run: cp .env.example .env")
        print("   Then edit .env with your tokens")
        return False
    print("✅ .env file found")
    return True


def check_env_variables():
    """Check if required environment variables are set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    errors = []
    
    discord_token = os.getenv('DISCORD_TOKEN')
    if not discord_token or discord_token == 'your_discord_bot_token_here':
        errors.append("DISCORD_TOKEN not configured")
    else:
        print("✅ DISCORD_TOKEN is set")
    
    openapi_token = os.getenv('OPENAPI_TOKEN')
    if not openapi_token or openapi_token == 'your_openapi_token_here':
        errors.append("OPENAPI_TOKEN not configured")
    else:
        print("✅ OPENAPI_TOKEN is set")
    
    if errors:
        print("\n❌ Configuration errors:")
        for error in errors:
            print(f"   - {error}")
        print("\nPlease edit .env and add your actual tokens")
        return False
    
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'discord': 'discord.py',
        'aiohttp': 'aiohttp',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✅ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} not installed")
    
    if missing:
        print("\nInstall missing packages with:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True


def check_files():
    """Check if all required files exist"""
    required_files = ['bot.py', 'api_client.py', 'embed_formatter.py', 'requirements.txt']
    
    missing = []
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} found")
        else:
            missing.append(file)
            print(f"❌ {file} not found")
    
    if missing:
        print("\n❌ Missing required files")
        return False
    
    return True


def main():
    """Main validation function"""
    print("=" * 50)
    print("Info Aziende Bot - Configuration Validator")
    print("=" * 50)
    print()
    
    print("Checking files...")
    files_ok = check_files()
    print()
    
    print("Checking dependencies...")
    deps_ok = check_dependencies()
    print()
    
    print("Checking environment configuration...")
    env_file_ok = check_env_file()
    if env_file_ok:
        env_vars_ok = check_env_variables()
    else:
        env_vars_ok = False
    print()
    
    print("=" * 50)
    if all([files_ok, deps_ok, env_file_ok, env_vars_ok]):
        print("✅ All checks passed! Bot is ready to run.")
        print("\nStart the bot with: python bot.py")
        print("Or use the run script: ./run.sh (Linux/Mac) or run.bat (Windows)")
    else:
        print("❌ Configuration incomplete. Please fix the issues above.")
        sys.exit(1)
    print("=" * 50)


if __name__ == "__main__":
    main()
