"""
Unit tests for Info Aziende Bot components
"""
import unittest
from unittest.mock import Mock, patch, AsyncMock
import discord
from datetime import datetime

# Import our modules
from api_client import OpenAPIClient
from embed_formatter import CompanyEmbedFormatter


class TestAPIClient(unittest.TestCase):
    """Test cases for OpenAPIClient"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = OpenAPIClient("test_token")
    
    def test_initialization(self):
        """Test client initialization"""
        self.assertEqual(self.client.api_token, "test_token")
        self.assertEqual(self.client.api_calls_count, 0)
        self.assertIsInstance(self.client.last_reset, datetime)
    
    def test_partita_iva_validation(self):
        """Test Partita IVA validation"""
        # Test with async wrapper
        import asyncio
        
        async def test_invalid():
            # Invalid: too short
            with self.assertRaises(ValueError):
                await self.client.get_company_info("123")
            
            # Invalid: too long
            with self.assertRaises(ValueError):
                await self.client.get_company_info("123456789012")
            
            # Invalid: contains letters
            with self.assertRaises(ValueError):
                await self.client.get_company_info("1234567890A")
        
        asyncio.run(test_invalid())
    
    def test_get_api_usage(self):
        """Test API usage tracking"""
        usage = self.client.get_api_usage()
        
        self.assertIn('calls_count', usage)
        self.assertIn('last_reset', usage)
        self.assertIn('hours_since_reset', usage)
        self.assertEqual(usage['calls_count'], 0)
    
    def test_reset_usage_counter(self):
        """Test resetting usage counter"""
        self.client.api_calls_count = 50
        old_reset_time = self.client.last_reset
        
        # Wait a tiny bit to ensure time difference
        import time
        time.sleep(0.01)
        
        self.client.reset_usage_counter()
        
        self.assertEqual(self.client.api_calls_count, 0)
        self.assertGreater(self.client.last_reset, old_reset_time)


class TestEmbedFormatter(unittest.TestCase):
    """Test cases for CompanyEmbedFormatter"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.formatter = CompanyEmbedFormatter()
    
    def test_emojis_exist(self):
        """Test that emoji dictionary is properly defined"""
        self.assertIsInstance(CompanyEmbedFormatter.EMOJIS, dict)
        self.assertIn('company', CompanyEmbedFormatter.EMOJIS)
        self.assertIn('vat', CompanyEmbedFormatter.EMOJIS)
        self.assertIn('error', CompanyEmbedFormatter.EMOJIS)
    
    def test_create_company_embed_with_data(self):
        """Test creating embed with valid company data"""
        test_data = {
            'denominazione': 'Test Company SRL',
            'partita_iva': '12345678901',
            'codice_fiscale': '12345678901',
            'stato': 'Attiva',
            'forma_giuridica': 'SRL',
            'capitale_sociale': 10000.00,
            'indirizzo': 'Via Roma 1',
            'cap': '00100',
            'comune': 'Roma',
            'provincia': 'RM',
            'rea': 'RM-123456',
            'ateco': '62.01.00',
            'descrizione_attivita': 'Produzione software',
            'data_iscrizione': '2020-01-01'
        }
        
        embed = self.formatter.create_company_embed(test_data)
        
        self.assertIsInstance(embed, discord.Embed)
        self.assertIn('Test Company SRL', embed.title)
        self.assertEqual(embed.color, discord.Color.blue())
        self.assertGreater(len(embed.fields), 0)
    
    def test_create_error_embed(self):
        """Test creating embed with error data"""
        error_data = {
            'error': 'Company not found',
            'status': 404
        }
        
        embed = self.formatter.create_company_embed(error_data)
        
        self.assertIsInstance(embed, discord.Embed)
        self.assertEqual(embed.color, discord.Color.red())
        self.assertIn('Errore', embed.title)
    
    def test_create_usage_embed(self):
        """Test creating usage statistics embed"""
        usage_data = {
            'calls_count': 25,
            'hours_since_reset': 5.5,
            'note': 'Free tier typically allows 100-500 requests per day'
        }
        
        embed = self.formatter.create_usage_embed(usage_data)
        
        self.assertIsInstance(embed, discord.Embed)
        self.assertIn('Utilizzo API', embed.title)
        self.assertGreater(len(embed.fields), 0)
    
    def test_usage_embed_color_coding(self):
        """Test that usage embed colors change based on usage"""
        # Low usage - should be green
        low_usage = {
            'calls_count': 10,
            'hours_since_reset': 1.0,
            'note': 'Test'
        }
        embed_low = self.formatter.create_usage_embed(low_usage)
        self.assertEqual(embed_low.color, discord.Color.green())
        
        # Medium usage - should be orange
        medium_usage = {
            'calls_count': 60,
            'hours_since_reset': 1.0,
            'note': 'Test'
        }
        embed_medium = self.formatter.create_usage_embed(medium_usage)
        self.assertEqual(embed_medium.color, discord.Color.orange())
        
        # High usage - should be red
        high_usage = {
            'calls_count': 90,
            'hours_since_reset': 1.0,
            'note': 'Test'
        }
        embed_high = self.formatter.create_usage_embed(high_usage)
        self.assertEqual(embed_high.color, discord.Color.red())


class TestBotConfiguration(unittest.TestCase):
    """Test bot configuration and setup"""
    
    def test_imports(self):
        """Test that all necessary modules can be imported"""
        try:
            import discord
            from discord.ext import commands
            import aiohttp
            from dotenv import load_dotenv
            success = True
        except ImportError as e:
            success = False
            print(f"Import error: {e}")
        
        self.assertTrue(success, "All required modules should be importable")
    
    def test_bot_file_structure(self):
        """Test that bot.py has the expected structure"""
        import os
        
        # Check that bot.py exists and is readable
        self.assertTrue(os.path.exists('bot.py'))
        
        with open('bot.py', 'r') as f:
            content = f.read()
            
            # Check for essential components
            self.assertIn('InfoAziendeBot', content)
            self.assertIn('hybrid_command', content)
            self.assertIn('search_company', content)
            self.assertIn('show_usage', content)
            self.assertIn('reset_usage', content)
            self.assertIn('show_help', content)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
