"""
استراتيجية التعرف على الأنماط
Pattern Recognition Strategy
"""

import pandas as pd
import numpy as np

class PatternRecognitionStrategy:
    """
    استراتيجية التعرف على الأنماط الشهيرة:
    - Head and Shoulders
    - Double Bottom/Top
    - Triangle Patterns
    - Wedges
    """
    
    def __init__(self):
        self.name = "Pattern Recognition"
    
    def detect_double_bottom(self, prices, window=20):
        """الكشف عن نمط القاع المزدوج"""
        if len(prices) < window * 2:
            return False, 0.0
        
        recent = prices.iloc[-window:]
        min_price = recent.min()
        min_index = recent.idxmin()
        min_pos = len(recent) - (recent.index[-1] - min_index)
        
        # البحث عن قاع آخر
        if min_pos > 5:
            first_part = recent.iloc[:min_pos]
            if first_part.min() == min_price:
                return True, 0.7
        
        return False, 0.0
    
    def detect_double_top(self, prices, window=20):
        """الكشف عن نمط القمة المزدوجة"""
        if len(prices) < window * 2:
            return False, 0.0
        
        recent = prices.iloc[-window:]
        max_price = recent.max()
        max_index = recent.idxmax()
        max_pos = len(recent) - (recent.index[-1] - max_index)
        
        # البحث عن قمة أخرى
        if max_pos > 5:
            first_part = recent.iloc[:max_pos]
            if first_part.max() == max_price:
                return True, 0.7
        
        return False, 0.0
    
    def detect_triangle(self, prices, window=30):
        """الكشف عن نمط المثلث"""
        if len(prices) < window:
            return 'NONE', 0.0
        
        recent = prices.iloc[-window:]
        high_points = []
        low_points = []
        
        for i in range(1, len(recent) - 1):
            if recent.iloc[i] > recent.iloc[i-1] and recent.iloc[i] > recent.iloc[i+1]:
                high_points.append(recent.iloc[i])
            elif recent.iloc[i] < recent.iloc[i-1] and recent.iloc[i] < recent.iloc[i+1]:
                low_points.append(recent.iloc[i])
        
        # التحقق من تقارب القيم
        if len(high_points) >= 2 and len(low_points) >= 2:
            high_range = max(high_points) - min(high_points)
            low_range = max(low_points) - min(low_points)
            
            if high_range < recent.mean() * 0.02 and low_range < recent.mean() * 0.02:
                return 'TRIANGLE', 0.6
        
        return 'NONE', 0.0
    
    def generate_signal(self, prices):
        """
        توليد إشارات التداول
        Returns: {'signal': 'BUY'/'SELL'/'HOLD', 'confidence': 0.0-1.0, 'pattern': 'pattern_name'}
        """
        signal = 'HOLD'
        confidence = 0.0
        pattern = 'NONE'
        
        # فحص الأنماط
        double_bottom, db_confidence = self.detect_double_bottom(prices)
        if double_bottom:
            signal = 'BUY'
            confidence = db_confidence
            pattern = 'DOUBLE_BOTTOM'
        
        double_top, dt_confidence = self.detect_double_top(prices)
        if double_top:
            signal = 'SELL'
            confidence = dt_confidence
            pattern = 'DOUBLE_TOP'
        
        triangle_type, tri_confidence = self.detect_triangle(prices)
        if triangle_type != 'NONE':
            signal = 'WAIT'
            confidence = tri_confidence
            pattern = triangle_type
        
        return {'signal': signal, 'confidence': confidence, 'pattern': pattern}
    
    def get_status(self):
        """الحصول على حالة الاستراتيجية"""
        return {
            'name': self.name,
            'patterns': ['DOUBLE_BOTTOM', 'DOUBLE_TOP', 'TRIANGLE', 'HEAD_AND_SHOULDERS'],
        }
