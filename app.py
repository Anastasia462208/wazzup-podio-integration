#!/usr/bin/env python3
"""
Wazzup-Podio Integration Webhook Server
Основное Flask приложение для обработки вебхуков от Wazzup и передачи данных в Podio
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from src.wazzup.webhook_handler import WazzupWebhookHandler
from src.podio.client import PodioClient
from src.utils.logger import setup_logger

# Загрузка переменных окружения
load_dotenv()

# Настройка приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

# Настройка логирования
logger = setup_logger(__name__)

# Инициализация клиентов
podio_client = PodioClient()
webhook_handler = WazzupWebhookHandler()

@app.route('/', methods=['GET'])
def health_check():
    """Проверка работоспособности сервиса"""
    return jsonify({
        'status': 'active',
        'service': 'Wazzup-Podio Integration',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/webhook/wazzup', methods=['POST'])
def wazzup_webhook():
    """
    Обработчик вебхуков от Wazzup
    Принимает сообщения и передает их в Podio
    """
    try:
        # Получение данных из запроса
        data = request.get_json()
        
        if not data:
            logger.warning("Получен пустой запрос")
            return jsonify({'error': 'No data provided'}), 400
        
        logger.info(f"Получен вебхук от Wazzup: {json.dumps(data, ensure_ascii=False)}")
        
        # Валидация вебхука
        if not webhook_handler.validate_webhook(request):
            logger.error("Ошибка валидации вебхука")
            return jsonify({'error': 'Invalid webhook'}), 401
        
        # Обработка вебхука
        processed_items = webhook_handler.process_webhook(data)
        
        if processed_items:
            results = []
            for item in processed_items:
                # Отправка в Podio
                result = podio_client.create_message_item(item)
                
                if result:
                    logger.info(f"Элемент успешно отправлен в Podio: {result}")
                    results.append(result)
                else:
                    logger.error("Ошибка отправки элемента в Podio")
            
            if results:
                return jsonify({
                    'status': 'success',
                    'message': f'Processed {len(results)} items and sent to Podio',
                    'podio_items': results
                })
            else:
                return jsonify({'error': 'Failed to send any items to Podio'}), 500
        else:
            logger.warning("Вебхук не содержал обрабатываемых данных")
            return jsonify({'status': 'ignored', 'message': 'No processable data in webhook'})
    
    except Exception as e:
        logger.error(f"Ошибка обработки вебхука: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/webhook/test', methods=['POST'])
def test_webhook():
    """Тестовый эндпоинт для проверки работы вебхука"""
    try:
        data = request.get_json()
        logger.info(f"Тестовый вебхук: {json.dumps(data, ensure_ascii=False)}")
        
        return jsonify({
            'status': 'success',
            'message': 'Test webhook received',
            'received_data': data,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Ошибка тестового вебхука: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Статус интеграции и подключений"""
    try:
        # Проверка подключения к Podio
        podio_status = podio_client.check_connection()
        
        return jsonify({
            'service': 'Wazzup-Podio Integration',
            'status': 'running',
            'connections': {
                'podio': 'connected' if podio_status else 'disconnected'
            },
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Ошибка проверки статуса: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Обработчик 404 ошибок"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Обработчик 500 ошибок"""
    logger.error(f"Внутренняя ошибка сервера: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Настройка порта
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Запуск Wazzup-Podio Integration на порту {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
