"""
🚀 البرنامج الرئيسي
Main Application Entry Point
"""

import logging
import sys
from datetime import datetime
from trading.engine import TradingEngine
from config.settings import LOG_FILE, LOG_LEVEL

# ============ إعداد السجلات ============
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def print_banner():
    """طباعة بافتتاحية البرنامج"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🏆 GOLD TRADING BOT - برنامج تداول الذهب          ║
║                                                              ║
║         Professional Algorithmic Gold Trading System         ║
║                  محرك تداول ذهب احترافي جداً                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    logger.info(f"\n{banner}")

def main():
    """
الدالة الرئيسية
    """
    print_banner()
    
    logger.info("="*60)
    logger.info(f"🕐 بدء التشغيل: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*60)
    
    try:
        # إنشاء محرك التداول
        logger.info("🔧 تهيئة محرك التداول...")
        engine = TradingEngine()
        
        # بدء التداول
        logger.info("\n🚀 بدء التداول...\n")
        engine.run(volume=0.1, max_iterations=None)
        
    except KeyboardInterrupt:
        logger.info("\n\n⏹️  تم إيقاف البرنامج من قبل المستخدم")
    except Exception as e:
        logger.error(f"❌ خطأ في البرنامج الرئيسي: {str(e)}", exc_info=True)
    finally:
        logger.info("="*60)
        logger.info(f"🛑 إيقاف البرنامج: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*60)

if __name__ == '__main__':
    main()
