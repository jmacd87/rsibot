# Bitcoin RSI Trading Bot

A Python-based trading bot that monitors Bitcoin's RSI (Relative Strength Index) on a 5-minute timeframe and sends WhatsApp alerts when the RSI reaches overbought (≥68) or oversold (≤32) conditions.

## Features

- Real-time Bitcoin/USD RSI monitoring
- 5-minute timeframe analysis
- WhatsApp alerts via Twilio
- Duplicate alert prevention
- Configurable RSI thresholds

## Prerequisites

- Python 3.7+
- Twilio account with WhatsApp integration
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
   - Open `config.py`
   - Update the following values:
     - `TWILIO_SID`: Your Twilio Account SID
     - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
     - `TWILIO_WHATSAPP_NUMBER`: Your Twilio WhatsApp number
     - `YOUR_WHATSAPP_NUMBER`: Your WhatsApp number
     - `HYPERLIQUID_API_URL`: Hyperliquid API endpoint

## Usage

Run the bot:
```bash
python rsi_bot.py
```

The bot will:
1. Start monitoring Bitcoin RSI every 5 minutes
2. Send WhatsApp alerts when RSI reaches overbought (≥68) or oversold (≤32) conditions
3. Prevent duplicate alerts for the same condition

## Configuration

You can modify the following parameters in `config.py`:
- `RSI_OVERBOUGHT`: Overbought threshold (default: 68)
- `RSI_OVERSOLD`: Oversold threshold (default: 32)
- `CHECK_INTERVAL`: Monitoring interval in minutes (default: 5)

## Error Handling

The bot includes error handling for:
- API connection issues
- Invalid RSI data
- WhatsApp message delivery failures

## License

MIT License
