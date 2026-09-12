"""
استراتيجية المذبذب العشوائي
Stochastic Oscillator Strategy
"""

import pandas as pd
import numpy as np
from config.settings import STOCH_K_PERIOD, STOCH_D_PERIOD, STOCH_SMOOTH

class StochasticStrategy:
    """
    استراتيجية Stochastic
    - K > 80 أو D > 80 → مشبع بالشراء (بيع)
    - K < 20 أو D < 20 → مشبع بالبيع (شراء)
    """
    
    def __init__(self, k_period=STOCH_K_PERIOD, d_period=STOCH_D_PERIOD, smooth=STOCH_SMOOTH):
        self.k_period = k_period
        self.d_period = d_period
        self.smooth = smooth
        self.name = "Stochastic Oscillator"
    
    def calculate_stochastic(self, prices):
        """حساب مؤشر Stochastic"""
        lowest_low = prices.rolling(window=self.k_period).min()
        highest_high = prices.rolling(window=self.k_period).max()
        
        k_percent = 100 * ((prices - lowest_low) / (highest_high - lowest_low))
        k_percent_smooth = k_percent.rolling(window=self.smooth).mean()
        
        d_percent = k_percent_smooth.rolling(window=self.d_period).mean()
        
        return k_percent_smooth, d_percent
    
    def generate_signal(self, prices):
        """
        توليد إشارات التداول
        Returns: {'signal': 'BUY'/'SELL'/'HOLD', 'confidence': 0.0-1.0}
        """
        if len(prices) < self.k_period + self.d_period:
            return {'signal': 'HOLD', 'confidence': 0.0}
        
        k_percent, d_percent = self.calculate_stochastic(prices)
        
        k_value = k_percent.iloc[-1]
        d_value = d_percent.iloc[-1]
        
        # مشبع بالبيع - إشارة شراء
        if k_value < 20 and d_value < 20:
            confidence = (20 - min(k_value, d_value)) / 20
            return {'signal': 'BUY', 'confidence': max(confidence, 0.5)}
        
        # مشبع بالشراء - إشارة بيع
        elif k_value > 80 and d_value > 80:
            confidence = (min(k_value, d_value) - 80) / 20
            return {'signal': 'SELL', 'confidence': max(confidence, 0.5)}
        
        return {'signal': 'HOLD', 'confidence': 0.3}
    
    def get_status(self):
        """الحصول على حالة الاستراتيجية"""
        return {
            'name': self.name,
            'k_period': self.k_period,
            'd_period': self.d_period,
            'smooth': self.smooth,
        }
