# Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       Info Aziende Bot                          │
│                   Discord Bot Architecture                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│   Discord User  │
│   (sends cmd)   │
└────────┬────────┘
         │ /azienda 12345678901
         │
         ▼
┌─────────────────────────────────────────┐
│          bot.py (Main Bot)              │
│  ┌───────────────────────────────────┐  │
│  │  @hybrid_command decorators       │  │
│  │  - search_company()               │  │
│  │  - show_usage()                   │  │
│  │  - reset_usage()                  │  │
│  │  - show_help()                    │  │
│  └───────────────────────────────────┘  │
└────────┬─────────────────────┬──────────┘
         │                     │
         │                     │ validate input
         │                     │
         ▼                     ▼
┌──────────────────────┐  ┌──────────────────────┐
│   api_client.py      │  │  embed_formatter.py  │
│   (API Requests)     │  │  (Rich Embeds)       │
│                      │  │                      │
│ - get_company_info() │  │ - create_embed()     │
│ - track usage        │  │ - format data        │
│ - validate P.IVA     │  │ - add emojis         │
└──────────┬───────────┘  └───────────┬──────────┘
           │                          │
           │ HTTP GET                 │
           │ Bearer Token             │
           ▼                          │
  ┌────────────────────┐              │
  │   OpenAPI.it API   │              │
  │ Company Advanced   │              │
  │      Italia        │              │
  └────────┬───────────┘              │
           │                          │
           │ JSON Response            │
           │                          │
           └──────────────────────────┘
                        │
                        │ formatted embed
                        ▼
              ┌─────────────────┐
              │  Discord User   │
              │ (receives embed)│
              └─────────────────┘
```

## Data Flow

1. **User Input** → Discord command with Partita IVA
2. **Validation** → Bot validates 11-digit format
3. **API Call** → Request sent to OpenAPI.it
4. **Tracking** → API call counter incremented
5. **Response** → JSON data received
6. **Formatting** → Data transformed to rich embed
7. **Display** → Embed sent back to Discord

## File Organization

```
Info-Aziende-Bot/
│
├── Core Application
│   ├── bot.py              # Discord bot + commands
│   ├── api_client.py       # OpenAPI.it client
│   └── embed_formatter.py  # Embed creation
│
├── Quality Assurance
│   ├── test_bot.py         # Unit tests
│   └── validate_config.py  # Configuration check
│
├── User Scripts
│   ├── run.sh             # Linux/Mac launcher
│   └── run.bat            # Windows launcher
│
├── Documentation
│   ├── README.md          # Full documentation
│   ├── QUICKSTART.md      # Quick setup guide
│   └── IMPLEMENTATION.md  # Technical details
│
└── Configuration
    ├── requirements.txt   # Python dependencies
    ├── .env.example      # Environment template
    └── .env              # Actual tokens (not in git)
```

## Command Flow

### /azienda Command
```
User: /azienda 12345678901
  │
  ├─► Validate input (11 digits)
  │   └─► ❌ Invalid → Send error embed
  │   └─► ✅ Valid → Continue
  │
  ├─► Call API (api_client.get_company_info)
  │   ├─► Increment usage counter
  │   └─► HTTP GET with Bearer token
  │       ├─► 200 OK → Return data
  │       ├─► 404 → Company not found
  │       ├─► 401 → Invalid token
  │       └─► 429 → Rate limit exceeded
  │
  ├─► Format response (embed_formatter.create_company_embed)
  │   ├─► Parse JSON data
  │   ├─► Add emojis
  │   ├─► Format fields
  │   └─► Create Discord Embed
  │
  └─► Send embed to user
      └─► User sees rich formatted company info
```

### /usage Command
```
User: /usage
  │
  ├─► Get usage stats (api_client.get_api_usage)
  │   ├─► Read call counter
  │   ├─► Calculate time since reset
  │   └─► Calculate percentage
  │
  ├─► Format usage embed (embed_formatter.create_usage_embed)
  │   ├─► Add call count
  │   ├─► Add time info
  │   ├─► Color code by percentage
  │   │   ├─► 0-50% = Green ✅
  │   │   ├─► 50-80% = Orange ⚠️
  │   │   └─► 80-100% = Red ❌
  │   └─► Add visual indicators
  │
  └─► Send embed to user
      └─► User sees API usage stats
```

## Security Layers

```
┌────────────────────────────────────┐
│  Environment Variables (.env)      │  ← Secrets not in code
├────────────────────────────────────┤
│  Input Validation                  │  ← 11-digit check
├────────────────────────────────────┤
│  API Authentication (Bearer)       │  ← Token-based auth
├────────────────────────────────────┤
│  Permission Checks (Admin only)    │  ← Discord perms
├────────────────────────────────────┤
│  Error Handling (Try/Catch)        │  ← Graceful failures
├────────────────────────────────────┤
│  Rate Limiting (Usage Monitor)     │  ← Stay in free tier
└────────────────────────────────────┘
```

## Emoji Mapping

The bot uses 20+ emojis for visual clarity:

| Category | Emojis |
|----------|--------|
| Company | 🏢 🆔 💳 |
| Location | 📍 🏙️ 🗺️ 📮 |
| Contact | 📞 📧 🌐 📨 |
| Status | ✅ ❌ ⚠️ |
| Financial | 💰 💵 |
| Legal | ⚖️ 📋 🏷️ |
| Info | ℹ️ 📊 📈 |

## Testing Coverage

```
test_bot.py (11 tests)
├── TestAPIClient (4 tests)
│   ├── test_initialization
│   ├── test_partita_iva_validation
│   ├── test_get_api_usage
│   └── test_reset_usage_counter
│
├── TestEmbedFormatter (5 tests)
│   ├── test_emojis_exist
│   ├── test_create_company_embed_with_data
│   ├── test_create_error_embed
│   ├── test_create_usage_embed
│   └── test_usage_embed_color_coding
│
└── TestBotConfiguration (2 tests)
    ├── test_imports
    └── test_bot_file_structure

Results: ✅ 11/11 passed (100%)
```

## Error Handling

Every level has error handling:

1. **Input Level**: Validate before API call
2. **API Level**: Handle HTTP errors (401, 404, 429)
3. **Format Level**: Handle missing data fields
4. **Display Level**: User-friendly error messages

```python
try:
    # Validate input
    # Call API
    # Format response
    # Send embed
except ValueError as e:
    # Validation error
except aiohttp.ClientError as e:
    # Network error
except Exception as e:
    # Catch-all error
```

## Performance

- **Async Operations**: All API calls are async
- **No Blocking**: Uses aiohttp, not requests
- **Fast Responses**: Typically < 2 seconds
- **Scalable**: Can handle multiple guilds

## Deployment Checklist

- [x] Python 3.8+ compatible
- [x] Cross-platform (Linux/Mac/Windows)
- [x] Dependencies documented
- [x] Environment variables template
- [x] Error handling complete
- [x] Security best practices
- [x] Tests passing (11/11)
- [x] Documentation complete
- [x] Ready for production

---
Generated: 2026-02-12
Status: ✅ Production Ready
