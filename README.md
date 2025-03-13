# Загрузчик видео с YouTube

Простой и мощный инструмент для загрузки видео с YouTube. Поддерживает загрузку отдельных видео и целых плейлистов, с возможностью выбора качества и формата.

## Возможности

- Загрузка отдельных видео
- Загрузка целых плейлистов
- Выбор качества видео
- Загрузка только аудио
- Поддержка различных форматов
- Отображение прогресса загрузки
- Просмотр информации о видео перед загрузкой
- Автоматическая обработка ошибок

## Установка

```bash
git clone https://github.com/looapz/py-youtube-downloader.git
cd py-youtube-downloader
pip install -r requirements.txt
```

## Использование

### Просмотр информации о видео

```bash
python youtube_downloader.py -i "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Загрузка видео

Базовая загрузка (наилучшее качество):
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Загрузка с указанным разрешением:
```bash
python youtube_downloader.py -r 720p "https://www.youtube.com/watch?v=VIDEO_ID"
```

Загрузка только аудио в формате MP3:
```bash
python youtube_downloader.py -a -f mp3 "https://www.youtube.com/watch?v=VIDEO_ID"
```

Загрузка в указанную директорию:
```bash
python youtube_downloader.py -o "/path/to/output/video.mp4" "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Загрузка плейлиста

Загрузка всего плейлиста:
```bash
python youtube_downloader.py -p "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

Загрузка плейлиста в определенном качестве:
```bash
python youtube_downloader.py -p -r 720p "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

Загрузка только аудио из плейлиста:
```bash
python youtube_downloader.py -p -a -f mp3 "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

## Параметры командной строки

- `url`: URL видео или плейлиста на YouTube (обязательный параметр)
- `-o, --output`: Путь для сохранения файла или директория для плейлиста
- `-r, --resolution`: Разрешение видео (например, 720p)
- `-a, --audio-only`: Загрузить только аудио
- `-f, --format`: Формат выходного файла (mp4, mp3 и т.д.)
- `-p, --playlist`: Загрузить весь плейлист
- `-i, --info`: Показать информацию о видео

## Особенности

- Автоматический выбор наилучшего качества при недоступности указанного разрешения
- Прогресс-бар с отображением скорости загрузки
- Обработка ошибок и информативные сообщения
- Поддержка длинных названий файлов
- Автоматическое создание директорий при необходимости
- Очистка недопустимых символов в именах файлов

## Зависимости

- pytube: для работы с YouTube API
- tqdm: для отображения прогресса загрузки

## Требования к системе

- Python 3.6 или выше
- Установленные зависимости из requirements.txt
- Доступ в интернет

## Лицензия

MIT