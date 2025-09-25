# Настройка Podio API

## ❌ Проблема с текущими ключами

Текущие Podio API ключи не работают:
- **Client ID:** `pZqUvnzzLx2ncMdUk5x227lGBIWrqhT2XA9JPg2nNU342xcAHq1sOrkoKIC9QbQd`
- **Client Secret:** `brige`

**Ошибка:** `invalid_client_id` - неверный Client ID

## ✅ Как получить правильные ключи

### Шаг 1: Создание приложения в Podio

1. **Перейдите на страницу разработчиков:**
   - Откройте [podio.com/developers](https://podio.com/developers)
   - Войдите в свой аккаунт Podio

2. **Создайте новое приложение:**
   - Нажмите "Create new app"
   - Заполните форму:
     - **App name:** `Wazzup Integration`
     - **Description:** `Integration between Wazzup and Podio for message synchronization`
     - **URL:** `https://your-domain.com` (можно указать любой)

3. **Получите ключи:**
   - После создания приложения вы получите:
     - **Client ID** (длинная строка)
     - **Client Secret** (короткая строка)

### Шаг 2: Получение App Token

1. **В вашем рабочем пространстве Podio:**
   - Перейдите в приложение "Wazzup Messages"
   - Откройте настройки приложения
   - Перейдите в раздел "Developer"

2. **Создайте App Token:**
   - Нажмите "Generate new app token"
   - Скопируйте полученный токен

### Шаг 3: Получение Space ID

1. **Найдите Space ID:**
   - Откройте ваше рабочее пространство
   - Посмотрите URL: `https://podio.com/your-workspace-name`
   - Или используйте API запрос:
   ```bash
   curl -H "Authorization: OAuth2 YOUR_ACCESS_TOKEN" \
        https://api.podio.com/space/
   ```

## 🔧 Альтернативный способ аутентификации

Если у вас есть проблемы с App Authentication, можно использовать User Authentication:

### 1. Получение Authorization Code

Откройте в браузере:
```
https://podio.com/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code
```

### 2. Обмен кода на токен

```bash
curl -X POST https://api.podio.com/oauth/token \
  -d "grant_type=authorization_code" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=YOUR_REDIRECT_URI" \
  -d "code=AUTHORIZATION_CODE"
```

## 📋 Что нужно обновить

После получения правильных ключей обновите переменные окружения:

```bash
PODIO_CLIENT_ID=ваш_новый_client_id
PODIO_CLIENT_SECRET=ваш_новый_client_secret
PODIO_APP_ID=30487652  # Остается тот же
PODIO_APP_TOKEN=ваш_новый_app_token
PODIO_SPACE_ID=ваш_space_id
```

## 🧪 Тестирование

После обновления ключей запустите тест:

```bash
python3 -c "
from src.podio.client import PodioClient
from dotenv import load_dotenv
load_dotenv()
client = PodioClient()
print('Результат:', client.check_connection())
"
```

## 📞 Поддержка Podio

Если возникают проблемы:
- [Podio Developer Documentation](https://developers.podio.com/)
- [Podio API Reference](https://developers.podio.com/doc)
- [Podio Support](https://help.podio.com/)
