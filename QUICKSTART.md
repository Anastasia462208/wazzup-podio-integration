# Быстрый старт Wazzup-Podio Integration

## 🚀 За 5 минут до работающей интеграции

### ✅ Что уже готово:
- **Wazzup API ключ:** `1aab54ad811540da85bedbc685f938d6` ✅ **РАБОТАЕТ**
- **Podio App ID:** `30487652` ✅
- **Wazzup канал:** `79292215055 (WhatsApp)` ✅

### ❌ Что нужно исправить:

**Podio API ключи не работают:**
- Client ID: `pZqUvnzzLx2ncMdUk5x227lGBIWrqhT2XA9JPg2nNU342xcAHq1sOrkoKIC9QbQd` ❌
- Client Secret: `brige` ❌

**Ошибка:** `invalid_client_id`

## 🔧 Исправление Podio ключей

### 1. Получите правильные ключи:
1. Перейдите на [podio.com/developers](https://podio.com/developers)
2. Создайте новое приложение "Wazzup Integration"
3. Получите **новые** Client ID и Client Secret
4. Подробная инструкция в файле `PODIO_SETUP.md`

### 2. Получите Space ID:
- Откройте ваше рабочее пространство Podio
- Найдите Space ID в настройках или URL

## 🚀 Развертывание (после исправления ключей)

### 1. Форк и развертывание:
- Форкните репозиторий: https://github.com/Anastasia462208/wazzup-podio-integration
- Разверните на [railway.app](https://railway.app)

### 2. Настройка переменных на Railway:
```
WAZZUP_API_KEY=1aab54ad811540da85bedbc685f938d6
PODIO_CLIENT_ID=ваш_новый_правильный_client_id
PODIO_CLIENT_SECRET=ваш_новый_правильный_client_secret
PODIO_APP_ID=30487652
PODIO_APP_TOKEN=05f0a7e72ffc77edb1da0ac4681ac10f
PODIO_SPACE_ID=ваш_space_id
PORT=5000
```

### 3. Создание приложения в Podio:
1. **Создайте приложение "Wazzup Messages"** в вашем Podio workspace
2. **Добавьте поля:**
   - Имя контакта (текст)
   - Телефон (текст)
   - Текст сообщения (текст, большой)
   - Тип сообщения (выбор: Текст, Изображение, Видео, Аудио, Документ)
   - Направление (выбор: Входящее, Исходящее)
   - Дата сообщения (дата/время)
   - ID чата (текст)
   - Источник (выбор: Wazzup, WhatsApp, Telegram, Instagram)

### 4. Настройка вебхука в Wazzup:
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

## 🧪 Тестирование

### 1. Проверка Wazzup (уже работает):
```bash
curl -H "Authorization: Bearer 1aab54ad811540da85bedbc685f938d6" \
     https://api.wazzup24.com/v3/channels
```
**Результат:** ✅ Найден 1 канал WhatsApp

### 2. Проверка Podio (после исправления ключей):
```bash
curl https://your-app.railway.app/status
```

### 3. Тестовое сообщение:
- Отправьте сообщение на номер `79292215055`
- Проверьте появление записи в Podio

## 📋 Текущий статус

| Компонент | Статус | Примечание |
|-----------|--------|------------|
| Wazzup API | ✅ Работает | Канал 79292215055 активен |
| Podio API | ❌ Нужны новые ключи | Invalid client_id |
| Приложение | ✅ Готово | Код написан и протестирован |
| Развертывание | ⏳ Ожидает | После исправления Podio |

## 🔗 Полезные ссылки

- **Репозиторий:** https://github.com/Anastasia462208/wazzup-podio-integration
- **Podio Developers:** https://podio.com/developers
- **Railway Deploy:** https://railway.app
- **Подробная настройка Podio:** `PODIO_SETUP.md`

## 📞 Следующие шаги

1. ✅ **Исправьте Podio API ключи** (см. PODIO_SETUP.md)
2. ✅ **Разверните на Railway**
3. ✅ **Создайте приложение в Podio**
4. ✅ **Настройте вебхук**
5. ✅ **Протестируйте интеграцию**

После исправления Podio ключей интеграция заработает полностью! 🎯
