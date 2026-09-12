"""
📈 نظام Backtesting - اختبار الاستراتيجيات
Backtesting Module
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from strategies import (
    MovingAverageStrategy,
    RSIStrategy,
    MACDStrategy,
    BollingerBandsStrategy,
    StochasticStrategy,
)

logger = logging.getLogger(__name__)

class Backtester:
    """
نظام اختبار الاستراتيجيات على بيانات تاريخية
    """
    
    def __init__(self, initial_balance=10000, commission=0.001):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.commission = commission
        self.trades = []
        self.equity_curve = [initial_balance]
        
        # تهيئة الاستراتيجيات
        self.strategies = {
            'MA': MovingAverageStrategy(),
            'RSI': RSIStrategy(),
            'MACD': MACDStrategy(),
            'BB': BollingerBandsStrategy(),
            'STOCH': StochasticStrategy(),
        }
    
    def backtest_strategy(self, data, strategy_name='MA', entry_stop_loss=50, entry_take_profit=100):
        """
تشغيل الاختبار على بيانات تاريخية
        """
        logger.info(f"\n🧪 بدء الاختبار: {strategy_name}")
        logger.info(f"   البيانات: {len(data)} شمعة")
        logger.info(f"   الرصيد الأولي: {self.initial_balance}")
        
        strategy = self.strategies.get(strategy_name)
        if not strategy:
            logger.error(f"❌ استراتيجية غير موجودة: {strategy_name}")
            return None
        
        trades_count = 0
        winning_trades = 0
        losing_trades = 0
        total_profit = 0
        
        for i in range(100, len(data)):  # البدء من 100 لوجود بيانات كافية
            prices = data['close'].iloc[:i]
            
            # الحصول على الإشارة
            signal = strategy.generate_signal(prices)
            
            if signal['signal'] == 'BUY':
                # حساب نقطة الدخول والخروج
                entry_price = data['close'].iloc[i]
                stop_loss = entry_price - (entry_stop_loss * 0.01)
                take_profit = entry_price + (entry_take_profit * 0.01)
                
                # البحث عن الخروج
                for j in range(i+1, min(i+100, len(data))):
                    price = data['close'].iloc[j]
                    
                    if price <= stop_loss:
                        # خسارة
                        profit = (stop_loss - entry_price) * 100  # حجم العقد 0.1
                        profit_pct = (stop_loss / entry_price - 1) * 100
                        losing_trades += 1
                        break
                    elif price >= take_profit:
                        # ربح
                        profit = (take_profit - entry_price) * 100
                        profit_pct = (take_profit / entry_price - 1) * 100
                        winning_trades += 1
                        break
                else:
                    # لم يتم الخروج
                    profit = (data['close'].iloc[-1] - entry_price) * 100
                    profit_pct = (data['close'].iloc[-1] / entry_price - 1) * 100
                    if profit > 0:
                        winning_trades += 1
                    else:
                        losing_trades += 1
                
                # تطبيق العمولة
                profit -= abs(profit) * self.commission
                
                # تحديث الرصيد
                self.current_balance += profit
                total_profit += profit
                trades_count += 1
                
                # تسجيل الصفقة
                self.trades.append({
                    'index': i,
                    'entry_price': entry_price,
                    'exit_price': stop_loss if profit < 0 else take_profit,
                    'profit': profit,
                    'profit_pct': profit_pct,
                    'type': 'BUY',
                })
                
                self.equity_curve.append(self.current_balance)
            
            elif signal['signal'] == 'SELL':
                # حساب نقطة الدخول والخروج
                entry_price = data['close'].iloc[i]
                stop_loss = entry_price + (entry_stop_loss * 0.01)
                take_profit = entry_price - (entry_take_profit * 0.01)
                
                # البحث عن الخروج
                for j in range(i+1, min(i+100, len(data))):
                    price = data['close'].iloc[j]
                    
                    if price >= stop_loss:
                        # خسارة
                        profit = (entry_price - stop_loss) * 100
                        profit_pct = (1 - stop_loss / entry_price) * 100
                        losing_trades += 1
                        break
                    elif price <= take_profit:
                        # ربح
                        profit = (entry_price - take_profit) * 100
                        profit_pct = (1 - take_profit / entry_price) * 100
                        winning_trades += 1
                        break
                else:
                    # لم يتم الخروج
                    profit = (entry_price - data['close'].iloc[-1]) * 100
                    profit_pct = (1 - data['close'].iloc[-1] / entry_price) * 100
                    if profit > 0:
                        winning_trades += 1
                    else:
                        losing_trades += 1
                
                # تطبيق العمولة
                profit -= abs(profit) * self.commission
                
                # تحديث الرصيد
                self.current_balance += profit
                total_profit += profit
                trades_count += 1
                
                # تسجيل الصفقة
                self.trades.append({
                    'index': i,
                    'entry_price': entry_price,
                    'exit_price': stop_loss if profit < 0 else take_profit,
                    'profit': profit,
                    'profit_pct': profit_pct,
                    'type': 'SELL',
                })
                
                self.equity_curve.append(self.current_balance)
        
        # حساب الإحصائيات
        stats = {
            'strategy': strategy_name,
            'total_trades': trades_count,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': f"{(winning_trades/trades_count*100):.2f}%" if trades_count > 0 else "0%",
            'total_profit': f"{total_profit:.2f}",
            'profit_factor': f"{(total_profit/abs(total_profit-total_profit) if total_profit != 0 else 1):.2f}",
            'final_balance': f"{self.current_balance:.2f}",
            'roi': f"{((self.current_balance/self.initial_balance - 1) * 100):.2f}%",
            'max_drawdown': self._calculate_max_drawdown(),
        }
        
        logger.info(f"\n📊 نتائج الاختبار: {strategy_name}")
        logger.info(f"   {'='*50}")
        for key, value in stats.items():
            logger.info(f"   {key}: {value}")
        logger.info(f"   {'='*50}\n")
        
        return stats
    
    def _calculate_max_drawdown(self):
        """
حساب الحد الأقصى للانخفاض
        """
        equity = np.array(self.equity_curve)
        running_max = np.maximum.accumulate(equity)
        drawdown = (equity - running_max) / running_max
        max_drawdown = np.min(drawdown)
        return f"{max_drawdown*100:.2f}%"

if __name__ == '__main__':
    # مثال على الاستخدام
    logger.info("🧪 بدء نظام الاختبار...")
    
    # إنشاء بيانات تجريبية
    dates = pd.date_range(start='2023-01-01', periods=500, freq='H')
    prices = 2000 + np.cumsum(np.random.randn(500) * 5)
    data = pd.DataFrame({
        'time': dates,
        'close': prices,
    })
    
    # تشغيل الاختبار
    backtester = Backtester()
    for strategy in ['MA', 'RSI', 'MACD', 'BB', 'STOCH']:
        backtester.backtest_strategy(data, strategy_name=strategy)
