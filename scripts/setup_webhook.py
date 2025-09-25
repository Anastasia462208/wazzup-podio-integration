#!/usr/bin/env python3
"""
Скрипт для настройки вебхука в Wazzup
Автоматически регистрирует URL вебхука в системе Wazzup
"""

import os
import json
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class WazzupWebhookSetup:
    """Класс для настройки вебхуков в Wazzup"""
    
    def __init__(self):
        self.api_key = os.getenv('WAZZUP_API_KEY')
        self.api_url = os.getenv('WAZZUP_API_URL', 'https://api.wazzup24.com/v3')
        self.webhook_url = os.getenv('WEBHOOK_URL')
        
        if not self.api_key:
            raise ValueError("WAZZUP_API_KEY не найден в переменных окружения")
        
        if not self.webhook_url:
            raise ValueError("WEBHOOK_URL не найден в переменных окружения")
    
    def setup_webhook(self):
        """Настройка вебхука в Wazzup"""
        try:
            url = f"{self.api_url}/webhooks"
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Конфигурация вебхука
            webhook_config = {
                "webhooksUrl": self.webhook_url,
                "subscriptions": {
                    "messagesAndStatuses": True,  # Вебхук о новых сообщениях и изменении статуса
                    "contactsAndDealsCreation": False,  # Вебхук о создании контактов и сделок
                    "channelsUpdates": False  # Вебхук об изменении статуса канала
                }
            }
            
            print(f"Настройка вебхука для URL: {self.webhook_url}")
            print(f"Конфигурация: {json.dumps(webhook_config, indent=2, ensure_ascii=False)}")
            
            # Отправка PATCH запроса
            response = requests.patch(url, headers=headers, json=webhook_config)
            
            if response.status_code == 200:
                print("✅ Вебхук успешно настроен!")
                result = response.json()
                print(f"Ответ сервера: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return True
            else:
                print(f"❌ Ошибка настройки вебхука: {response.status_code}")
                print(f"Ответ сервера: {response.text}")
                return False
        
        except Exception as e:
            print(f"❌ Исключение при настройке вебхука: {str(e)}")
            return False
    
    def get_webhook_info(self):
        """Получение информации о текущих настройках вебхука"""
        try:
            url = f"{self.api_url}/webhooks"
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                print("📋 Текущие настройки вебхука:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return result
            else:
                print(f"❌ Ошибка получения информации о вебхуке: {response.status_code}")
                print(f"Ответ сервера: {response.text}")
                return None
        
        except Exception as e:
            print(f"❌ Исключение при получении информации о вебхуке: {str(e)}")
            return None
    
    def test_webhook_connection(self):
        """Тестирование подключения к API Wazzup"""
        try:
            # Тестовый запрос к API для проверки авторизации
            url = f"{self.api_url}/channels"
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                print("✅ Подключение к API Wazzup успешно!")
                channels = response.json()
                print(f"Найдено каналов: {len(channels)}")
                return True
            else:
                print(f"❌ Ошибка подключения к API: {response.status_code}")
                print(f"Ответ сервера: {response.text}")
                return False
        
        except Exception as e:
            print(f"❌ Исключение при тестировании подключения: {str(e)}")
            return False

def main():
    """Основная функция"""
    print("🚀 Настройка вебхука Wazzup-Podio Integration")
    print("=" * 50)
    
    try:
        setup = WazzupWebhookSetup()
        
        # Тестирование подключения
        print("\n1. Тестирование подключения к API...")
        if not setup.test_webhook_connection():
            print("❌ Не удалось подключиться к API Wazzup. Проверьте API ключ.")
            return
        
        # Получение текущих настроек
        print("\n2. Получение текущих настроек вебхука...")
        setup.get_webhook_info()
        
        # Настройка вебхука
        print("\n3. Настройка нового вебхука...")
        if setup.setup_webhook():
            print("\n✅ Настройка завершена успешно!")
            print(f"Вебхук настроен на URL: {setup.webhook_url}")
            print("\nТеперь все входящие сообщения будут отправляться на ваш сервер.")
        else:
            print("\n❌ Не удалось настроить вебхук. Проверьте настройки.")
    
    except Exception as e:
        print(f"❌ Критическая ошибка: {str(e)}")

if __name__ == "__main__":
    main()
