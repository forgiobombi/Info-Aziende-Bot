# Info-Aziende-Bot 🇮🇹

A Discord bot that fetches and displays Italian company information using the **Partita IVA** (Italian VAT number) through the [OpenAPI.it](https://openapi.it/) Company Advanced Italia API.

## ✨ Features

- 🔍 **Company Search**: Look up Italian companies by their Partita IVA (11-digit VAT number)
- 🎨 **Beautiful Embeds**: Rich, formatted embeds with emojis for easy reading
- ⚡ **Hybrid Commands**: Support for both slash commands (`/`) and prefix commands (`!`)
- 📊 **API Usage Monitoring**: Track your API calls to stay within the free tier limits
- 🔒 **Admin Controls**: Reset usage counters (admin-only command)
- 🌐 **Comprehensive Data**: Display company name, address, legal form, capital, status, contacts, and more

## 📋 Prerequisites

- Python 3.8 or higher
- Discord Bot Token ([Create one here](https://discord.com/developers/applications))
- OpenAPI.it API Token ([Get one here](https://openapi.it/))

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/forgiobombi/Info-Aziende-Bot.git
   cd Info-Aziende-Bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your tokens:
     ```
     DISCORD_TOKEN=your_discord_bot_token_here
     OPENAPI_TOKEN=your_openapi_token_here
     ```

4. **Run the bot**:
   ```bash
   python bot.py
   ```

## 🎮 Commands

### `/azienda <partita_iva>`
Search for Italian company information using the Partita IVA (VAT number).

**Example:**
```
/azienda 12345678901
```

**Displays:**
- 🏢 Company name (Denominazione)
- 💳 Partita IVA
- 🆔 Codice Fiscale
- ✅ Company status (Stato)
- ⚖️ Legal form (Forma Giuridica)
- 💰 Share capital (Capitale Sociale)
- 📍 Full address
- 🏷️ ATECO code
- 🏭 Business sector/activity
- 📅 Registration date
- 📞 Contact information (phone, email, PEC, website)
- 📋 REA code

### `/usage`
Display current API usage statistics to monitor your consumption.

**Shows:**
- 📊 Number of API calls made
- ⏱️ Time since last reset
- 📈 Percentage of free tier limit used
- ⚠️ Warning status if approaching limit

### `/reset_usage`
Reset the API usage counter (Administrator permission required).

### `/help`
Display the help message with all available commands.

## 🔧 Configuration

### Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Copy the bot token and add it to your `.env` file
5. Enable "Message Content Intent" under Privileged Gateway Intents
6. Invite the bot to your server using OAuth2 URL with `bot` and `applications.commands` scopes

### OpenAPI.it Setup

1. Register at [OpenAPI.it](https://openapi.it/)
2. Subscribe to the "Company Advanced Italia" API
3. Copy your API token
4. Add it to your `.env` file

**Note:** The free tier typically allows 100-500 API calls per day. The bot tracks usage locally to help you stay within limits.

## 📊 API Usage Monitoring

The bot includes built-in API usage monitoring to help you stay within the free tier:

- **Local Counter**: Tracks API calls since bot startup
- **Usage Command**: Check current usage anytime with `/usage`
- **Visual Indicators**: Color-coded status (green = good, orange = warning, red = approaching limit)
- **Reset Option**: Administrators can reset the counter with `/reset_usage`

## 🗂️ Project Structure

```
Info-Aziende-Bot/
├── bot.py                 # Main bot file with Discord commands
├── api_client.py          # OpenAPI.it API client
├── embed_formatter.py     # Discord embed formatting with emojis
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment file
├── .env                  # Your environment file (not in git)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🔒 Security Notes

- Never commit your `.env` file or share your API tokens
- The `.env` file is already in `.gitignore` to prevent accidental commits
- Keep your Discord bot token and OpenAPI token secure
- Use administrator permissions carefully when deploying the bot

## 📝 Example Usage

1. **Search for a company:**
   ```
   User: /azienda 12345678901
   Bot: [Displays rich embed with company information]
   ```

2. **Check API usage:**
   ```
   User: /usage
   Bot: [Shows API usage statistics with color-coded status]
   ```

3. **Get help:**
   ```
   User: /help
   Bot: [Displays all available commands and usage instructions]
   ```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAPI.it](https://openapi.it/) for providing the Italian company data API
- [discord.py](https://github.com/Rapptz/discord.py) for the excellent Discord bot framework

## 💡 Tips

- The Partita IVA must be exactly 11 digits
- The bot automatically validates input before making API calls
- Use the `/usage` command regularly to monitor your API consumption
- Free tier limits are approximate; check OpenAPI.it for exact limits
- Hybrid commands work as both slash commands (`/`) and prefix commands (`!`)

## 🐛 Troubleshooting

**Bot doesn't respond to commands:**
- Ensure "Message Content Intent" is enabled in Discord Developer Portal
- Check that the bot has proper permissions in your server
- Verify your Discord token is correct in `.env`

**API errors:**
- Verify your OpenAPI token is valid
- Check if you've exceeded your API rate limit
- Ensure the Partita IVA format is correct (11 digits)

**Commands not showing as slash commands:**
- Wait a few minutes for Discord to sync commands
- Try kicking and re-inviting the bot with proper scopes
- Ensure `applications.commands` scope was included when inviting the bot

---

Made with ❤️ for the Italian business community