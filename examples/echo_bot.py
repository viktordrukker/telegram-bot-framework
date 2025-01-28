"""
Simple Echo Bot Example

This bot demonstrates basic functionality of the framework:
- Command handling
- Message handling
- State management
- Status reporting
"""

from telegram_bot_framework import BotBase
from telegram.ext import CommandHandler, MessageHandler, filters

class EchoBot(BotBase):
    def __init__(self):
        super().__init__()
        self.state = {
            'messages_echoed': 0,
            'users': set()
        }
    
    async def start(self):
        """Initialize bot and set up handlers."""
        # Set up command handlers
        self.application.add_handler(
            CommandHandler("start", self.cmd_start)
        )
        self.application.add_handler(
            CommandHandler("stats", self.cmd_stats)
        )
        
        # Set up message handlers
        self.application.add_handler(
            MessageHandler(filters.TEXT, self.handle_message)
        )
        
        # Start the bot
        await self.application.initialize()
        await self.application.start()
        self.update_status('running')
    
    async def stop(self):
        """Clean up and stop bot."""
        await self.application.stop()
        self.update_status('stopped')
    
    async def cmd_start(self, update, context):
        """Handle /start command."""
        user_id = update.effective_user.id
        self.state['users'].add(user_id)
        
        await update.message.reply_text(
            "Hello! I'm an Echo Bot. Send me any message and I'll repeat it!"
        )
    
    async def cmd_stats(self, update, context):
        """Handle /stats command."""
        await update.message.reply_text(
            f"Stats:\n"
            f"- Messages echoed: {self.state['messages_echoed']}\n"
            f"- Unique users: {len(self.state['users'])}"
        )
    
    async def handle_message(self, update, context):
        """Echo back the user's message."""
        user_id = update.effective_user.id
        self.state['users'].add(user_id)
        self.state['messages_echoed'] += 1
        
        await update.message.reply_text(update.message.text)

if __name__ == '__main__':
    bot = EchoBot()
    bot.run()