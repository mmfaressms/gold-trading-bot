"""
🏗️ هيكل مجلد التطبيق
Application Structure
"""

# gold-trading-bot/
# ├── config/                    # الإعدادات
# │   ├── __init__.py
# │   ├── settings.py             # الإعدادات الرئيسية
# │   └── credentials.example.json
# │
# ├── strategies/                 # الاستراتيجيات
# │   ├── __init__.py
# │   ├── moving_average.py       # استراتيجية MA
# │   ├── rsi.py                  # استراتيجية RSI
# │   ├── macd.py                 # استراتيجية MACD
# │   ├── bollinger_bands.py      # استراتيجية Bollinger Bands
# │   ├── stochastic.py           # استراتيجية Stochastic
# │   └── pattern_recognition.py  # استراتيجية Pattern Recognition
# │
# ├── trading/                    # محرك التداول
# │   ├── __init__.py
# │   ├── metatrader_api.py       # API MetaTrader 5
# │   ├── order_manager.py        # إدارة الأوامر
# │   └── engine.py               # محرك التداول الرئيسي
# │
# ├── analytics/                  # التحليلات
# │   ├── __init__.py
# │   ├── technical_analysis.py   # التحليل الفني
# │   ├── machine_learning.py     # الذكاء الاصطناعي
# │   └── backtesting.py          # اختبار الاستراتيجيات
# │
# ├── dashboard/                  # لوحة التحكم
# │   ├── app.py                  # تطبيق Flask
# │   ├── templates/              # صفحات HTML
# │   └── static/                 # الملفات الثابتة (CSS, JS)
# │
# ├── alerts/                     # نظام الإشعارات
# │   ├── __init__.py
# │   ├── telegram_bot.py         # إشعارات Telegram
# │   └── email_alerts.py         # إشعارات البريد
# │
# ├── database/                   # قاعدة البيانات
# │   ├── __init__.py
# │   ├── models.py               # نماذج قاعدة البيانات
# │   └── db.py                   # إدارة قاعدة البيانات
# │
# ├── logs/                       # السجلات
# │   └── trading_bot.log         # ملف السجل
# │
# ├── tests/                      # الاختبارات
# │   ├── __init__.py
# │   ├── test_strategies.py      # اختبار الاستراتيجيات
# │   └── test_trading.py         # اختبار التداول
# │
# ├── main.py                     # البرنامج الرئيسي
# ├── requirements.txt            # المكتبات المطلوبة
# ├── README.md                   # الدليل
# ├── .env.example               # متغيرات البيئة
# ├── .gitignore                 # ملف التجاهل
# └── LICENSE                    # الترخيص
