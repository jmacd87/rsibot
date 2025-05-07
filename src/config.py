import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Email Configuration
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_RECIPIENT = os.environ.get('EMAIL_RECIPIENT')

# Hyperliquid API Configuration
HYPERLIQUID_API_URL = os.environ.get('HYPERLIQUID_API_URL', 'https://api.hyperliquid.xyz/info')
SYMBOL = os.environ.get('SYMBOL', 'BTC')
TIMEFRAME = os.environ.get('TIMEFRAME', '5m')

# RSI Thresholds
RSI_OVERBOUGHT = int(os.environ.get('RSI_OVERBOUGHT', 68))
RSI_OVERSOLD = int(os.environ.get('RSI_OVERSOLD', 32))

# Monitoring Interval (in minutes)
CHECK_INTERVAL = int(os.environ.get('CHECK_INTERVAL', 1)) 