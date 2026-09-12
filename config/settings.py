"""
⚙️ إعدادات برنامج تداول الذهب
Gold Trading Bot Configuration Settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============ 📱 إعدادات MetaTrader 5 ============
MT5_LOGIN = int(os.getenv("MT5_LOGIN", "0"))
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
MT5_SERVER = os.getenv("MT5_SERVER", "ICMarketsSC-Demo")
MT5_EXECUTABLE_PATH = os.getenv("MT5_EXECUTABLE_PATH", r"C:\Program Files\MetaTrader 5\terminal64.exe")

# ============ 🎯 إعدادات التداول ============
TRADING_SYMBOL = "XAUUSD"  # الذهب/الدولار
TIMEFRAME = "H1"            # الإطار الزمني: 1 ساعة
LOT_SIZE = 0.1              # حجم العقد
MIN_LOT_SIZE = 0.01
MAX_LOT_SIZE = 10.0

# ============ 💰 إدارة المخاطر ============
MAX_DRAWDOWN = 10.0         # أقصى خسارة مسموحة: 10%
MAX_DAILY_LOSS = 500        # أقصى خسارة يومية: 500 دولار
MAX_OPEN_TRADES = 5         # عدد الصفقات المفتوحة الأقصى

STOP_LOSS = 50              # وقف الخسارة: 50 نقطة
TAKE_PROFIT = 100           # جني الأرباح: 100 نقطة
RISK_REWARD_RATIO = 2.0     # نسبة المخاطرة/الربح: 1:2

# ============ 📊 الاستراتيجيات المفعلة ============
ENABLED_STRATEGIES = {
    "moving_average": True,
    "rsi": True,
    "macd": True,
    "bollinger_bands": True,
    "stochastic": True,
    "pattern_recognition": True,
    "machine_learning": True,
}

# Moving Average إعدادات
MA_FAST = 9
MA_SLOW = 21
MA_TYPE = "EMA"

# RSI إعدادات
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# MACD إعدادات
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Bollinger Bands إعدادات
BB_PERIOD = 20
BB_STDDEV = 2.0

# Stochastic إعدادات
STOCH_K_PERIOD = 14
STOCH_D_PERIOD = 3
STOCH_SMOOTH = 3

# ============ 🤖 إعدادات الذكاء الاصطناعي ============
ML_MODEL = "random_forest"
ML_ENABLED = True
ML_CONFIDENCE_THRESHOLD = 0.65
ML_UPDATE_FREQUENCY = 3600

# ============ 🔄 إعدادات Backtesting ============
BACKTEST_START_DATE = "2023-01-01"
BACKTEST_END_DATE = "2024-01-01"
BACKTEST_INITIAL_BALANCE = 10000.0
BACKTEST_COMMISSION = 0.001

# ============ 📈 لوحة التحكم ============
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")

# ============ 💾 قاعدة البيانات ============
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///gold_trading.db")

# ============ 🔔 الإشعارات ============
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_ENABLED = True

EMAIL_ENABLED = False
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

# ============ 🌡️ APIs الخارجية ============
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_ENABLED = True

# ============ 🕐 إعدادات التوقيت ============
TRADING_START_TIME = "00:00"
TRADING_END_TIME = "23:59"
TIMEZONE = "UTC"

# ============ 📝 السجلات ============
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "logs/trading_bot.log"
LOG_MAX_SIZE = 10485760
LOG_BACKUP_COUNT = 10

# ============ 🔍 إعدادات مراقبة الأداء ============
PERFORMANCE_MONITORING = True
METRICS_UPDATE_INTERVAL = 300
SAVE_METRICS_TO_DB = True
