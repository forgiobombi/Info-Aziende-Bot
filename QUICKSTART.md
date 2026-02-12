# Quick Start Guide - Info Aziende Bot

## 🚀 Fast Setup (5 minutes)

### Step 1: Get Your Tokens

1. **Discord Bot Token**
   - Go to: https://discord.com/developers/applications
   - Click "New Application" and give it a name
   - Go to "Bot" section → Click "Add Bot"
   - Under "Token" click "Reset Token" and copy it
   - ⚠️ Important: Enable "Message Content Intent" in Bot settings

2. **OpenAPI.it Token**
   - Register at: https://openapi.it/
   - Subscribe to "Company Advanced Italia" (free tier available)
   - Copy your API token from the dashboard

### Step 2: Configure the Bot

```bash
# Clone and enter directory
cd Info-Aziende-Bot

# Copy environment template
cp .env.example .env

# Edit .env and paste your tokens
nano .env  # or use any text editor
```

In `.env` file, replace:
```
DISCORD_TOKEN=paste_your_discord_token_here
OPENAPI_TOKEN=paste_your_openapi_token_here
```

### Step 3: Install & Run

**Option A - Using the run script (Recommended):**
```bash
# Linux/Mac
./run.sh

# Windows
run.bat
```

**Option B - Manual:**
```bash
pip install -r requirements.txt
python bot.py
```

### Step 4: Invite Bot to Your Server

1. Go to Discord Developer Portal → Your App → OAuth2 → URL Generator
2. Select scopes: `bot` and `applications.commands`
3. Select permissions: 
   - Send Messages
   - Embed Links
   - Read Message History
   - Use Slash Commands
4. Copy the generated URL and open it in browser
5. Select your server and authorize

## 📱 Using the Bot

### Search for a Company
```
/azienda 12345678901
```
Replace with actual 11-digit Partita IVA

### Check API Usage
```
/usage
```

### Reset Counter (Admin Only)
```
/reset_usage
```

### Get Help
```
/help
```

## 🔍 Finding a Partita IVA

Need to find a company's Partita IVA?
- Search on Google: "company name partita iva"
- Check company website (usually in footer or legal page)
- Use official registries: https://www.registroimprese.it/

## ⚠️ Troubleshooting

**"Application did not respond"**
- Check that bot is running (look for "Bot connected as..." message)
- Verify Discord token is correct in `.env`

**"Invalid API token"**
- Verify OpenAPI token in `.env`
- Check you're subscribed to Company Advanced Italia API

**Commands not showing as slash commands**
- Wait 5-10 minutes after inviting bot
- Make sure you selected `applications.commands` scope
- Try kicking and re-inviting the bot

**"Partita IVA must be 11 digits"**
- Ensure you entered exactly 11 numeric digits
- Remove any spaces or special characters

## 📊 API Usage Limits

**Free Tier:** Typically 100-500 calls per day
- The bot tracks usage locally
- Use `/usage` command to monitor
- Counter resets when bot restarts
- Administrators can reset with `/reset_usage`

## 💡 Tips

✅ Save frequently searched companies' P.IVA for quick access
✅ Check `/usage` regularly to avoid hitting limits
✅ The bot works in DMs too!
✅ Use descriptive server channels like `#company-lookup`
✅ Pin important company info for easy reference

## 🆘 Need Help?

1. Run the config validator: `python validate_config.py`
2. Check the logs in your terminal
3. Review the full README.md
4. Check Discord Developer Portal for token issues

## 🎉 You're All Set!

Start searching Italian companies by their Partita IVA!
