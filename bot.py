"""
Info Aziende Discord Bot - Italian Company Information Bot
Fetches and displays Italian company data using OpenAPI.it API
"""
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import logging
from typing import Optional

from api_client import OpenAPIClient
from embed_formatter import CompanyEmbedFormatter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('InfoAziendeBot')

# Load environment variables
load_dotenv()

# Get tokens from environment
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAPI_TOKEN = os.getenv('OPENAPI_TOKEN')

# Validate tokens
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables")
if not OPENAPI_TOKEN:
    raise ValueError("OPENAPI_TOKEN not found in environment variables")


class InfoAziendeBot(commands.Bot):
    """Discord Bot for Italian Company Information Lookup"""
    
    def __init__(self):
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Initialize bot with hybrid commands (slash + prefix)
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        # Initialize API client
        self.api_client = OpenAPIClient(OPENAPI_TOKEN)
        self.formatter = CompanyEmbedFormatter()
        
        logger.info("Bot initialized successfully")
    
    async def setup_hook(self):
        """Setup hook called when bot is starting"""
        # Sync commands with Discord
        await self.tree.sync()
        logger.info("Command tree synced")
    
    async def on_ready(self):
        """Event handler for when bot is ready"""
        logger.info(f'Bot connected as {self.user} (ID: {self.user.id})')
        logger.info(f'Connected to {len(self.guilds)} guilds')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Italian companies 🇮🇹"
            )
        )


# Create bot instance
bot = InfoAziendeBot()


@bot.hybrid_command(
    name="azienda",
    description="Cerca informazioni su un'azienda italiana tramite Partita IVA"
)
@app_commands.describe(
    partita_iva="Partita IVA dell'azienda (11 cifre)"
)
async def search_company(ctx: commands.Context, partita_iva: str):
    """
    Search for Italian company information by Partita IVA (VAT number)
    
    Args:
        ctx: Command context
        partita_iva: Italian VAT number (11 digits)
    """
    # Defer the response as API call might take time
    await ctx.defer()
    
    try:
        # Clean the partita_iva input (remove spaces and special characters)
        partita_iva = ''.join(filter(str.isdigit, partita_iva))
        
        # Validate input length
        if len(partita_iva) != 11:
            embed = discord.Embed(
                title="❌ Errore di Validazione",
                description=f"La Partita IVA deve essere di 11 cifre. Hai inserito {len(partita_iva)} cifre.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        logger.info(f"Searching for company with Partita IVA: {partita_iva}")
        
        # Fetch company data from API
        company_data = await bot.api_client.get_company_info(partita_iva)
        
        # Create embed from data
        embed = bot.formatter.create_company_embed(company_data)
        
        # Send the embed
        await ctx.send(embed=embed)
        
        logger.info(f"Company information sent for P.IVA: {partita_iva}")
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        embed = discord.Embed(
            title="❌ Errore di Validazione",
            description=str(e),
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        logger.error(f"Error processing command: {e}", exc_info=True)
        embed = discord.Embed(
            title="❌ Errore",
            description=f"Si è verificato un errore durante la ricerca: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


@bot.hybrid_command(
    name="usage",
    description="Mostra le statistiche di utilizzo dell'API"
)
async def show_usage(ctx: commands.Context):
    """
    Show API usage statistics
    
    Args:
        ctx: Command context
    """
    try:
        # Get usage data
        usage_data = bot.api_client.get_api_usage()
        
        # Create usage embed
        embed = bot.formatter.create_usage_embed(usage_data)
        
        # Send the embed
        await ctx.send(embed=embed)
        
        logger.info("API usage statistics displayed")
        
    except Exception as e:
        logger.error(f"Error showing usage: {e}", exc_info=True)
        embed = discord.Embed(
            title="❌ Errore",
            description=f"Errore nel recupero delle statistiche: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


@bot.hybrid_command(
    name="reset_usage",
    description="Resetta il contatore di utilizzo dell'API (solo admin)"
)
@commands.has_permissions(administrator=True)
async def reset_usage(ctx: commands.Context):
    """
    Reset the API usage counter (admin only)
    
    Args:
        ctx: Command context
    """
    try:
        bot.api_client.reset_usage_counter()
        
        embed = discord.Embed(
            title="✅ Reset Completato",
            description="Il contatore di utilizzo dell'API è stato resettato.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
        logger.info(f"API usage counter reset by {ctx.author}")
        
    except Exception as e:
        logger.error(f"Error resetting usage: {e}", exc_info=True)
        embed = discord.Embed(
            title="❌ Errore",
            description=f"Errore nel reset del contatore: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


@bot.hybrid_command(
    name="help",
    description="Mostra i comandi disponibili"
)
async def show_help(ctx: commands.Context):
    """
    Show available commands
    
    Args:
        ctx: Command context
    """
    embed = discord.Embed(
        title="🤖 Info Aziende Bot - Guida",
        description="Bot per cercare informazioni sulle aziende italiane usando la Partita IVA",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📋 /azienda <partita_iva>",
        value="Cerca informazioni su un'azienda italiana usando la Partita IVA (11 cifre)\nEsempio: `/azienda 12345678901`",
        inline=False
    )
    
    embed.add_field(
        name="📊 /usage",
        value="Mostra le statistiche di utilizzo dell'API OpenAPI.it",
        inline=False
    )
    
    embed.add_field(
        name="🔄 /reset_usage",
        value="Resetta il contatore di utilizzo (solo amministratori)",
        inline=False
    )
    
    embed.add_field(
        name="❓ /help",
        value="Mostra questo messaggio di aiuto",
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ Informazioni",
        value="Il bot utilizza l'API di OpenAPI.it per recuperare dati ufficiali sulle aziende italiane.",
        inline=False
    )
    
    embed.set_footer(text="Powered by OpenAPI.it")
    
    await ctx.send(embed=embed)


# Error handler for missing permissions
@reset_usage.error
async def reset_usage_error(ctx: commands.Context, error):
    """Handle errors for reset_usage command"""
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ Permessi Insufficienti",
            description="Solo gli amministratori possono utilizzare questo comando.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


def main():
    """Main entry point"""
    try:
        logger.info("Starting Info Aziende Bot...")
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
