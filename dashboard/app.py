"""
📊 لوحة التحكم الويب - Flask Dashboard
Web Dashboard Module
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime
from config.settings import (
    FLASK_HOST, FLASK_PORT, FLASK_DEBUG, SECRET_KEY, DATABASE_URL
)
from trading.engine import TradingEngine

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app)

# تهيئة محرك التداول
trading_engine = TradingEngine()

# ============ الإحصائيات العامة ============
stats = {
    'status': 'idle',
    'connected': False,
    'last_update': None,
    'total_trades': 0,
    'winning_trades': 0,
    'losing_trades': 0,
    'current_profit': 0,
}

@app.route('/')
def dashboard():
    """الصفحة الرئيسية"""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """الحصول على حالة البرنامج"""
    return jsonify({
        'status': stats['status'],
        'connected': stats['connected'],
        'last_update': stats['last_update'],
        'timestamp': datetime.now().isoformat(),
    })

@app.route('/api/account')
def get_account_info():
    """الحصول على معلومات الحساب"""
    try:
        account_info = trading_engine.api.get_account_info()
        if account_info:
            return jsonify({
                'success': True,
                'data': account_info,
            })
        return jsonify({'success': False, 'error': 'Failed to get account info'})
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/positions')
def get_positions():
    """الحصول على الصفقات المفتوحة"""
    try:
        positions = trading_engine.api.get_open_positions()
        return jsonify({
            'success': True,
            'data': positions,
            'count': len(positions),
        })
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/statistics')
def get_statistics():
    """الحصول على الإحصائيات"""
    try:
        stats_data = trading_engine.order_manager.get_trade_statistics()
        return jsonify({
            'success': True,
            'data': stats_data,
        })
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/start', methods=['POST'])
def start_trading():
    """بدء التداول"""
    try:
        stats['status'] = 'running'
        logger.info("✅ تم بدء التداول")
        return jsonify({'success': True, 'message': 'Trading started'})
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stop', methods=['POST'])
def stop_trading():
    """إيقاف التداول"""
    try:
        stats['status'] = 'idle'
        logger.info("⏹️ تم إيقاف التداول")
        return jsonify({'success': True, 'message': 'Trading stopped'})
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/price')
def get_current_price():
    """الحصول على السعر الحالي"""
    try:
        price = trading_engine.api.get_current_price()
        if price:
            return jsonify({
                'success': True,
                'data': price,
            })
        return jsonify({'success': False, 'error': 'Failed to get price'})
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/close-trade/<int:ticket>', methods=['POST'])
def close_trade(ticket):
    """إغلاق صفقة معينة"""
    try:
        result = trading_engine.api.close_position(ticket)
        if result:
            return jsonify({'success': True, 'message': f'Trade {ticket} closed'})
        return jsonify({'success': False, 'error': 'Failed to close trade'})
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/strategies')
def get_strategies():
    """الحصول على قائمة الاستراتيجيات المفعلة"""
    try:
        strategies = {
            name: strategy.get_status()
            for name, strategy in trading_engine.strategies.items()
        }
        return jsonify({
            'success': True,
            'data': strategies,
        })
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/settings')
def get_settings():
    """الحصول على الإعدادات"""
    try:
        from config import settings
        settings_data = {
            'trading_symbol': settings.TRADING_SYMBOL,
            'timeframe': settings.TIMEFRAME,
            'lot_size': settings.LOT_SIZE,
            'max_open_trades': settings.MAX_OPEN_TRADES,
            'stop_loss': settings.STOP_LOSS,
            'take_profit': settings.TAKE_PROFIT,
            'max_drawdown': settings.MAX_DRAWDOWN,
            'max_daily_loss': settings.MAX_DAILY_LOSS,
        }
        return jsonify({
            'success': True,
            'data': settings_data,
        })
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    logger.info(f"🚀 بدء لوحة التحكم على http://{FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
