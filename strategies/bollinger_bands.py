"""
استراتيجية فرقات بولينجر
Bollinger Bands Strategy
"""

import pandas as pd
import numpy as np
from config.settings import BB_PERIOD, BB_STDDEV

class BollingerBandsStrategy:
    """
    استراتيجية Bollinger Bands
    - السعر يلامس الحد الأسفل → إشارة شراء
    - السعر يلامس الحد الأعلى → إشارة بيع
    """
    
    def __init__(self, period=BB_PERIOD, std_dev=BB_STDDEV):
        self.period = period
        self.std_dev = std_dev
        self.name = "Bollinger Bands"
    
    def calculate_bollinger_bands(self, prices):
        """حساب فرقات بولينجر"""
        middle_band = prices.rolling(window=self.period).mean()
        std = prices.rolling(window=self.period).std()
        
        upper_band = middle_band + (std * self.std_dev)
        lower_band = middle_band - (std * self.std_dev)
        
        return upper_band, middle_band, lower_band
    
    def generate_signal(self, prices):
        """
        توليد إشارات التداول
        Returns: {'signal': 'BUY'/'SELL'/'HOLD', 'confidence': 0.0-1.0}
        """
        if len(prices) < self.period:
            return {'signal': 'HOLD', 'confidence': 0.0}
        
        upper_band, middle_band, lower_band = self.calculate_bollinger_bands(prices)
        
        current_price = prices.iloc[-1]
        upper = upper_band.iloc[-1]
        lower = lower_band.iloc[-1]
        middle = middle_band.iloc[-1]
        
        # السعر قريب من الحد الأسفل - إشارة شراء
        if current_price <= lower * 1.02:
            confidence = 1 - ((current_price - lower) / (middle - lower))
            return {'signal': 'BUY', 'confidence': max(min(confidence, 1.0), 0.5)}
        
        # السعر قريب من الحد الأعلى - إشارة بيع
        elif current_price >= upper * 0.98:
            confidence = 1 - ((upper - current_price) / (upper - middle))
            return {'signal': 'SELL', 'confidence': max(min(confidence, 1.0), 0.5)}
        
        return {'signal': 'HOLD', 'confidence': 0.3}
    
    def get_status(self):
        """الحصول على حالة الاستراتيجية"""
        return {
            'name': self.name,
            'period': self.period,
            'std_dev': self.std_dev,
        }
