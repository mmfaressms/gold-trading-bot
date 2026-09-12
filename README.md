# 🏆 Gold Trading Bot - برنامج تداول الذهب الاحترافي

**برنامج تداول ذهب احترافي جداً** مع أفضل الاستراتيجيات والميزات المتقدمة!

## ✨ الميزات الرئيسية

### 📊 الاستراتيجيات المتقدمة
- ✅ **Moving Averages (MA)** - المتوسطات المتحركة
- ✅ **RSI (Relative Strength Index)** - مؤشر القوة النسبية
- ✅ **MACD** - تقارب وتباعد المتوسطات المتحركة
- ✅ **Bollinger Bands** - فرقات بولينجر
- ✅ **Stochastic Oscillator** - المذبذب العشوائي
- ✅ **Pattern Recognition** - التعرف على الأنماط
- ✅ **Machine Learning/AI** - الذكاء الاصطناعي

### 🎯 الميزات الإضافية
- 📈 **Real-time Trading** - التداول الفوري
- 🔔 **Real-time Alerts** - إشعارات فورية
- 📊 **Advanced Dashboard** - لوحة تحكم متقدمة
- 💾 **Trade History** - سجل الصفقات الكامل
- 📉 **Analytics & Statistics** - إحصائيات متقدمة
- 🛡️ **Risk Management** - إدارة المخاطر (Stop Loss, Take Profit)
- 🔄 **Backtesting** - اختبار الاستراتيجيات
- 🌡️ **Weather Impact Analysis** - تحليل تأثير الطقس
- 💰 **Portfolio Management** - إدارة المحفظة

### 🔌 التكنولوجيا المستخدمة
- **Python 3.9+**
- **MetaTrader 5 API**
- **Flask** - لوحة التحكم
- **pandas & numpy** - معالجة البيانات
- **scikit-learn** - الذكاء الاصطناعي
- **matplotlib & plotly** - الرسوم البيانية
- **SQLite/PostgreSQL** - قاعدة البيانات
- **Telegram Bot** - الإشعارات

---

## 📁 هيكل المشروع

```
gold-trading-bot/
├── config/                 # الإعدادات
│   ├── settings.py
│   └── credentials.json
├── strategies/            # الاستراتيجيات
│   ├── moving_average.py
│   ├── rsi.py
│   ├── macd.py
│   ├── bollinger_bands.py
│   ├── stochastic.py
│   └── pattern_recognition.py
├── trading/              # محرك التداول
│   ├── metatrader_api.py
│   ├── order_manager.py
│   └── portfolio.py
├── analytics/            # التحليلات
│   ├── technical_analysis.py
│   ├── machine_learning.py
│   └── backtesting.py
├── dashboard/            # لوحة التحكم
│   ├── app.py
│   ├── templates/
│   └── static/
├── alerts/              # نظام الإشعارات
│   ├── telegram_bot.py
│   └── email_alerts.py
├── database/            # قاعدة البيانات
│   ├── models.py
│   └── db.py
├── tests/               # الاختبارات
├── requirements.txt     # المكتبات المطلوبة
└── main.py             # البرنامج الرئيسي
```

---

## 🚀 البدء السريع

### 1️⃣ التثبيت
```bash
git clone https://github.com/mmfaressms/gold-trading-bot.git
cd gold-trading-bot
pip install -r requirements.txt
```

### 2️⃣ الإعدادات
```bash
# انسخ ملف الإعدادات
cp config/credentials.example.json config/credentials.json

# أضف مفاتيح API الخاصة بك
# - MetaTrader 5 API Key
# - Telegram Bot Token
# - Weather API Key
```

### 3️⃣ التشغيل
```bash
python main.py
```

### 4️⃣ الوصول للوحة التحكم
```
http://localhost:5000
```

---

## 📖 الوثائق

- [دليل الاستراتيجيات](docs/STRATEGIES.md)
- [دليل API](docs/API.md)
- [دليل التثبيت](docs/INSTALLATION.md)
- [دليل المستخدم](docs/USER_GUIDE.md)

---

## ⚙️ الإعدادات الأساسية

```python
# config/settings.py
TRADING_SYMBOL = "XAUUSD"  # الذهب/الدولار
TIMEFRAME = "H1"            # الإطار الزمني: 1 ساعة
LOT_SIZE = 0.1              # حجم العقد
MAX_DRAWDOWN = 10           # أقصى خسارة: 10%
STOP_LOSS = 50              # وقف الخسارة: 50 نقطة
TAKE_PROFIT = 100           # جني الأرباح: 100 نقطة
```

---

## 📊 لوحة التحكم

**الميزات:**
- 📈 الرسوم البيانية الفورية
- 🎯 عرض الصفقات الفعالة
- 📉 إحصائيات الأرباح والخسائر
- 🔔 الإشعارات الفورية
- 🛡️ إدارة المخاطر
- 💾 سجل الصفقات الكامل

---

## 🔔 الإشعارات

البرنامج يرسل إشعارات عبر:
- 📱 **Telegram Bot** - إشعارات فورية
- 📧 **البريد الإلكتروني** - تقارير يومية
- 🔊 **التنبيهات الصوتية** - نبهات فورية

---

## 🧪 Backtesting

اختبر الاستراتيجيات على بيانات تاريخية:

```bash
python analytics/backtesting.py --strategy=ma --start=2023-01-01 --end=2024-01-01
```

---

## 🤖 الذكاء الاصطناعي

البرنامج يستخدم **Machine Learning** لـ:
- التنبؤ بأسعار الذهب
- اكتشاف الأنماط المتقدمة
- تحسين الاستراتيجيات تلقائياً
- تحديد أفضل أوقات الدخول والخروج

---

## 📜 الترخيص

MIT License - استخدم بحرية!

---

## 👨‍💻 المساهمة

نرحب بمساهماتك! 🙌

---

## ⚠️ تحذير مهم

⚠️ **هذا البرنامج لأغراض تعليمية فقط!**
- **لا تستثمر أموالاً حقيقية** بدون اختبار شامل
- **جرب على حساب Demo أولاً**
- **المخاطر موجودة دائماً في التداول**
- **استشر مستشاراً مالياً قبل التداول**

---

## 📞 التواصل

- 📧 البريد: your.email@example.com
- 🐦 تويتر: @YourTwitter
- 💬 تيليجرام: @YourTelegram

---

**شكراً لاستخدامك Gold Trading Bot! 🙏**

**Happy Trading! 📈💰**
