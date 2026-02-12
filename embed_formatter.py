"""
Discord Embed Formatter for Italian Company Information
"""
import discord
from typing import Dict, Any


class CompanyEmbedFormatter:
    """Format company data into beautiful Discord embeds with emojis"""
    
    # Emoji mappings for different fields
    EMOJIS = {
        "company": "🏢",
        "id": "🆔",
        "vat": "💳",
        "address": "📍",
        "city": "🏙️",
        "province": "🗺️",
        "zip": "📮",
        "phone": "📞",
        "email": "📧",
        "website": "🌐",
        "status": "✅",
        "inactive": "❌",
        "capital": "💰",
        "employees": "👥",
        "revenue": "💵",
        "sector": "🏭",
        "legal_form": "⚖️",
        "registration": "📅",
        "rea": "📋",
        "ateco": "🏷️",
        "pec": "📨",
        "warning": "⚠️",
        "error": "❌",
        "success": "✅",
        "info": "ℹ️"
    }
    
    @staticmethod
    def create_company_embed(data: Dict[str, Any]) -> discord.Embed:
        """
        Create a formatted embed from company data
        
        Args:
            data: Company data dictionary from API
            
        Returns:
            Discord Embed object
        """
        # Check for errors first
        if "error" in data:
            return CompanyEmbedFormatter._create_error_embed(data)
        
        # Create main embed
        embed = discord.Embed(
            title=f"{CompanyEmbedFormatter.EMOJIS['company']} {data.get('denominazione', 'N/A')}",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        
        # Add company identification
        if data.get('partita_iva'):
            embed.add_field(
                name=f"{CompanyEmbedFormatter.EMOJIS['vat']} Partita IVA",
                value=f"`{data['partita_iva']}`",
                inline=True
            )
        
        if data.get('codice_fiscale'):
            embed.add_field(
                name=f"{CompanyEmbedFormatter.EMOJIS['id']} Codice Fiscale",
                value=f"`{data['codice_fiscale']}`",
                inline=True
            )
        
        # Add status
        status = data.get('stato', 'N/A')
        status_emoji = CompanyEmbedFormatter.EMOJIS['status'] if status.lower() in ['attiva', 'active'] else CompanyEmbedFormatter.EMOJIS['inactive']
        embed.add_field(
            name=f"{status_emoji} Stato",
            value=status,
            inline=True
        )
        
        # Add legal form
        if data.get('forma_giuridica'):
            embed.add_field(
                name=f"{CompanyEmbedFormatter.EMOJIS['legal_form']} Forma Giuridica",
                value=data['forma_giuridica'],
                inline=True
            )
        
        # Add capital
        if data.get('capitale_sociale'):
            capital = data['capitale_sociale']
            if isinstance(capital, (int, float)):
                capital_str = f"€ {capital:,.2f}"
            else:
                capital_str = str(capital)
            embed.add_field(
                name=f"{CompanyEmbedFormatter.EMOJIS['capital']} Capitale Sociale",
                value=capital_str,
                inline=True
            )
        
        # Add REA code
        if data.get('rea'):
            embed.add_field(
                name=f"{CompanyEmbedFormatter.EMOJIS['rea']} Codice REA",
                value=data['rea'],
                inline=True
            )
        
        # Add address information
        address_parts = []
        if data.get('indirizzo'):
            address_parts.append(data['indirizzo'])
        if data.get('cap'):
            address_parts.append(data['cap'])
        if data.get('comune'):
            address_parts.append(data['comune'])
        if data.get('provincia'):
            address_parts.append(f"({data['provincia']})")
        
        if address_parts:
            embed.add_field(
                name=f"{CompanyEmbedFormatter.EMOJIS['address']} Indirizzo",
                value=" ".join(address_parts),
                inline=False
            )
        
        # Add ATECO code
        if data.get('ateco'):
            ateco = data['ateco']
            ateco_str = ateco if isinstance(ateco, str) else str(ateco)
            embed.add_field(
                name=f"{CompanyEmbedFormatter.EMOJIS['ateco']} Codice ATECO",
                value=ateco_str,
                inline=True
            )
        
        # Add sector/activity description
        if data.get('descrizione_attivita'):
            descrizione = data['descrizione_attivita']
            embed.add_field(
                name=f"{CompanyEmbedFormatter.EMOJIS['sector']} Attività",
                value=descrizione[:100] + ('...' if len(descrizione) > 100 else ''),
                inline=False
            )
        
        # Add registration date
        if data.get('data_iscrizione'):
            embed.add_field(
                name=f"{CompanyEmbedFormatter.EMOJIS['registration']} Data Iscrizione",
                value=data['data_iscrizione'],
                inline=True
            )
        
        # Add contact information
        contact_info = []
        if data.get('telefono'):
            contact_info.append(f"{CompanyEmbedFormatter.EMOJIS['phone']} {data['telefono']}")
        if data.get('email'):
            contact_info.append(f"{CompanyEmbedFormatter.EMOJIS['email']} {data['email']}")
        if data.get('pec'):
            contact_info.append(f"{CompanyEmbedFormatter.EMOJIS['pec']} PEC: {data['pec']}")
        if data.get('sito_web'):
            contact_info.append(f"{CompanyEmbedFormatter.EMOJIS['website']} {data['sito_web']}")
        
        if contact_info:
            embed.add_field(
                name="📞 Contatti",
                value="\n".join(contact_info),
                inline=False
            )
        
        # Add footer
        embed.set_footer(text="Dati forniti da OpenAPI.it")
        
        return embed
    
    @staticmethod
    def _create_error_embed(data: Dict[str, Any]) -> discord.Embed:
        """Create an error embed"""
        error_msg = data.get('error', 'Unknown error')
        
        embed = discord.Embed(
            title=f"{CompanyEmbedFormatter.EMOJIS['error']} Errore",
            description=error_msg,
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        
        if data.get('status'):
            embed.add_field(
                name="Status Code",
                value=f"`{data['status']}`",
                inline=True
            )
        
        if data.get('details'):
            embed.add_field(
                name="Dettagli",
                value=f"```{data['details'][:200]}```",
                inline=False
            )
        
        return embed
    
    @staticmethod
    def create_usage_embed(usage_data: Dict[str, Any]) -> discord.Embed:
        """
        Create an embed showing API usage statistics
        
        Args:
            usage_data: API usage data dictionary
            
        Returns:
            Discord Embed object
        """
        embed = discord.Embed(
            title=f"{CompanyEmbedFormatter.EMOJIS['info']} Utilizzo API",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        
        calls = usage_data.get('calls_count', 0)
        hours = usage_data.get('hours_since_reset', 0)
        
        embed.add_field(
            name="📊 Chiamate Effettuate",
            value=f"`{calls}`",
            inline=True
        )
        
        embed.add_field(
            name="⏱️ Ore dall'ultimo reset",
            value=f"`{hours:.2f}`",
            inline=True
        )
        
        # Calculate percentage of free tier (assuming 100 calls/day)
        free_tier_limit = 100
        percentage = (calls / free_tier_limit) * 100
        
        if percentage < 50:
            status = f"{CompanyEmbedFormatter.EMOJIS['success']} Ottimo"
            color = discord.Color.green()
        elif percentage < 80:
            status = f"{CompanyEmbedFormatter.EMOJIS['warning']} Attenzione"
            color = discord.Color.orange()
        else:
            status = f"{CompanyEmbedFormatter.EMOJIS['error']} Limite vicino"
            color = discord.Color.red()
        
        embed.color = color
        
        embed.add_field(
            name="📈 Utilizzo del Limite Giornaliero",
            value=f"{status} - `{percentage:.1f}%` di {free_tier_limit} chiamate",
            inline=False
        )
        
        embed.add_field(
            name=f"{CompanyEmbedFormatter.EMOJIS['info']} Nota",
            value=usage_data.get('note', 'Tier gratuito limitato'),
            inline=False
        )
        
        embed.set_footer(text="Contatore locale - resetta all'avvio del bot")
        
        return embed
