"""
🔔 نظام الإشعارات عبر Telegram
Telegram Notifications Module
"""

import logging
from telegram import Bot, error
import asyncio
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ENABLED

logger = logging.getLogger(__name__)

class TelegramNotifier:
    """نظام الإشعارات عبر Telegram"""
    
    def __init__(self):
        self.enabled = TELEGRAM_ENABLED and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
        self.bot = None
        
        if self.enabled:
            try:
                self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
                logger.info("✅ تم تهيئة Telegram Bot بنجاح")
            except Exception as e:
                logger.error(f"❌ فشل تهيئة Telegram Bot: {str(e)}")
                self.enabled = False
    
    async def send_message(self, message):
        """إرسال رسالة عبر Telegram"""
        if not self.enabled:
            logger.warning("⚠️ Telegram غير مفعل")
            return False
        
        try:
            await self.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
            logger.info(f"✅ تم إرسال الرسالة: {message[:50]}...")
            return True
        
        except error.TelegramError as e:
            logger.error(f"❌ خطأ في إرسال رسالة Telegram: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"❌ خطأ غير متوقع: {str(e)}")
            return False
    
    def send_message_sync(self, message):
        """إرسال رسالة بطريقة متزامنة (غير غير متزامنة)"""
        try:
            asyncio.run(self.send_message(message))
            return True
        except Exception as e:
            logger.error(f"❌ خطأ: {str(e)}")
            return False
    
    async def send_buy_signal(self, symbol, price, strategy, confidence):
        """إرسال إشارة شراء"""
        message = f"""
🟢 إشارة شراء قوية!

💱 العملة: {symbol}
📊 السعر: {price:.2f}
🎯 الاستراتيجية: {strategy}
📈 الثقة: {confidence*100:.1f}%
⏰ الوقت: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        await self.send_message(message)
    
    async def send_sell_signal(self, symbol, price, strategy, confidence):
        """إرسال إشارة بيع"""
        message = f"""
🔴 إشارة بيع قوية!

💱 العملة: {symbol}
📊 السعر: {price:.2f}
🎯 الاستراتيجية: {strategy}
📈 الثقة: {confidence*100:.1f}%
⏰ الوقت: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        await self.send_message(message)
    
    async def send_trade_opened(self, ticket, trade_type, volume, entry_price):
        """إشعار بفتح صفقة"""
        message = f"""
✅ تم فتح صفقة جديدة!

🎫 الرقم: {ticket}
📊 النوع: {trade_type}
📈 الحجم: {volume}
💰 سعر الدخول: {entry_price:.2f}
⏰ الوقت: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        await self.send_message(message)
    
    async def send_trade_closed(self, ticket, profit_loss, profit_percentage):
        """إشعار بإغلاق صفقة"""
        emoji = "✅" if profit_loss > 0 else "❌"
        message = f"""
{emoji} تم إغلاق صفقة!

🎫 الرقم: {ticket}
💰 الربح/الخسارة: {profit_loss:.2f} $
📊 النسبة: {profit_percentage:.2f}%
⏰ الوقت: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        await self.send_message(message)
    
    async def send_status_report(self, stats):
        """إرسال تقرير الحالة اليومي"""
        message = f"""
📊 تقرير يومي - Gold Trading Bot

📈 عدد الصفقات: {stats.get('total_trades', 0)}
✅ صفقات رابحة: {stats.get('winning_trades', 0)}
❌ صفقات خاسرة: {stats.get('losing_trades', 0)}
📊 نسبة الربح: {stats.get('win_rate', '0%')}
💰 إجمالي الربح: {stats.get('total_profit', 0):.2f} $
🔄 صفقات مفتوحة: {stats.get('open_trades', 0)}
⏰ التاريخ: {pd.Timestamp.now().strftime('%Y-%m-%d')}
        """
        await self.send_message(message)

import pandas as pd
