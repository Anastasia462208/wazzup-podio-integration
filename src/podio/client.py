"""
Клиент для работы с Podio API
Модуль для создания и управления элементами в Podio
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional, Any, List
import requests

logger = logging.getLogger(__name__)

class PodioClient:
    """Клиент для работы с Podio API"""
    
    def __init__(self):
        self.client_id = os.getenv('PODIO_CLIENT_ID', '')
        self.client_secret = os.getenv('PODIO_CLIENT_SECRET', '')
        self.app_id = os.getenv('PODIO_APP_ID', '')
        self.app_token = os.getenv('PODIO_APP_TOKEN', '')
        self.space_id = os.getenv('PODIO_SPACE_ID', '')
        
        self.base_url = 'https://api.podio.com'
        self.access_token = None
        self.token_expires_at = None
        
        # Инициализация подключения
        self._authenticate()
    
    def _authenticate(self) -> bool:
        """Аутентификация в Podio API"""
        try:
            if not all([self.client_id, self.client_secret, self.app_id, self.app_token]):
                logger.error("Не все параметры Podio API настроены")
                return False
            
            # Используем App Authentication для простоты
            url = f"{self.base_url}/oauth/token"
            
            data = {
                'grant_type': 'app',
                'app_id': self.app_id,
                'app_token': self.app_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                expires_in = token_data.get('expires_in', 3600)
                
                # Вычисляем время истечения токена
                from datetime import timedelta
                self.token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
                
                logger.info("Успешная аутентификация в Podio")
                return True
            else:
                logger.error(f"Ошибка аутентификации в Podio: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Исключение при аутентификации в Podio: {str(e)}")
            return False
    
    def _ensure_authenticated(self) -> bool:
        """Проверка и обновление токена при необходимости"""
        if not self.access_token:
            return self._authenticate()
        
        # Проверяем, не истек ли токен
        if self.token_expires_at and datetime.utcnow() >= self.token_expires_at:
            logger.info("Токен истек, обновляем...")
            return self._authenticate()
        
        return True
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Выполнение запроса к Podio API"""
        try:
            if not self._ensure_authenticated():
                logger.error("Не удалось аутентифицироваться в Podio")
                return None
            
            url = f"{self.base_url}{endpoint}"
            headers = {
                'Authorization': f'OAuth2 {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=data)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            else:
                logger.error(f"Неподдерживаемый HTTP метод: {method}")
                return None
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                logger.error(f"Ошибка API Podio: {response.status_code} - {response.text}")
                return None
        
        except Exception as e:
            logger.error(f"Ошибка запроса к Podio API: {str(e)}")
            return None
    
    def check_connection(self) -> bool:
        """Проверка подключения к Podio"""
        try:
            result = self._make_request('GET', f'/app/{self.app_id}')
            return result is not None
        except:
            return False
    
    def get_app_fields(self) -> Optional[List[Dict]]:
        """Получение полей приложения Podio"""
        try:
            result = self._make_request('GET', f'/app/{self.app_id}')
            if result:
                return result.get('fields', [])
            return None
        except Exception as e:
            logger.error(f"Ошибка получения полей приложения: {str(e)}")
            return None
    
    def create_message_item(self, message_data: Dict[str, Any]) -> Optional[Dict]:
        """
        Создание элемента в Podio для сообщения
        """
        try:
            # Подготовка данных для создания элемента
            fields = self._prepare_item_fields(message_data)
            
            item_data = {
                'fields': fields
            }
            
            # Создание элемента
            result = self._make_request('POST', f'/item/app/{self.app_id}/', item_data)
            
            if result:
                item_id = result.get('item_id')
                logger.info(f"Создан элемент в Podio с ID: {item_id}")
                
                # Добавление комментария с форматированным сообщением
                self._add_comment_to_item(item_id, message_data)
                
                return {
                    'item_id': item_id,
                    'podio_url': f"https://podio.com/app/{self.app_id}/items/{item_id}"
                }
            
            return None
        
        except Exception as e:
            logger.error(f"Ошибка создания элемента в Podio: {str(e)}")
            return None
    
    def _prepare_item_fields(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Подготовка полей для создания элемента в Podio"""
        try:
            # Базовые поля (адаптируйте под вашу структуру приложения в Podio)
            fields = {}
            
            # Поле "Контакт" (текстовое поле)
            if 'contact_name' in message_data:
                fields['contact-name'] = {
                    'value': message_data['contact_name']
                }
            
            # Поле "Телефон" (текстовое поле)
            if 'contact_phone' in message_data:
                fields['contact-phone'] = {
                    'value': message_data['contact_phone']
                }
            
            # Поле "Сообщение" (текстовое поле)
            if 'message_text' in message_data:
                fields['message-text'] = {
                    'value': message_data['message_text']
                }
            
            # Поле "Тип сообщения" (категория)
            if 'message_type' in message_data:
                fields['message-type'] = {
                    'value': message_data['message_type']
                }
            
            # Поле "Направление" (категория)
            if 'direction' in message_data:
                fields['direction'] = {
                    'value': message_data['direction']
                }
            
            # Поле "Дата сообщения" (дата)
            if 'timestamp' in message_data:
                try:
                    # Конвертируем timestamp в формат Podio
                    dt = datetime.fromisoformat(message_data['timestamp'].replace('Z', '+00:00'))
                    fields['message-date'] = {
                        'start': dt.strftime('%Y-%m-%d %H:%M:%S')
                    }
                except:
                    pass
            
            # Поле "Chat ID" (текстовое поле)
            if 'chat_id' in message_data:
                fields['chat-id'] = {
                    'value': message_data['chat_id']
                }
            
            # Поле "Источник" (категория)
            fields['source'] = {
                'value': message_data.get('source', 'wazzup')
            }
            
            return fields
        
        except Exception as e:
            logger.error(f"Ошибка подготовки полей: {str(e)}")
            return {}
    
    def _add_comment_to_item(self, item_id: int, message_data: Dict[str, Any]) -> bool:
        """Добавление комментария к элементу с форматированным сообщением"""
        try:
            from src.wazzup.webhook_handler import WazzupWebhookHandler
            
            # Форматируем сообщение
            handler = WazzupWebhookHandler()
            formatted_message = handler.format_message_for_podio(message_data)
            
            comment_data = {
                'value': formatted_message,
                'external_id': message_data.get('message_id', '')
            }
            
            result = self._make_request('POST', f'/comment/item/{item_id}/', comment_data)
            
            if result:
                logger.info(f"Добавлен комментарий к элементу {item_id}")
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Ошибка добавления комментария: {str(e)}")
            return False
    
    def find_existing_chat(self, chat_id: str) -> Optional[Dict]:
        """Поиск существующего чата по chat_id"""
        try:
            # Поиск по полю chat-id
            filter_data = {
                'filters': {
                    'chat-id': chat_id
                },
                'limit': 1
            }
            
            result = self._make_request('POST', f'/item/app/{self.app_id}/filter/', filter_data)
            
            if result and result.get('items'):
                return result['items'][0]
            
            return None
        
        except Exception as e:
            logger.error(f"Ошибка поиска чата: {str(e)}")
            return None
    
    def update_item(self, item_id: int, fields: Dict[str, Any]) -> Optional[Dict]:
        """Обновление существующего элемента"""
        try:
            update_data = {
                'fields': fields
            }
            
            result = self._make_request('PUT', f'/item/{item_id}', update_data)
            
            if result:
                logger.info(f"Обновлен элемент {item_id}")
                return result
            
            return None
        
        except Exception as e:
            logger.error(f"Ошибка обновления элемента: {str(e)}")
            return None
