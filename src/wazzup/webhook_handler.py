"""
Обработчик вебхуков от Wazzup
Модуль для валидации и обработки входящих сообщений
"""

import os
import json
import hashlib
import hmac
import logging
from datetime import datetime
from typing import Dict, Optional, Any, List

logger = logging.getLogger(__name__)

class WazzupWebhookHandler:
    """Класс для обработки вебхуков от Wazzup"""
    
    def __init__(self):
        self.webhook_secret = os.getenv('WAZZUP_WEBHOOK_SECRET', '')
        self.api_key = os.getenv('WAZZUP_API_KEY', '')
    
    def validate_webhook(self, request) -> bool:
        """
        Валидация вебхука от Wazzup
        Проверяет подпись запроса для обеспечения безопасности
        """
        try:
            if not self.webhook_secret:
                logger.warning("WAZZUP_WEBHOOK_SECRET не настроен, пропускаем валидацию")
                return True
            
            # Получение подписи из заголовков
            signature = request.headers.get('X-Wazzup-Signature', '')
            if not signature:
                logger.error("Отсутствует заголовок X-Wazzup-Signature")
                return False
            
            # Получение тела запроса
            body = request.get_data()
            
            # Вычисление ожидаемой подписи
            expected_signature = self._calculate_signature(body)
            
            # Сравнение подписей
            return hmac.compare_digest(signature, expected_signature)
        
        except Exception as e:
            logger.error(f"Ошибка валидации вебхука: {str(e)}")
            return False
    
    def _calculate_signature(self, body: bytes) -> str:
        """Вычисление HMAC подписи для тела запроса"""
        return hmac.new(
            self.webhook_secret.encode('utf-8'),
            body,
            hashlib.sha256
        ).hexdigest()
    
    def process_webhook(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Обработка вебхука от Wazzup
        Возвращает список структурированных данных для отправки в Podio
        """
        try:
            processed_items = []
            
            # Обработка сообщений
            if 'messages' in data:
                for message in data['messages']:
                    processed_message = self._process_message(message)
                    if processed_message:
                        processed_items.append(processed_message)
            
            # Обработка статусов
            if 'statuses' in data:
                for status in data['statuses']:
                    processed_status = self._process_status(status)
                    if processed_status:
                        processed_items.append(processed_status)
            
            return processed_items
        
        except Exception as e:
            logger.error(f"Ошибка обработки вебхука: {str(e)}")
            return []
    
    def _process_message(self, message_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Обработка отдельного сообщения"""
        try:
            # Извлечение основной информации согласно документации Wazzup
            message_id = message_data.get('messageId', '')
            channel_id = message_data.get('channelId', '')
            chat_type = message_data.get('chatType', '')
            chat_id = message_data.get('chatId', '')
            date_time = message_data.get('dateTime', datetime.utcnow().isoformat())
            message_type = message_data.get('type', 'text')
            is_echo = message_data.get('isEcho', False)
            message_text = message_data.get('text', '')
            content_uri = message_data.get('contentUri', '')
            status = message_data.get('status', 'inbound')
            
            # Информация о контакте
            contact = message_data.get('contact', {})
            contact_name = contact.get('name', 'Неизвестный контакт')
            contact_avatar = contact.get('avatarUri', '')
            contact_username = contact.get('username', '')
            contact_phone = contact.get('phone', chat_id)
            
            # Дополнительная информация
            author_name = message_data.get('authorName', '')
            author_id = message_data.get('authorId', '')
            is_edited = message_data.get('isEdited', False)
            is_deleted = message_data.get('isDeleted', False)
            sent_from_app = message_data.get('sentFromApp', False)
            
            # Определение направления сообщения
            direction = 'outbound' if is_echo else 'inbound'
            
            # Формирование структурированного объекта
            processed_message = {
                'source': 'wazzup',
                'event_type': 'message',
                'message_id': message_id,
                'channel_id': channel_id,
                'chat_type': chat_type,
                'chat_id': chat_id,
                'contact_name': contact_name,
                'contact_phone': contact_phone,
                'contact_username': contact_username,
                'contact_avatar': contact_avatar,
                'message_text': message_text,
                'message_type': message_type,
                'content_uri': content_uri,
                'timestamp': date_time,
                'direction': direction,
                'status': status,
                'author_name': author_name,
                'author_id': author_id,
                'is_edited': is_edited,
                'is_deleted': is_deleted,
                'sent_from_app': sent_from_app,
                'raw_data': message_data
            }
            
            # Логирование
            direction_text = "исходящее" if is_echo else "входящее"
            logger.info(f"Обработано {direction_text} сообщение: {contact_name} ({chat_type}): {message_text[:50]}...")
            
            return processed_message
        
        except Exception as e:
            logger.error(f"Ошибка обработки сообщения: {str(e)}")
            return None
    
    def _process_status(self, status_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Обработка изменения статуса сообщения"""
        try:
            message_id = status_data.get('messageId', '')
            timestamp = status_data.get('timestamp', datetime.utcnow().isoformat())
            status = status_data.get('status', '')
            
            # Обрабатываем только важные статусы
            important_statuses = ['delivered', 'read', 'error', 'edited']
            
            if status not in important_statuses:
                return None
            
            processed_status = {
                'source': 'wazzup',
                'event_type': 'status_update',
                'message_id': message_id,
                'status': status,
                'timestamp': timestamp,
                'raw_data': status_data
            }
            
            logger.info(f"Обработан статус: {message_id} - {status}")
            
            return processed_status
        
        except Exception as e:
            logger.error(f"Ошибка обработки статуса: {str(e)}")
            return None
    
    def format_message_for_podio(self, message_data: Dict[str, Any]) -> str:
        """Форматирование сообщения для отображения в Podio"""
        try:
            if message_data.get('event_type') == 'status_update':
                return self._format_status_for_podio(message_data)
            
            contact_name = message_data.get('contact_name', 'Неизвестный')
            contact_phone = message_data.get('contact_phone', '')
            contact_username = message_data.get('contact_username', '')
            message_text = message_data.get('message_text', '')
            message_type = message_data.get('message_type', 'text')
            chat_type = message_data.get('chat_type', '')
            direction = message_data.get('direction', 'inbound')
            timestamp = message_data.get('timestamp', '')
            is_edited = message_data.get('is_edited', False)
            is_deleted = message_data.get('is_deleted', False)
            
            # Форматирование времени
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%d.%m.%Y %H:%M')
            except:
                formatted_time = timestamp
            
            # Определение иконки мессенджера
            messenger_icons = {
                'whatsapp': '💬',
                'whatsgroup': '👥',
                'telegram': '✈️',
                'telegroup': '👥✈️',
                'instagram': '📷',
                'viber': '💜',
                'vk': '🔵',
                'avito': '🏠'
            }
            
            messenger_icon = messenger_icons.get(chat_type, '📱')
            direction_icon = '📤' if direction == 'outbound' else '📥'
            
            # Базовый формат сообщения
            formatted_message = f"{messenger_icon} **{contact_name}**"
            
            if contact_username:
                formatted_message += f" (@{contact_username})"
            
            if contact_phone and contact_phone != contact_username:
                formatted_message += f" ({contact_phone})"
            
            formatted_message += f"\n{direction_icon} {formatted_time}"
            
            # Добавление меток для отредактированных/удаленных сообщений
            if is_edited:
                formatted_message += " ✏️ *отредактировано*"
            if is_deleted:
                formatted_message += " 🗑️ *удалено*"
            
            formatted_message += "\n\n"
            
            # Добавление содержимого в зависимости от типа
            type_icons = {
                'text': '',
                'image': '🖼️',
                'video': '🎥',
                'audio': '🎵',
                'document': '📄',
                'vcard': '👤',
                'geo': '📍',
                'wapi_template': '📋',
                'unsupported': '❓',
                'missing_call': '📞'
            }
            
            type_icon = type_icons.get(message_type, '📎')
            
            if message_type == 'text':
                formatted_message += message_text
            else:
                formatted_message += f"{type_icon} {message_type.title()}"
                if message_text:
                    formatted_message += f"\n{message_text}"
            
            # Добавление ссылки на контент
            content_uri = message_data.get('content_uri')
            if content_uri:
                formatted_message += f"\n\n🔗 [Файл]({content_uri})"
            
            return formatted_message
        
        except Exception as e:
            logger.error(f"Ошибка форматирования сообщения: {str(e)}")
            return f"Ошибка форматирования сообщения: {str(e)}"
    
    def _format_status_for_podio(self, status_data: Dict[str, Any]) -> str:
        """Форматирование статуса для отображения в Podio"""
        try:
            message_id = status_data.get('message_id', '')
            status = status_data.get('status', '')
            timestamp = status_data.get('timestamp', '')
            
            # Форматирование времени
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%d.%m.%Y %H:%M')
            except:
                formatted_time = timestamp
            
            status_icons = {
                'sent': '📤',
                'delivered': '✅',
                'read': '👁️',
                'error': '❌',
                'edited': '✏️'
            }
            
            status_names = {
                'sent': 'отправлено',
                'delivered': 'доставлено',
                'read': 'прочитано',
                'error': 'ошибка',
                'edited': 'отредактировано'
            }
            
            icon = status_icons.get(status, '📋')
            name = status_names.get(status, status)
            
            return f"{icon} **Статус обновлен**: {name}\n🕐 {formatted_time}\n📨 ID: {message_id[:8]}..."
        
        except Exception as e:
            logger.error(f"Ошибка форматирования статуса: {str(e)}")
            return f"Обновление статуса: {status}"
