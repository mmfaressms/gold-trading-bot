"""
🎯 نظام التداول الرئيسي
Main Trading Engine
"""

import logging
import pandas as pd
from trading.metatrader_api import MetaTraderAPI
from trading.order_manager import OrderManager
from strategies import (
    MovingAverageStrategy,
    RSIStrategy,
    MACDStrategy,
    BollingerBandsStrategy,
    StochasticStrategy,
    PatternRecognitionStrategy,
)
from config.settings import ENABLED_STRATEGIES
from alerts.telegram_bot import TelegramNotifier

logger = logging.getLogger(__name__)

class TradingEngine:
    """محرك التداول الرئيسي"""
    
    def __init__(self):
        self.api = MetaTraderAPI()
        self.order_manager = OrderManager(self.api)
        self.notifier = TelegramNotifier()
        
        # تهيئة الاستراتيجيات
        self.strategies = {}
        if ENABLED_STRATEGIES.get('moving_average'):
            self.strategies['MA'] = MovingAverageStrategy()
        if ENABLED_STRATEGIES.get('rsi'):
            self.strategies['RSI'] = RSIStrategy()
        if ENABLED_STRATEGIES.get('macd'):
            self.strategies['MACD'] = MACDStrategy()
        if ENABLED_STRATEGIES.get('bollinger_bands'):
            self.strategies['BB'] = BollingerBandsStrategy()
        if ENABLED_STRATEGIES.get('stochastic'):
            self.strategies['STOCH'] = StochasticStrategy()
        if ENABLED_STRATEGIES.get('pattern_recognition'):
            self.strategies['PATTERN'] = PatternRecognitionStrategy()
        
        logger.info(f"🚀 تم تهيئة محرك التداول مع {len(self.strategies)} استراتيجيات")
    
    def connect(self):
        """الاتصال بـ MetaTrader"""
        return self.api.connect()
    
    def disconnect(self):
        """قطع الاتصال"""
        return self.api.disconnect()
    
    def analyze_signals(self, prices):
        """تحليل الإشارات من جميع الاستراتيجيات"""
        signals = {}
        
        for name, strategy in self.strategies.items():
            try:
                signal = strategy.generate_signal(prices['close'])
                signals[name] = signal
                logger.info(f"🎯 {name}: {signal['signal']} (Confidence: {signal.get('confidence', 0):.2f})")
            except Exception as e:
                logger.error(f"❌ خطأ في استراتيجية {name}: {str(e)}")
                signals[name] = {'signal': 'HOLD', 'confidence': 0.0}
        
        return signals
    
    def aggregate_signals(self, signals):
        """دمج الإشارات من جميع الاستراتيجيات"""
        buy_count = sum(1 for s in signals.values() if s['signal'] == 'BUY')
        sell_count = sum(1 for s in signals.values() if s['signal'] == 'SELL')
        avg_confidence = sum(s['confidence'] for s in signals.values()) / len(signals) if signals else 0
        
        total_strategies = len(signals)
        buy_percentage = (buy_count / total_strategies * 100) if total_strategies > 0 else 0
        sell_percentage = (sell_count / total_strategies * 100) if total_strategies > 0 else 0
        
        # القرار النهائي
        if buy_percentage > 50:
            final_signal = 'BUY'
        elif sell_percentage > 50:
            final_signal = 'SELL'
        else:
            final_signal = 'HOLD'
        
        logger.info(f"""
        📊 تجميع الإشارات:
        - إشارات شراء: {buy_percentage:.1f}%
        - إشارات بيع: {sell_percentage:.1f}%
        - الثقة العامة: {avg_confidence:.2f}
        - القرار النهائي: {final_signal}
        """)
        
        return {
            'signal': final_signal,
            'buy_signals': buy_count,
            'sell_signals': sell_count,
            'confidence': avg_confidence,
            'buy_percentage': buy_percentage,
            'sell_percentage': sell_percentage,
        }
    
    def execute_trade(self, aggregated_signal, current_price, volume):
        """تنفيذ التداول"""
        signal = aggregated_signal['signal']
        confidence = aggregated_signal['confidence']
        
        if signal == 'BUY' and confidence > 0.65:
            logger.info(f"🟢 تنفيذ أمر شراء - السعر: {current_price}, الحجم: {volume}")
            trade = self.order_manager.open_buy_trade(volume, current_price)
            if trade:
                self.notifier.send_message_sync(f"✅ تم فتح صفقة شراء!\nالسعر: {current_price}\nالحجم: {volume}")
            return trade
        
        elif signal == 'SELL' and confidence > 0.65:
            logger.info(f"🔴 تنفيذ أمر بيع - السعر: {current_price}, الحجم: {volume}")
            trade = self.order_manager.open_sell_trade(volume, current_price)
            if trade:
                self.notifier.send_message_sync(f"✅ تم فتح صفقة بيع!\nالسعر: {current_price}\nالحجم: {volume}")
            return trade
        
        return None
    
    def run(self, volume=0.1, max_iterations=None):
        """تشغيل محرك التداول الرئيسي"""
        if not self.connect():
            logger.error("❌ فشل الاتصال بـ MetaTrader")
            return False
        
        try:
            iteration = 0
            while True:
                iteration += 1
                logger.info(f"\n{'='*60}")
                logger.info(f"🔄 التكرار #{iteration}")
                logger.info(f"{'='*60}")
                
                # الحصول على البيانات
                prices = self.api.get_prices(bars=100)
                if prices is None:
                    logger.error("❌ فشل الحصول على الأسعار")
                    continue
                
                # الحصول على السعر الحالي
                current_price = self.api.get_current_price()
                if current_price is None:
                    logger.error("❌ فشل الحصول على السعر الحالي")
                    continue
                
                logger.info(f"💱 السعر الحالي: {current_price['bid']}")
                
                # تحليل الإشارات
                signals = self.analyze_signals(prices)
                
                # دمج الإشارات
                aggregated = self.aggregate_signals(signals)
                
                # تنفيذ التداول
                self.execute_trade(aggregated, current_price['bid'], volume)
                
                # الحصول على معلومات الحساب
                account_info = self.api.get_account_info()
                if account_info:
                    logger.info(f"💰 الرصيد: {account_info['balance']}")
                    logger.info(f"📊 الإيكويتي: {account_info['equity']}")
                    logger.info(f"📈 الربح/الخسارة: {account_info['profit']}")
                
                if max_iterations and iteration >= max_iterations:
                    break
                
                # الانتظار قبل التكرار التالي
                import time
                time.sleep(60)  # انتظر دقيقة واحدة
        
        except KeyboardInterrupt:
            logger.info("⏸️ تم إيقاف البرنامج من قبل المستخدم")
        except Exception as e:
            logger.error(f"❌ خطأ في محرك التداول: {str(e)}")
        finally:
            self.disconnect()
