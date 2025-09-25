# Структура вебхуков Wazzup

## Общая информация

Вебхуки отправляются методом POST на указанный URL и содержат JSON в теле запроса с заголовком `Content-Type: application/json; charset-utf-8`.

## Настройка вебхука

Для подключения вебхука используется PATCH запрос:
```
PATCH https://api.wazzup24.com/v3/webhooks
```

## Типы вебхуков

### 1. Вебхук сообщений (messages)

JSON-объект с ключом `messages`, содержащий массив объектов сообщений:

#### Основные параметры:
- `messageId` (String, uuid4) - GUID сообщения в Wazzup
- `channelId` (String, uuid4) - ID канала
- `chatType` (String) - Тип чата (whatsapp, whatsgroup, viber, instagram, telegram, telegroup, vk, avito)
- `chatId` (String) - ID чата (номер телефона для WhatsApp/Viber, username для Instagram и т.д.)
- `dateTime` (String) - Время отправки в формате yyyy-mm-ddThh:mm:ss.ms
- `type` (String) - Тип сообщения (text, image, audio, video, document, vcard, geo, wapi_template, unsupported, missing_call)
- `isEcho` (Boolean) - false для входящих, true для исходящих сообщений
- `text` (String) - Текст сообщения
- `contentUri` (String) - Ссылка на контент сообщения
- `status` (String) - Статус сообщения (sent, delivered, read, error, inbound)

#### Информация о контакте:
- `contact.name` (String) - Имя контакта
- `contact.avatarUri` (String) - URI аватарки контакта
- `contact.username` (String) - Username для Telegram
- `contact.phone` (String) - Телефон для Telegram

#### Дополнительные параметры:
- `error` (Object) - Информация об ошибке (если status: error)
- `authorName` (String) - Имя пользователя, отправившего сообщение
- `authorId` (String) - Идентификатор пользователя CRM
- `instPost` (Object) - Информация о посте Instagram
- `interactive` (Interactive) - Кнопки Salesbot amoCRM
- `quotedMessage` (Object) - Цитируемое сообщение
- `sentFromApp` (Boolean) - Отправлено из приложения Wazzup
- `isEdited` (Boolean) - Сообщение отредактировано
- `isDeleted` (Boolean) - Сообщение удалено
- `oldInfo` (Object) - Информация об измененном/удаленном сообщении

### 2. Вебхук статусов (statuses)

JSON-объект с ключом `statuses`, содержащий массив объектов статусов:

#### Параметры:
- `messageId` (String) - GUID сообщения в Wazzup
- `timestamp` (String) - Время получения информации об обновлении статуса
- `status` (String) - Обновленный статус (sent, delivered, read, error, edited)

## Коды ошибок

- `BAD_CONTACT` - Аккаунт с таким chatId не существует
- `CHATID_IGSID_MISMATCH` - Аккаунт Instagram не существует
- `TOO_LONG_TEXT` - Слишком длинный текст
- `BAD_LINK` - Фильтры Instagram не пропускают ссылку
- `TOO_BIG_CONTENT` - Размер файла превышает 50 Мб
- `SPAM` - Подозрение на спам
- `24_HOURS_EXCEEDED` - 24-часовое окно WABA закрыто
- `7_DAYS_EXCEEDED` - 7-дневное окно Instagram закрыто
- И другие...

## Авторизация

Если есть crmKey, добавляется заголовок `Authorization: Bearer ${crmKey}`.

## Ответ

Ожидается код 200 OK. В некоторых случаях ждем определенную информацию в теле ответа. Таймаут — 30 секунд.
