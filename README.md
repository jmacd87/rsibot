# Bitcoin RSI Alert Bot

A Python bot that monitors the Relative Strength Index (RSI) for Bitcoin (BTC) on Hyperliquid using 5-minute candles. When RSI crosses above or below user-defined thresholds, the bot sends real-time alerts via email (Gmail SMTP). Designed for traders who want to catch overbought/oversold conditions without constantly watching the charts.

## Features

- Accurate RSI calculation (matches TradingView/Hyperliquid)
- Configurable RSI thresholds and monitoring interval
- Sends alerts only on threshold crossings (prevents duplicate spam)
- Secure configuration via `.env` file (no secrets in code)
- Easy deployment to Railway, Render, or any cloud/server
- Robust error handling and logging

## Prerequisites

- Python 3.7+
- Gmail account with App Password (for email alerts)
- Hyperliquid API access

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd rsi-bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure your settings:
   - Create a `.env` file in the project root with the following content:
```
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECIPIENT=recipient@gmail.com
HYPERLIQUID_API_URL=https://api.hyperliquid.xyz/info
SYMBOL=BTC
TIMEFRAME=5m
RSI_OVERBOUGHT=68
RSI_OVERSOLD=32
CHECK_INTERVAL=1
```
   - [How to get a Gmail App Password](https://support.google.com/accounts/answer/185833)

## Usage

Run the bot:
```bash
python rsi_bot.py
```

The bot will:
1. Start monitoring Bitcoin RSI every 1 minute (or your configured interval)
2. Send email alerts when RSI reaches overbought (≥68) or oversold (≤32) conditions
3. Prevent duplicate alerts for the same condition until RSI crosses back above/below the threshold

## Configuration

You can modify the following parameters in your `.env` file:
- `RSI_OVERBOUGHT`: Overbought threshold (default: 68)
- `RSI_OVERSOLD`: Oversold threshold (default: 32)
- `CHECK_INTERVAL`: Monitoring interval in minutes (default: 1)
- `TIMEFRAME`: Candle timeframe (default: 5m)

## Error Handling

The bot includes error handling for:
- API connection issues
- Invalid RSI data
- Email delivery failures

## Deployment

You can deploy this bot to Railway, Render, Fly.io, or any always-on server for 24/7 operation. See the project documentation for deployment instructions.

## License

MIT License
