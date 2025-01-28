# Getting Started with Telegram Bot Framework

This guide will help you set up your development environment and create your first bot using the framework.

## Prerequisites

Before you begin, ensure you have:

1. Python 3.10 or higher installed
2. Redis server running
3. A Telegram Bot Token (get one from [@BotFather](https://t.me/botfather))
4. Basic knowledge of Python and async/await

## Installation

1. **Create a new project directory**:
```bash
mkdir my-telegram-bot
cd my-telegram-bot
```

2. **Set up a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

3. **Install the framework**:
```bash
pip install telegram-bot-framework
```

## Basic Bot Setup

1. **Create your bot file** (`my_bot.py`):
```python
from telegram_bot_framework import BotBase
from telegram.ext import CommandHandler, MessageHandler, filters

class MyFirstBot(BotBase):
    def __init__(self):
        super().__init__()
        self.state = {
            'messages_received': 0
        }
    
    async def start(self):
        """Initialize bot and set up handlers."""
        # Set up command handlers
        self.application.add_handler(
            CommandHandler("start", self.cmd_start)
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
        await update.message.reply_text(
            "Hello! I'm your first bot!"
        )
    
    async def handle_message(self, update, context):
        """Handle text messages."""
        self.state['messages_received'] += 1
        await update.message.reply_text(
            f"Message received! Total messages: {self.state['messages_received']}"
        )
```

2. **Create environment file** (`.env`):
```bash
BOT_TOKEN=your-bot-token-from-botfather
REDIS_URL=redis://localhost:6379/0
```

3. **Create runner script** (`main.py`):
```python
from my_bot import MyFirstBot

if __name__ == '__main__':
    bot = MyFirstBot()
    bot.run()
```

4. **Run your bot**:
```bash
python main.py
```

## State Management

The framework provides built-in state persistence through Redis:

```python
# State is automatically loaded on start
self.state = {
    'counter': 0,
    'users': set(),
    'settings': {}
}

# Update state
self.state['counter'] += 1

# State is automatically saved on stop
```

## Status Reporting

Keep track of your bot's status:

```python
# Update bot status
self.update_status(
    status='running',
    error=None,
    webhook_url=None
)

# Available status types:
# - running
# - error
# - stopped
# - starting
# - stopping
```

## Error Handling

Implement proper error handling:

```python
try:
    result = await some_operation()
except Exception as e:
    self.update_status('error', str(e))
    logger.error(f"Error: {e}", exc_info=True)
    # Handle the error appropriately
```

## Next Steps

1. Check out the [Bot Development Guide](bot_development.md) for more advanced features
2. Learn about [State Management](state_management.md) in detail
3. Explore [Deployment Options](deployment.md)
4. Browse [Example Bots](../examples/) for inspiration

## Common Issues

1. **Bot not responding**:
   - Check if your bot token is correct
   - Ensure Redis is running
   - Check your internet connection

2. **State not persisting**:
   - Verify Redis connection
   - Check Redis permissions
   - Ensure proper state serialization

3. **Handlers not working**:
   - Verify handler registration order
   - Check message filters
   - Enable debug logging

## Getting Help

If you run into issues:

1. Check the [documentation](../README.md)
2. Look for similar [issues](https://github.com/your-username/telegram-bot-framework/issues)
3. Ask in [discussions](https://github.com/your-username/telegram-bot-framework/discussions)
4. Open a new issue if needed