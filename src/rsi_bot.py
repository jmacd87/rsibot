import requests
import time
import schedule
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import (
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    EMAIL_RECIPIENT,
    HYPERLIQUID_API_URL,
    SYMBOL,
    TIMEFRAME,
    RSI_OVERBOUGHT,
    RSI_OVERSOLD,
    CHECK_INTERVAL
)
import pandas as pd
import numpy as np
import threading
from fastapi import FastAPI
import uvicorn

class RSIBot:
    def __init__(self):
        self.last_alert = None  # To prevent duplicate alerts
        self.oversold_alert_sent = False
        self.overbought_alert_sent = False

    def calculate_rsi(self, prices, period=14):
        """Calculate RSI from price data"""
        if len(prices) < period + 1:
            return None

        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [max(delta, 0) for delta in deltas]
        losses = [abs(min(delta, 0)) for delta in deltas]

        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period

        if avg_loss == 0:
            rs = 0
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        # Wilder's smoothing for the rest
        for i in range(period, len(gains)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
        return rsi

    def rsi_tradingview(self, closes, period=14, round_rsi=True):
        """Implements the RSI indicator as defined by TradingView using pandas and numpy."""
        ohlc = pd.DataFrame({'close': closes})
        delta = ohlc["close"].diff()

        up = delta.copy()
        up[up < 0] = 0
        up = pd.Series.ewm(up, alpha=1/period).mean()

        down = delta.copy()
        down[down > 0] = 0
        down *= -1
        down = pd.Series.ewm(down, alpha=1/period).mean()

        rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))
        return np.round(rsi, 2) if round_rsi else rsi

    def get_rsi(self):
        """Fetch price data and calculate RSI using 500 candles for high accuracy (matches TradingView/exchange)."""
        try:
            now = int(time.time())
            interval_sec = 5 * 60  # 5 minutes in seconds
            num_candles = 500
            # Align to the next candle boundary to include the current forming candle
            next_candle_end = ((now // interval_sec) + 1) * interval_sec * 1000  # ms
            start_time = next_candle_end - num_candles * interval_sec * 1000
            end_time = next_candle_end

            payload = {
                "type": "candleSnapshot",
                "req": {
                    "coin": SYMBOL,
                    "interval": TIMEFRAME,
                    "startTime": start_time,
                    "endTime": end_time
                }
            }

            response = requests.post(
                HYPERLIQUID_API_URL,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            data = response.json()

            if not data or len(data) < 15:
                print(f"No or insufficient candlestick data received. Got {len(data) if data else 0} candles.")
                return None

            # Use all candles, including the current (possibly forming) candle
            prices = [float(candle['c']) for candle in data]
            times = [candle['t'] for candle in data] if 't' in data[0] else None


            # Calculate TradingView-style RSI for the entire series, use the last value
            rsi_series = self.rsi_tradingview(prices)
            rsi = rsi_series[-1] if len(rsi_series) > 0 else None
            print(f"Current RSI: {rsi}" if rsi is not None else "RSI could not be calculated.")
            return rsi

        except Exception as e:
            print(f"Error fetching RSI data: {e}")
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.content}")
            return None

    def send_email_alert(self, message):
        """Send email alert using Gmail SMTP"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = EMAIL_SENDER
            msg['To'] = EMAIL_RECIPIENT
            msg['Subject'] = f"Bitcoin RSI Alert - {time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Add message body
            msg.attach(MIMEText(message, 'plain'))
            
            # Create SMTP session
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)
            
            print(f"Alert sent: {message}")
        except Exception as e:
            print(f"Error sending email alert: {e}")

    def check_rsi(self):
        """Check RSI levels and send alerts if conditions are met"""
        rsi = self.get_rsi()
        if rsi is None:
            return

        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        message = None

        # Overbought logic
        if rsi >= RSI_OVERBOUGHT:
            if not self.overbought_alert_sent:
                message = f"""
🚨 BITCOIN RSI ALERT - OVERBOUGHT 🚨

Current RSI: {rsi}
Time: {current_time}
Status: Overbought (Above {RSI_OVERBOUGHT})

This indicates potential selling pressure and a possible price reversal.
"""
                self.overbought_alert_sent = True
                self.oversold_alert_sent = False
        else:
            self.overbought_alert_sent = False

        # Oversold logic
        if rsi <= RSI_OVERSOLD:
            if not self.oversold_alert_sent:
                message = f"""
🚨 BITCOIN RSI ALERT - OVERSOLD 🚨

Current RSI: {rsi}
Time: {current_time}
Status: Oversold (Below {RSI_OVERSOLD})

This indicates potential buying pressure and a possible price reversal.
"""
                self.oversold_alert_sent = True
                self.overbought_alert_sent = False
        else:
            self.oversold_alert_sent = False

        # Send alert if conditions are met
        if message:
            self.send_email_alert(message)
            self.last_alert = message

def run_bot():
    bot = RSIBot()
    print(f"Starting RSI Bot - Monitoring {SYMBOL} on {TIMEFRAME} timeframe")
    print(f"RSI Thresholds - Overbought: {RSI_OVERBOUGHT}, Oversold: {RSI_OVERSOLD}")
    schedule.every(CHECK_INTERVAL).minutes.do(bot.check_rsi)
    bot.check_rsi()
    while True:
        schedule.run_pending()
        time.sleep(1)

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "RSI bot is running"}

# Start the bot in a non-daemon background thread at module level
bot_thread = threading.Thread(target=run_bot)
bot_thread.start() 