"""
aستراتيجية المتوسطات المتحركة
Moving Average Strategy (MA)
"""

import pandas as pd
import numpy as np
from config.settings import MA_FAST, MA_SLOW, MA_TYPE

class MovingAverageStrategy:
    """
    استراتيجية تعتمد على المتوسطات المتحركة
    - عندما يتقاطع MA السريع فوق MA البطيء → إشارة شراء
    - عندما يتقاطع MA السريع تحت MA البطيء → إشارة بيع
    """
    
    def __init__(self, fast_period=MA_FAST, slow_period=MA_SLOW, ma_type=MA_TYPE):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.ma_type = ma_type
        self.name = "Moving Average"
    
    def calculate_ma(self, data, period, ma_type="EMA"):
        """حساب المتوسط المتحرك"""
        if ma_type == "EMA":
            return data.ewm(span=period, adjust=False).mean()
        else:  # SMA
            return data.rolling(window=period).mean()
    
    def generate_signal(self, prices):
        """
        توليد إشارات التداول
        Returns: {'signal': 'BUY'/'SELL'/'HOLD', 'confidence': 0.0-1.0}
        """
        if len(prices) < self.slow_period:
            return {'signal': 'HOLD', 'confidence': 0.0}
        
        # حساب المتوسطات
        ma_fast = self.calculate_ma(prices, self.fast_period, self.ma_type)
        ma_slow = self.calculate_ma(prices, self.slow_period, self.ma_type)
        
        # الحصول على آخر 3 قيم
        ma_fast_last = ma_fast.iloc[-3:].values
        ma_slow_last = ma_slow.iloc[-3:].values
        
        # فحص التقاطع
        if ma_fast_last[-1] > ma_slow_last[-1] and ma_fast_last[-2] <= ma_slow_last[-2]:
            # تقاطع صعودي - إشارة شراء
            confidence = min((ma_fast_last[-1] - ma_slow_last[-1]) / prices.iloc[-1] * 100, 1.0)
            return {'signal': 'BUY', 'confidence': max(confidence, 0.5)}
        
        elif ma_fast_last[-1] < ma_slow_last[-1] and ma_fast_last[-2] >= ma_slow_last[-2]:
            # تقاطع هابط - إشارة بيع
            confidence = min((ma_slow_last[-1] - ma_fast_last[-1]) / prices.iloc[-1] * 100, 1.0)
            return {'signal': 'SELL', 'confidence': max(confidence, 0.5)}
        
        # لا توجد إشارة واضحة
        return {'signal': 'HOLD', 'confidence': 0.3}
    
    def get_status(self):
        """الحصول على حالة الاستراتيجية"""
        return {
            'name': self.name,
            'fast_period': self.fast_period,
            'slow_period': self.slow_period,
            'ma_type': self.ma_type,
        }
