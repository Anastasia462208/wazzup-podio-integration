# Руководство по развертыванию Wazzup-Podio Integration

## Обзор

Данное руководство поможет развернуть интеграцию между Wazzup и Podio для автоматической передачи сообщений.

## Предварительные требования

### 1. Данные для интеграции

**Wazzup API:**
- API ключ: `1aab54ad811540da85bedbc685f938d6`
- Доступ к настройкам вебхуков в панели управления

**Podio API:**
- App ID: `30487652`
- App Token: `05f0a7e72ffc77edb1da0ac4681ac10f`
- Client ID и Client Secret (получить в Podio Developer)
- Space ID рабочего пространства

### 2. Хостинг

Для бесплатного развертывания рекомендуется:
- **Railway** (рекомендуется)
- **Render**
- **Heroku** (с ограничениями)
- **GitHub Actions + Serverless**

## Пошаговая настройка

### Шаг 1: Подготовка Podio

1. **Создание приложения в Podio:**
   - Войдите в ваше рабочее пространство Podio
   - Создайте новое приложение "Wazzup Messages"
   - Добавьте поля согласно `config/podio_app_config.json`:
     - Имя контакта (текст)
     - Телефон (текст)
     - Текст сообщения (текст, большой)
     - Тип сообщения (категория)
     - Направление (категория)
     - Дата сообщения (дата/время)
     - ID чата (текст)
     - Источник (категория)
     - Статус (категория)
     - Ссылка на медиа (ссылка)

2. **Получение API данных:**
   - Перейдите в Developer раздел Podio
   - Создайте новое приложение для получения Client ID и Secret
   - Запишите Space ID вашего рабочего пространства

### Шаг 2: Развертывание на Railway

1. **Подготовка репозитория:**
   ```bash
   git add .
   git commit -m "Initial commit: Wazzup-Podio integration"
   git push origin main
   ```

2. **Создание проекта на Railway:**
   - Зайдите на [railway.app](https://railway.app)
   - Подключите ваш GitHub репозиторий
   - Railway автоматически определит Python проект

3. **Настройка переменных окружения:**
   В разделе Variables добавьте:
   ```
   WAZZUP_API_KEY=1aab54ad811540da85bedbc685f938d6
   PODIO_CLIENT_ID=ваш_podio_client_id
   PODIO_CLIENT_SECRET=ваш_podio_client_secret
   PODIO_APP_ID=30487652
   PODIO_APP_TOKEN=05f0a7e72ffc77edb1da0ac4681ac10f
   PODIO_SPACE_ID=ваш_podio_space_id
   PORT=5000
   FLASK_ENV=production
   ```

4. **Получение URL развертывания:**
   После успешного развертывания Railway предоставит URL вида:
   `https://your-app-name.railway.app`

### Шаг 3: Настройка вебхука в Wazzup

1. **Автоматическая настройка:**
   ```bash
   # Установите WEBHOOK_URL в переменные окружения
   export WEBHOOK_URL=https://your-app-name.railway.app/webhook/wazzup
   
   # Запустите скрипт настройки
   python3 scripts/setup_webhook.py
   ```

2. **Ручная настройка через API:**
   ```bash
   curl -X PATCH https://api.wazzup24.com/v3/webhooks \
     -H "Authorization: Bearer 1aab54ad811540da85bedbc685f938d6" \
     -H "Content-Type: application/json" \
     -d '{
       "webhooksUrl": "https://your-app-name.railway.app/webhook/wazzup",
       "subscriptions": {
         "messagesAndStatuses": true,
         "contactsAndDealsCreation": false,
         "channelsUpdates": false
       }
     }'
   ```

### Шаг 4: Тестирование

1. **Проверка работоспособности:**
   ```bash
   curl https://your-app-name.railway.app/
   ```

2. **Тестовый вебхук:**
   ```bash
   curl -X POST https://your-app-name.railway.app/webhook/test \
     -H "Content-Type: application/json" \
     -d '{"test": "message"}'
   ```

3. **Отправка тестового сообщения:**
   - Отправьте сообщение на любой подключенный канал Wazzup
   - Проверьте появление записи в приложении Podio

## Альтернативные варианты развертывания

### Render

1. Создайте новый Web Service на [render.com](https://render.com)
2. Подключите GitHub репозиторий
3. Настройте:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment Variables: как указано выше

### Heroku

1. Создайте файл `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Разверните через Heroku CLI:
   ```bash
   heroku create your-app-name
   heroku config:set WAZZUP_API_KEY=1aab54ad811540da85bedbc685f938d6
   # ... остальные переменные
   git push heroku main
   ```

## Мониторинг и отладка

### Логи приложения

- **Railway:** Вкладка "Logs" в панели управления
- **Render:** Раздел "Logs" в настройках сервиса
- **Heroku:** `heroku logs --tail`

### Проверка статуса интеграции

```bash
curl https://your-app-name.railway.app/status
```

### Типичные проблемы

1. **Ошибка 401 при настройке вебхука:**
   - Проверьте правильность API ключа Wazzup
   - Убедитесь, что ключ имеет права на настройку вебхуков

2. **Ошибка подключения к Podio:**
   - Проверьте правильность Client ID, Secret и App Token
   - Убедитесь, что приложение в Podio создано и активно

3. **Сообщения не появляются в Podio:**
   - Проверьте логи приложения
   - Убедитесь, что поля в Podio соответствуют конфигурации
   - Проверьте, что вебхук правильно настроен в Wazzup

## Безопасность

1. **Переменные окружения:**
   - Никогда не коммитьте API ключи в репозиторий
   - Используйте только переменные окружения для конфиденциальных данных

2. **HTTPS:**
   - Всегда используйте HTTPS для вебхука
   - Большинство платформ предоставляют SSL сертификаты автоматически

3. **Валидация вебхуков:**
   - При необходимости настройте WAZZUP_WEBHOOK_SECRET для дополнительной безопасности

## Поддержка

При возникновении проблем:
1. Проверьте логи приложения
2. Убедитесь в правильности всех настроек
3. Проверьте статус подключений через `/status` эндпоинт
