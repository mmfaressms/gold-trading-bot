"""
استراتيجية مؤشر القوة النسبية
RSI (Relative Strength Index) Strategy
"""

import pandas as pd
import numpy as np
from config.settings import RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD

class RSIStrategy:
    """
    استراتيجية RSI
    - RSI > 70 → السوق مشبع بالشراء (بيع)
    - RSI < 30 → السوق مشبع بالبيع (شراء)
    - RSI بين 30-70 → محايد
    """
    
    def __init__(self, period=RSI_PERIOD, overbought=RSI_OVERBOUGHT, oversold=RSI_OVERSOLD):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        self.name = "RSI (Relative Strength Index)"
    
    def calculate_rsi(self, prices):
        """حساب مؤشر RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def generate_signal(self, prices):
        """
        توليد إشارات التداول
        Returns: {'signal': 'BUY'/'SELL'/'HOLD', 'confidence': 0.0-1.0, 'rsi_value': value}
        """
        if len(prices) < self.period:
            return {'signal': 'HOLD', 'confidence': 0.0, 'rsi_value': 0}
        
        rsi = self.calculate_rsi(prices)
        rsi_value = rsi.iloc[-1]
        
        # إشارة شراء عندما يكون RSI تحت 30 (مشبع ببيع)
        if rsi_value < self.oversold:
            confidence = (self.oversold - rsi_value) / self.oversold
            return {'signal': 'BUY', 'confidence': confidence, 'rsi_value': rsi_value}
        
        # إشارة بيع عندما يكون RSI فوق 70 (مشبع بشراء)
        elif rsi_value > self.overbought:
            confidence = (rsi_value - self.overbought) / (100 - self.overbought)
            return {'signal': 'SELL', 'confidence': confidence, 'rsi_value': rsi_value}
        
        # لا توجد إشارة واضحة
        return {'signal': 'HOLD', 'confidence': 0.2, 'rsi_value': rsi_value}
    
    def get_status(self):
        """الحصول على حالة الاستراتيجية"""
        return {
            'name': self.name,
            'period': self.period,
            'overbought': self.overbought,
            'oversold': self.oversold,
        }
