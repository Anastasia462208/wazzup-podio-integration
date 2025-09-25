# Wazzup-Podio Integration

Интеграция между Wazzup и Podio для автоматической передачи сообщений и синхронизации переписки.

## Описание

Этот проект создает мост между мессенджером Wazzup и CRM-системой Podio, позволяя:
- Автоматически передавать входящие сообщения из Wazzup в Podio
- Сохранять историю переписки в структурированном виде
- Использовать Podio как централизованную систему для управления чатами

## Архитектура

```
Wazzup → Webhook → Flask App → Podio API
```

## Компоненты

- **Webhook Receiver**: Flask-приложение для приема вебхуков от Wazzup
- **Podio Integration**: Модуль для работы с Podio API
- **Message Processor**: Обработчик сообщений и их форматирование
- **Configuration**: Управление настройками и API ключами

## Установка и настройка

### Требования

- Python 3.11+
- Flask
- Requests
- Podio API ключи
- Wazzup API ключи

### Переменные окружения

```bash
WAZZUP_API_KEY=your_wazzup_api_key
PODIO_CLIENT_ID=your_podio_client_id
PODIO_CLIENT_SECRET=your_podio_client_secret
PODIO_APP_ID=your_podio_app_id
PODIO_APP_TOKEN=your_podio_app_token
```

## Использование

1. Настройте вебхук в Wazzup, указав URL вашего развернутого приложения
2. Настройте Podio workspace и получите необходимые API ключи
3. Запустите приложение
4. Сообщения из Wazzup будут автоматически появляться в Podio

## Развертывание

Приложение может быть развернуто на различных платформах:
- Heroku
- Railway
- Render
- GitHub Actions (для простых случаев)

## Лицензия

MIT License
