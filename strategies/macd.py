"""
استراتيجية MACD
MACD (Moving Average Convergence Divergence) Strategy
"""

import pandas as pd
import numpy as np
from config.settings import MACD_FAST, MACD_SLOW, MACD_SIGNAL

class MACDStrategy:
    """
    استراتيجية MACD
    - عندما يتقاطع MACD فوق Signal Line → إشارة شراء
    - عندما يتقاطع MACD تحت Signal Line → إشارة بيع
    """
    
    def __init__(self, fast=MACD_FAST, slow=MACD_SLOW, signal=MACD_SIGNAL):
        self.fast = fast
        self.slow = slow
        self.signal = signal
        self.name = "MACD"
    
    def calculate_macd(self, prices):
        """حساب MACD"""
        ema_fast = prices.ewm(span=self.fast, adjust=False).mean()
        ema_slow = prices.ewm(span=self.slow, adjust=False).mean()
        
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=self.signal, adjust=False).mean()
        histogram = macd - signal_line
        
        return macd, signal_line, histogram
    
    def generate_signal(self, prices):
        """
        توليد إشارات التداول
        Returns: {'signal': 'BUY'/'SELL'/'HOLD', 'confidence': 0.0-1.0}
        """
        if len(prices) < self.slow:
            return {'signal': 'HOLD', 'confidence': 0.0}
        
        macd, signal_line, histogram = self.calculate_macd(prices)
        
        # الحصول على آخر 3 قيم
        macd_last = macd.iloc[-3:].values
        signal_last = signal_line.iloc[-3:].values
        histogram_last = histogram.iloc[-3:].values
        
        # فحص التقاطع
        if macd_last[-1] > signal_last[-1] and macd_last[-2] <= signal_last[-2]:
            # تقاطع صعودي - إشارة شراء
            confidence = min(abs(histogram_last[-1]) / abs(prices.iloc[-1]) * 100, 1.0)
            return {'signal': 'BUY', 'confidence': max(confidence, 0.5)}
        
        elif macd_last[-1] < signal_last[-1] and macd_last[-2] >= signal_last[-2]:
            # تقاطع هابط - إشارة بيع
            confidence = min(abs(histogram_last[-1]) / abs(prices.iloc[-1]) * 100, 1.0)
            return {'signal': 'SELL', 'confidence': max(confidence, 0.5)}
        
        return {'signal': 'HOLD', 'confidence': 0.3}
    
    def get_status(self):
        """الحصول على حالة الاستراتيجية"""
        return {
            'name': self.name,
            'fast': self.fast,
            'slow': self.slow,
            'signal': self.signal,
        }
