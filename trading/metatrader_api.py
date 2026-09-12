"""
📱 نظام الاتصال بـ MetaTrader 5
MetaTrader 5 API Module
"""

import MetaTrader5 as mt5
import pandas as pd
import logging
from config.settings import (
    MT5_LOGIN, MT5_PASSWORD, MT5_SERVER, MT5_EXECUTABLE_PATH,
    TRADING_SYMBOL, TIMEFRAME
)

logger = logging.getLogger(__name__)

class MetaTraderAPI:
    """نظام الاتصال بـ MetaTrader 5"""
    
    def __init__(self):
        self.connected = False
        self.symbol = TRADING_SYMBOL
        self.timeframe = self._get_timeframe(TIMEFRAME)
    
    def _get_timeframe(self, tf_str):
        """تحويل رمز الإطار الزمني إلى رقم"""
        timeframes = {
            'M1': mt5.TIMEFRAME_M1,
            'M5': mt5.TIMEFRAME_M5,
            'M15': mt5.TIMEFRAME_M15,
            'M30': mt5.TIMEFRAME_M30,
            'H1': mt5.TIMEFRAME_H1,
            'H4': mt5.TIMEFRAME_H4,
            'D1': mt5.TIMEFRAME_D1,
            'W1': mt5.TIMEFRAME_W1,
            'MN1': mt5.TIMEFRAME_MN1,
        }
        return timeframes.get(tf_str, mt5.TIMEFRAME_H1)
    
    def connect(self):
        """الاتصال بـ MetaTrader 5"""
        try:
            if not mt5.initialize(path=MT5_EXECUTABLE_PATH):
                logger.error(f"❌ فشل تهيئة MetaTrader 5: {mt5.last_error()}")
                return False
            
            # محاولة تسجيل الدخول
            if MT5_LOGIN and MT5_PASSWORD:
                login_result = mt5.login(MT5_LOGIN, MT5_PASSWORD, MT5_SERVER)
                if not login_result:
                    logger.error(f"❌ فشل تسجيل الدخول: {mt5.last_error()}")
                    return False
            
            self.connected = True
            logger.info("✅ تم الاتصال بـ MetaTrader 5 بنجاح")
            return True
        
        except Exception as e:
            logger.error(f"❌ خطأ في الاتصال: {str(e)}")
            return False
    
    def disconnect(self):
        """قطع الاتصال بـ MetaTrader 5"""
        try:
            mt5.shutdown()
            self.connected = False
            logger.info("✅ تم قطع الاتصال")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في قطع الاتصال: {str(e)}")
            return False
    
    def get_prices(self, bars=100):
        """الحصول على أسعار العملة"""
        try:
            if not self.connected:
                logger.warning("⚠️ غير متصل بـ MetaTrader")
                return None
            
            # الحصول على البيانات التاريخية
            rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, bars)
            
            if rates is None:
                logger.error(f"❌ فشل الحصول على الأسعار: {mt5.last_error()}")
                return None
            
            # تحويل إلى DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            
            return df
        
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على الأسعار: {str(e)}")
            return None
    
    def get_current_price(self):
        """الحصول على السعر الحالي"""
        try:
            if not self.connected:
                return None
            
            tick = mt5.symbol_info_tick(self.symbol)
            if tick is None:
                logger.error(f"❌ فشل الحصول على السعر الحالي: {mt5.last_error()}")
                return None
            
            return {
                'bid': tick.bid,
                'ask': tick.ask,
                'last': tick.last,
                'time': tick.time
            }
        
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على السعر: {str(e)}")
            return None
    
    def get_account_info(self):
        """الحصول على معلومات الحساب"""
        try:
            if not self.connected:
                return None
            
            account = mt5.account_info()
            if account is None:
                logger.error(f"❌ فشل الحصول على معلومات الحساب: {mt5.last_error()}")
                return None
            
            return {
                'balance': account.balance,
                'equity': account.equity,
                'profit': account.profit,
                'margin': account.margin,
                'margin_free': account.margin_free,
                'margin_level': account.margin_level,
                'leverage': account.leverage,
                'currency': account.currency,
            }
        
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على معلومات الحساب: {str(e)}")
            return None
    
    def get_open_positions(self):
        """الحصول على الصفقات المفتوحة"""
        try:
            if not self.connected:
                return []
            
            positions = mt5.positions_get(symbol=self.symbol)
            if positions is None:
                return []
            
            return [
                {
                    'ticket': pos.ticket,
                    'symbol': pos.symbol,
                    'type': 'BUY' if pos.type == 0 else 'SELL',
                    'volume': pos.volume,
                    'price_open': pos.price_open,
                    'price_current': pos.price_current,
                    'profit': pos.profit,
                    'time_open': pos.time,
                }
                for pos in positions
            ]
        
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على الصفقات: {str(e)}")
            return []
    
    def send_order(self, action, volume, price=None, stop_loss=None, take_profit=None, comment=""):
        """إرسال أمر تداول"""
        try:
            if not self.connected:
                logger.error("❌ غير متصل بـ MetaTrader")
                return None
            
            # تحديد نوع الأمر
            if action == 'BUY':
                order_type = mt5.ORDER_TYPE_BUY
            elif action == 'SELL':
                order_type = mt5.ORDER_TYPE_SELL
            else:
                logger.error(f"❌ نوع أمر غير صحيح: {action}")
                return None
            
            # الحصول على السعر الحالي
            tick = mt5.symbol_info_tick(self.symbol)
            if tick is None:
                logger.error("❌ فشل الحصول على السعر الحالي")
                return None
            
            price = tick.ask if action == 'BUY' else tick.bid
            
            # إنشاء طلب الأمر
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": volume,
                "type": order_type,
                "price": price,
                "sl": stop_loss if stop_loss else 0,
                "tp": take_profit if take_profit else 0,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # إرسال الأمر
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"❌ فشل إرسال الأمر: {result.comment}")
                return None
            
            logger.info(f"✅ تم إرسال أمر {action} بنجاح - Ticket: {result.order}")
            return result
        
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال الأمر: {str(e)}")
            return None
    
    def close_position(self, ticket, volume=None):
        """إغلاق صفقة"""
        try:
            if not self.connected:
                logger.error("❌ غير متصل بـ MetaTrader")
                return None
            
            # الحصول على معلومات الصفقة
            position = mt5.positions_get(ticket=ticket)
            if not position:
                logger.error(f"❌ لم تجد الصفقة: {ticket}")
                return None
            
            pos = position[0]
            volume = volume if volume else pos.volume
            
            # تحديد نوع الأمر المعاكس
            order_type = mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY
            
            # الحصول على السعر الحالي
            tick = mt5.symbol_info_tick(self.symbol)
            if tick is None:
                logger.error("❌ فشل الحصول على السعر الحالي")
                return None
            
            price = tick.bid if order_type == mt5.ORDER_TYPE_SELL else tick.ask
            
            # إنشاء طلب الإغلاق
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": volume,
                "type": order_type,
                "price": price,
                "position": ticket,
                "comment": "Close position",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # إرسال أمر الإغلاق
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"❌ فشل إغلاق الصفقة: {result.comment}")
                return None
            
            logger.info(f"✅ تم إغلاق الصفقة {ticket} بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"❌ خطأ في إغلاق الصفقة: {str(e)}")
            return None
    
    def get_status(self):
        """الحصول على حالة الاتصال"""
        return {
            'connected': self.connected,
            'symbol': self.symbol,
            'timeframe': TIMEFRAME,
            'last_check': pd.Timestamp.now().isoformat(),
        }
