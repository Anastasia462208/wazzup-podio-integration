#!/usr/bin/env python3
"""
Модуль для отправки сообщений через Wazzup API
"""

import os
import requests
import logging
from typing import Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class WazzupSender:
    """Класс для отправки сообщений через Wazzup API"""
    
    def __init__(self):
        self.api_key = os.getenv('WAZZUP_API_KEY')
        self.base_url = 'https://api.wazzup24.com/v3'
        self.channel_id = os.getenv('WAZZUP_CHANNEL_ID', '876c0da6-64ca-4aae-bf97-174348d56709')
        
        if not self.api_key:
            raise ValueError("WAZZUP_API_KEY не найден в переменных окружения")
    
    def send_message(self, chat_id: str, text: str, message_type: str = 'text') -> Optional[Dict]:
        """
        Отправка сообщения через Wazzup API
        
        Args:
            chat_id: ID чата (например, "79002121614")
            text: Текст сообщения
            message_type: Тип сообщения (text, image, etc.)
            
        Returns:
            Ответ API или None в случае ошибки
        """
        try:
            # Формируем chat_id в правильном формате для WhatsApp
            if not chat_id.endswith('@c.us'):
                formatted_chat_id = f"{chat_id}@c.us"
            else:
                formatted_chat_id = chat_id
            
            # Подготавливаем данные для отправки
            message_data = {
                'channelId': self.channel_id,
                'chatId': formatted_chat_id,
                'chatType': 'whatsapp',
                'text': text
            }
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}/message"
            
            logger.info(f"Отправка сообщения в чат {formatted_chat_id}: {text[:50]}...")
            
            response = requests.post(url, json=message_data, headers=headers)
            
            if response.status_code in [200, 201]:
                result = response.json()
                logger.info(f"Сообщение отправлено успешно: {result.get('messageId', 'unknown')}")
                return result
            else:
                logger.error(f"Ошибка отправки сообщения: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Исключение при отправке сообщения: {e}")
            return None
    
    def send_reply_to_podio_comment(self, podio_comment: Dict[str, Any]) -> Optional[Dict]:
        """
        Отправка ответа на комментарий из Podio в WhatsApp
        
        Args:
            podio_comment: Данные комментария из Podio
            
        Returns:
            Результат отправки сообщения
        """
        try:
            # Извлекаем информацию из комментария Podio
            comment_text = podio_comment.get('value', '')
            
            # Ищем chat_id в связанном элементе или в тексте комментария
            # Это нужно будет адаптировать под структуру ваших данных
            chat_id = self._extract_chat_id_from_comment(podio_comment)
            
            if not chat_id:
                logger.error("Не удалось определить chat_id для ответа")
                return None
            
            # Отправляем сообщение
            return self.send_message(chat_id, comment_text)
            
        except Exception as e:
            logger.error(f"Ошибка отправки ответа из Podio: {e}")
            return None
    
    def _extract_chat_id_from_comment(self, podio_comment: Dict[str, Any]) -> Optional[str]:
        """
        Извлечение chat_id из комментария Podio
        Нужно адаптировать под структуру ваших данных
        """
        try:
            # Пример логики извлечения chat_id
            # Может быть в external_id, в тексте или в связанном элементе
            
            # Вариант 1: из external_id комментария
            external_id = podio_comment.get('external_id', '')
            if external_id and '@c.us' in external_id:
                return external_id.replace('@c.us', '')
            
            # Вариант 2: из текста комментария (если есть специальный формат)
            comment_text = podio_comment.get('value', '')
            if 'chat_id:' in comment_text.lower():
                # Ищем паттерн chat_id: 79002121614
                import re
                match = re.search(r'chat_id:\s*(\d+)', comment_text, re.IGNORECASE)
                if match:
                    return match.group(1)
            
            # Вариант 3: возвращаем дефолтный chat_id (для тестирования)
            # В реальной системе нужно получать из связанного элемента
            return "79002121614"  # Ваш номер для тестирования
            
        except Exception as e:
            logger.error(f"Ошибка извлечения chat_id: {e}")
            return None
    
    def get_channel_info(self) -> Optional[Dict]:
        """Получение информации о канале"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}/channels"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                channels = response.json()
                for channel in channels:
                    if channel.get('channelId') == self.channel_id:
                        return channel
                return channels[0] if channels else None
            else:
                logger.error(f"Ошибка получения каналов: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Ошибка получения информации о канале: {e}")
            return None

if __name__ == "__main__":
    # Тестирование модуля
    from dotenv import load_dotenv
    load_dotenv()
    
    sender = WazzupSender()
    
    # Тест отправки сообщения
    result = sender.send_message(
        chat_id="79002121614",
        text="🤖 Тестовое сообщение из Podio через интеграцию!"
    )
    
    if result:
        print(f"✅ Сообщение отправлено: {result}")
    else:
        print("❌ Ошибка отправки сообщения")
