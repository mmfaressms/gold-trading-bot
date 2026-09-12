"""
💰 إدارة الأوامر والصفقات
Order and Trade Management Module
"""

import logging
from datetime import datetime
from config.settings import (
    STOP_LOSS, TAKE_PROFIT, RISK_REWARD_RATIO,
    MAX_OPEN_TRADES, MAX_DAILY_LOSS
)

logger = logging.getLogger(__name__)

class OrderManager:
    """إدارة الأوامر والصفقات"""
    
    def __init__(self, metatrader_api):
        self.api = metatrader_api
        self.open_trades = []
        self.daily_loss = 0.0
        self.trade_history = []
    
    def calculate_lot_size(self, account_balance, risk_percentage=1.0):
        """حساب حجم العقد بناءً على المخاطرة المسموحة"""
        try:
            # حساب المبلغ المسموح بخسارته
            risk_amount = account_balance * (risk_percentage / 100)
            
            # حساب عدد النقاط (Pips)
            pips = STOP_LOSS
            
            # حساب حجم العقد
            # الصيغة: حجم العقد = المبلغ المسموح / (عدد النقاط × قيمة النقطة)
            # بافتراض قيمة النقطة = 1 دولار لكل 0.1 عقد
            lot_size = risk_amount / (pips * 0.1)
            
            # تقريب إلى 0.01
            lot_size = round(lot_size, 2)
            
            logger.info(f"📊 حجم العقد المحسوب: {lot_size}")
            return lot_size
        
        except Exception as e:
            logger.error(f"❌ خطأ في حساب حجم العقد: {str(e)}")
            return 0.1
    
    def can_open_trade(self):
        """التحقق من إمكانية فتح صفقة جديدة"""
        # التحقق من عدد الصفقات المفتوحة
        open_positions = self.api.get_open_positions()
        if len(open_positions) >= MAX_OPEN_TRADES:
            logger.warning(f"⚠️ وصلنا للحد الأقصى من الصفقات: {MAX_OPEN_TRADES}")
            return False
        
        # التحقق من الخسائر اليومية
        if self.daily_loss >= MAX_DAILY_LOSS:
            logger.warning(f"⚠️ تجاوزنا الحد الأقصى من الخسائر اليومية: {MAX_DAILY_LOSS}")
            return False
        
        return True
    
    def open_buy_trade(self, volume, entry_price):
        """فتح صفقة شراء"""
        try:
            if not self.can_open_trade():
                logger.warning("❌ لا يمكن فتح صفقة جديدة حالياً")
                return None
            
            # حساب وقف الخسارة وجني الأرباح
            stop_loss = entry_price - STOP_LOSS * 0.01  # 50 نقطة
            take_profit = entry_price + (STOP_LOSS * RISK_REWARD_RATIO) * 0.01  # 100 نقطة
            
            # إرسال الأمر
            result = self.api.send_order(
                action='BUY',
                volume=volume,
                price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                comment="Auto BUY Order"
            )
            
            if result:
                trade = {
                    'ticket': result.order,
                    'type': 'BUY',
                    'volume': volume,
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'time_open': datetime.now(),
                }
                self.open_trades.append(trade)
                self.trade_history.append(trade)
                logger.info(f"✅ تم فتح صفقة شراء: Ticket {result.order}")
                return trade
            
            return None
        
        except Exception as e:
            logger.error(f"❌ خطأ في فتح صفقة شراء: {str(e)}")
            return None
    
    def open_sell_trade(self, volume, entry_price):
        """فتح صفقة بيع"""
        try:
            if not self.can_open_trade():
                logger.warning("❌ لا يمكن فتح صفقة جديدة حالياً")
                return None
            
            # حساب وقف الخسارة وجني الأرباح
            stop_loss = entry_price + STOP_LOSS * 0.01  # 50 نقطة
            take_profit = entry_price - (STOP_LOSS * RISK_REWARD_RATIO) * 0.01  # 100 نقطة
            
            # إرسال الأمر
            result = self.api.send_order(
                action='SELL',
                volume=volume,
                price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                comment="Auto SELL Order"
            )
            
            if result:
                trade = {
                    'ticket': result.order,
                    'type': 'SELL',
                    'volume': volume,
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'time_open': datetime.now(),
                }
                self.open_trades.append(trade)
                self.trade_history.append(trade)
                logger.info(f"✅ تم فتح صفقة بيع: Ticket {result.order}")
                return trade
            
            return None
        
        except Exception as e:
            logger.error(f"❌ خطأ في فتح صفقة بيع: {str(e)}")
            return None
    
    def close_trade(self, ticket):
        """إغلاق صفقة"""
        try:
            result = self.api.close_position(ticket)
            
            if result:
                # إزالة من الصفقات المفتوحة
                self.open_trades = [t for t in self.open_trades if t['ticket'] != ticket]
                logger.info(f"✅ تم إغلاق الصفقة: {ticket}")
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"❌ خطأ في إغلاق الصفقة: {str(e)}")
            return False
    
    def get_trade_statistics(self):
        """الحصول على إحصائيات الصفقات"""
        try:
            total_trades = len(self.trade_history)
            winning_trades = len([t for t in self.trade_history if t.get('profit', 0) > 0])
            losing_trades = len([t for t in self.trade_history if t.get('profit', 0) < 0])
            
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            total_profit = sum([t.get('profit', 0) for t in self.trade_history])
            
            return {
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': losing_trades,
                'win_rate': f"{win_rate:.2f}%",
                'total_profit': total_profit,
                'open_trades': len(self.open_trades),
            }
        
        except Exception as e:
            logger.error(f"❌ خطأ في حساب الإحصائيات: {str(e)}")
            return {}
