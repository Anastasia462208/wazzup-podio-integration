"""
Модуль настройки логирования для приложения
"""

import logging
import os
from datetime import datetime

def setup_logger(name: str, level: str = None) -> logging.Logger:
    """
    Настройка логгера для модуля
    
    Args:
        name: Имя логгера (обычно __name__)
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Настроенный логгер
    """
    
    # Определение уровня логирования
    if level is None:
        level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Создание логгера
    logger = logging.getLogger(name)
    
    # Если логгер уже настроен, возвращаем его
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, level, logging.INFO))
    
    # Создание форматтера
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level, logging.INFO))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Файловый обработчик (если указана директория для логов)
    log_dir = os.getenv('LOG_DIR', '')
    if log_dir and os.path.exists(log_dir):
        log_file = os.path.join(log_dir, f'wazzup_podio_{datetime.now().strftime("%Y%m%d")}.log')
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, level, logging.INFO))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
