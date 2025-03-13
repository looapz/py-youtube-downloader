import os
import sys
from pytube import YouTube, Playlist
import argparse
import logging
from tqdm import tqdm

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def format_size(bytes):
    """Форматирует размер файла в человекочитаемый вид"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"

def sanitize_filename(filename):
    """Очищает имя файла от недопустимых символов"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def get_video_info(url):
    """Получает информацию о видео"""
    try:
        yt = YouTube(url)
        return {
            'title': yt.title,
            'author': yt.author,
            'length': f"{yt.length // 60}:{yt.length % 60:02d}",
            'views': yt.views,
            'description': yt.description,
            'streams': {
                'video': [
                    {
                        'itag': stream.itag,
                        'resolution': stream.resolution,
                        'fps': stream.fps,
                        'size': format_size(stream.filesize)
                    } for stream in yt.streams.filter(progressive=True).order_by('resolution')
                ],
                'audio': [
                    {
                        'itag': stream.itag,
                        'abr': stream.abr,
                        'size': format_size(stream.filesize)
                    } for stream in yt.streams.filter(only_audio=True).order_by('abr')
                ]
            }
        }
    except Exception as e:
        logging.error(f"Ошибка при получении информации о видео: {str(e)}")
        return None

def download_video(url, output_path=None, resolution=None, audio_only=False, format='mp4'):
    """Загружает видео с YouTube"""
    try:
        yt = YouTube(url)
        
        # Настраиваем обработчики прогресса
        progress_bar = None
        
        def progress_callback(stream, chunk, bytes_remaining):
            nonlocal progress_bar
            if progress_bar is None:
                total_size = stream.filesize
                progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
            progress_bar.update(len(chunk))
        
        def complete_callback(stream, file_path):
            if progress_bar:
                progress_bar.close()
            logging.info(f"\nЗагрузка завершена: {file_path}")
        
        yt.register_on_progress_callback(progress_callback)
        yt.register_on_complete_callback(complete_callback)
        
        # Создаем директорию для сохранения, если её нет
        if output_path and not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))
        
        # Выбираем поток для загрузки
        if audio_only:
            stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            if not output_path:
                filename = sanitize_filename(f"{yt.title}.{format}")
                output_path = os.path.join(os.getcwd(), filename)
        else:
            if resolution:
                stream = yt.streams.filter(progressive=True, resolution=resolution).first()
                if not stream:
                    logging.warning(f"Разрешение {resolution} недоступно. Использую наилучшее доступное качество.")
                    stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
            else:
                stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
            
            if not output_path:
                filename = sanitize_filename(f"{yt.title}.{format}")
                output_path = os.path.join(os.getcwd(), filename)
        
        # Загружаем видео
        logging.info(f"Начинаю загрузку: {yt.title}")
        stream.download(output_path=os.path.dirname(output_path), filename=os.path.basename(output_path))
        
        return True
    except Exception as e:
        logging.error(f"Ошибка при загрузке видео: {str(e)}")
        if progress_bar:
            progress_bar.close()
        return False

def download_playlist(url, output_dir=None, resolution=None, audio_only=False, format='mp4'):
    """Загружает все видео из плейлиста"""
    try:
        playlist = Playlist(url)
        if not playlist.video_urls:
            logging.error("Плейлист пуст или недоступен")
            return False
        
        if not output_dir:
            output_dir = os.path.join(os.getcwd(), sanitize_filename(playlist.title))
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        logging.info(f"Начинаю загрузку плейлиста: {playlist.title}")
        logging.info(f"Всего видео: {len(playlist.video_urls)}")
        
        for index, video_url in enumerate(playlist.video_urls, 1):
            logging.info(f"\nЗагрузка видео {index} из {len(playlist.video_urls)}")
            filename = f"{index:03d}.{format}"
            output_path = os.path.join(output_dir, filename)
            
            success = download_video(
                video_url,
                output_path=output_path,
                resolution=resolution,
                audio_only=audio_only,
                format=format
            )
            
            if not success:
                logging.warning(f"Не удалось загрузить видео {index}")
        
        return True
    except Exception as e:
        logging.error(f"Ошибка при загрузке плейлиста: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Загрузчик видео с YouTube')
    parser.add_argument('url', help='URL видео или плейлиста на YouTube')
    parser.add_argument('-o', '--output', help='Путь для сохранения файла или директория для плейлиста')
    parser.add_argument('-r', '--resolution', help='Разрешение видео (например, 720p)')
    parser.add_argument('-a', '--audio-only', action='store_true', help='Загрузить только аудио')
    parser.add_argument('-f', '--format', default='mp4', help='Формат выходного файла (mp4, mp3 и т.д.)')
    parser.add_argument('-p', '--playlist', action='store_true', help='Загрузить весь плейлист')
    parser.add_argument('-i', '--info', action='store_true', help='Показать информацию о видео')
    
    args = parser.parse_args()
    
    if args.info and not args.playlist:
        info = get_video_info(args.url)
        if info:
            print(f"\nИнформация о видео:")
            print(f"Название: {info['title']}")
            print(f"Автор: {info['author']}")
            print(f"Длительность: {info['length']}")
            print(f"Просмотры: {info['views']}\n")
            
            print("Доступные форматы видео:")
            for stream in info['streams']['video']:
                print(f"- {stream['resolution']} ({stream['fps']} fps, {stream['size']})")
            
            print("\nДоступные форматы аудио:")
            for stream in info['streams']['audio']:
                print(f"- {stream['abr']} ({stream['size']})")
        return
    
    if args.playlist:
        success = download_playlist(
            args.url,
            output_dir=args.output,
            resolution=args.resolution,
            audio_only=args.audio_only,
            format=args.format
        )
    else:
        success = download_video(
            args.url,
            output_path=args.output,
            resolution=args.resolution,
            audio_only=args.audio_only,
            format=args.format
        )
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()