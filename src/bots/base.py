"""
Base Bot Class

This module provides the core functionality for creating Telegram bots.
"""

import os
import json
import logging
import asyncio
import redis
from telegram.ext import Application

logger = logging.getLogger(__name__)

class BotBase:
    """Base class for all bots."""
    
    def __init__(self):
        """Initialize bot instance."""
        self.application = None
        self.state = {}
        self._status = 'starting'
        self._redis = None
        self._setup()
    
    def _setup(self):
        """Initialize bot application and connections."""
        # Set up bot application
        self.application = Application.builder().token(
            os.getenv('BOT_TOKEN')
        ).build()
        
        # Set up Redis connection
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self._redis = redis.from_url(redis_url)
        
        # Load initial state
        self.state = self._load_state()
    
    def _load_state(self):
        """Load bot state from Redis."""
        try:
            state_key = f"bot_state:{os.getenv('BOT_TOKEN')}"
            state_data = self._redis.get(state_key)
            if state_data:
                return json.loads(state_data)
        except Exception as e:
            logger.error(f"Error loading state: {e}", exc_info=True)
        return {}
    
    def _save_state(self):
        """Save bot state to Redis."""
        try:
            state_key = f"bot_state:{os.getenv('BOT_TOKEN')}"
            state_data = json.dumps(self.state)
            self._redis.set(state_key, state_data)
        except Exception as e:
            logger.error(f"Error saving state: {e}", exc_info=True)
    
    def update_status(self, status, error=None, webhook_url=None):
        """Update bot status in Redis."""
        try:
            self._status = status
            status_key = f"bot:{os.getenv('BOT_TOKEN')}"
            status_data = {
                'status': status,
                'error': error,
                'webhook_url': webhook_url
            }
            self._redis.hmset(status_key, status_data)
        except Exception as e:
            logger.error(f"Error updating status: {e}", exc_info=True)
    
    async def start(self):
        """Initialize and start the bot.
        
        This method should be implemented by subclasses to set up
        handlers and start the bot.
        """
        raise NotImplementedError
    
    async def stop(self):
        """Clean up and stop the bot.
        
        This method should be implemented by subclasses to perform
        cleanup and stop the bot.
        """
        raise NotImplementedError
    
    def run(self):
        """Run the bot."""
        try:
            # Set up logging
            logging.basicConfig(
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=logging.INFO
            )
            
            # Create event loop
            loop = asyncio.get_event_loop()
            
            # Start bot
            loop.run_until_complete(self.start())
            
            # Run event loop
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("Stopping bot...")
            # Save state and stop bot
            self._save_state()
            loop.run_until_complete(self.stop())
        except Exception as e:
            logger.error(f"Error running bot: {e}", exc_info=True)
            self.update_status('error', str(e))
        finally:
            loop.close()