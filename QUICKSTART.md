# Быстрый старт Wazzup-Podio Integration

## 🚀 За 5 минут до работающей интеграции

### 1. Подготовка данных

**У вас уже есть:**
- ✅ Wazzup API ключ: `1aab54ad811540da85bedbc685f938d6`
- ✅ Podio App ID: `30487652`
- ✅ Podio App Token: `05f0a7e72ffc77edb1da0ac4681ac10f`

**Нужно получить:**
- 🔑 Podio Client ID и Client Secret
- 📍 Podio Space ID

### 2. Получение недостающих данных Podio

1. **Client ID и Secret:**
   - Перейдите на [podio.com/developers](https://podio.com/developers)
   - Создайте новое приложение
   - Скопируйте Client ID и Client Secret

2. **Space ID:**
   - Откройте ваше рабочее пространство в Podio
   - Посмотрите URL: `https://podio.com/your-workspace-name`
   - Space ID можно найти в настройках пространства или через API

### 3. Развертывание на Railway (рекомендуется)

1. **Форк репозитория:**
   - Перейдите на [GitHub](https://github.com/Anastasia462208/wazzup-podio-integration)
   - Нажмите "Fork"

2. **Развертывание:**
   - Зайдите на [railway.app](https://railway.app)
   - Нажмите "Deploy from GitHub repo"
   - Выберите ваш форк репозитория
   - Railway автоматически развернет приложение

3. **Настройка переменных:**
   В разделе Variables добавьте:
   ```
   WAZZUP_API_KEY=1aab54ad811540da85bedbc685f938d6
   PODIO_CLIENT_ID=ваш_client_id
   PODIO_CLIENT_SECRET=ваш_client_secret
   PODIO_APP_ID=30487652
   PODIO_APP_TOKEN=05f0a7e72ffc77edb1da0ac4681ac10f
   PODIO_SPACE_ID=ваш_space_id
   PORT=5000
   ```

4. **Получение URL:**
   После развертывания скопируйте URL вида: `https://your-app.railway.app`

### 4. Настройка вебхука в Wazzup

**Быстрый способ через curl:**
```bash
curl -X PATCH https://api.wazzup24.com/v3/webhooks \
  -H "Authorization: Bearer 1aab54ad811540da85bedbc685f938d6" \
  -H "Content-Type: application/json" \
  -d '{
    "webhooksUrl": "https://your-app.railway.app/webhook/wazzup",
    "subscriptions": {
      "messagesAndStatuses": true,
      "contactsAndDealsCreation": false,
      "channelsUpdates": false
    }
  }'
```

### 5. Создание приложения в Podio

1. **Создайте новое приложение "Wazzup Messages"**
2. **Добавьте поля:**
   - Имя контакта (текст)
   - Телефон (текст)
   - Текст сообщения (текст, большой)
   - Тип сообщения (выбор: Текст, Изображение, Видео, Аудио, Документ)
   - Направление (выбор: Входящее, Исходящее)
   - Дата сообщения (дата/время)
   - ID чата (текст)
   - Источник (выбор: Wazzup, WhatsApp, Telegram, Instagram)

### 6. Тестирование

1. **Проверьте статус:**
   ```bash
   curl https://your-app.railway.app/status
   ```

2. **Отправьте тестовое сообщение:**
   - Отправьте сообщение на любой канал Wazzup
   - Проверьте появление записи в Podio

## ✅ Готово!

Теперь все входящие сообщения из Wazzup автоматически появляются в вашем приложении Podio.

## 🔧 Альтернативные платформы

### Render
- Перейдите на [render.com](https://render.com)
- Создайте Web Service из GitHub репозитория
- Настройте переменные окружения

### Heroku
- Установите Heroku CLI
- `heroku create your-app-name`
- `git push heroku master`
- Настройте переменные через `heroku config:set`

## 📞 Поддержка

Если что-то не работает:
1. Проверьте логи приложения на платформе
2. Убедитесь, что все переменные окружения настроены
3. Проверьте `/status` эндпоинт для диагностики подключений
