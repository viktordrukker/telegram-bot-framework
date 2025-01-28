# Telegram Bot Framework

A lightweight, extensible framework for building Telegram bots with Python. This framework provides a standardized way to create, manage, and monitor Telegram bots with built-in state management and status reporting.

## Features

- 🤖 Easy-to-use bot development interface
- 📦 Built-in state persistence with Redis
- 🔄 Automatic status reporting
- 🐳 Docker support out of the box
- 🧩 Extensible architecture
- 📊 Integration with monitoring systems
- ⚡ Async/await support
- 🔒 Security best practices

## Quick Start

1. **Create a new bot project**:
```bash
git clone https://github.com/your-username/telegram-bot-framework.git
cd telegram-bot-framework
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

2. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your settings:
# BOT_TOKEN=your-bot-token
# REDIS_URL=redis://localhost:6379/0
```

3. **Create your first bot**:
```python
from src.bots.base import BotBase

class MyBot(BotBase):
    async def start(self):
        """Initialize bot and set up handlers."""
        self.application.add_handler(
            CommandHandler("start", self.cmd_start)
        )
        await self.application.initialize()
        await self.application.start()
        self.update_status('running')
    
    async def cmd_start(self, update, context):
        """Handle /start command."""
        await update.message.reply_text("Hello! I'm your bot!")
```

4. **Run your bot**:
```bash
python src/main.py
```

## Documentation

- [Getting Started Guide](docs/getting_started.md)
- [Bot Development Guide](docs/bot_development.md)
- [State Management](docs/state_management.md)
- [Deployment Guide](docs/deployment.md)
- [API Reference](docs/api_reference.md)

## Prerequisites

- Python 3.10+
- Redis server
- python-telegram-bot v20.0+

## Installation

### Using pip

```bash
pip install telegram-bot-framework
```

### From source

```bash
git clone https://github.com/your-username/telegram-bot-framework.git
cd telegram-bot-framework
pip install -e .
```

## Docker Support

Build and run your bot using Docker:

```bash
# Build image
docker build -t my-telegram-bot .

# Run container
docker run -d \
  --name my_bot \
  --env-file .env \
  my-telegram-bot
```

## Examples

Check out example bots in the [examples](examples/) directory:

- Echo Bot - Simple message echo bot
- Number Converter - Number base conversion bot
- State Management Demo - Bot demonstrating state persistence
- Webhook Example - Bot using webhooks instead of polling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📚 [Documentation](docs/)
- 💬 [Discussions](https://github.com/your-username/telegram-bot-framework/discussions)
- 🐛 [Issue Tracker](https://github.com/your-username/telegram-bot-framework/issues)