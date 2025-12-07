#!/usr/bin/env python3
"""
TikTok Auto Viral Video Downloader
Busca y descarga automáticamente videos virales de TikTok
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime
import yt_dlp
import requests
from urllib.parse import quote


class TikTokAutoDownloader:
    def __init__(self, output_dir="downloads"):
        """
        Inicializa el descargador automático de TikTok

        Args:
            output_dir: Directorio donde se guardarán los videos
        """
        self.output_dir = output_dir
        self.create_output_dir()
        self.downloaded_videos = []

    def create_output_dir(self):
        """Crea el directorio de salida si no existe"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"✅ Directorio creado: {self.output_dir}")

    def download_video(self, url, include_metadata=True):
        """
        Descarga un video de TikTok

        Args:
            url: URL del video de TikTok
            include_metadata: Si es True, guarda también los metadatos

        Returns:
            dict: Información del video descargado
        """
        ydl_opts = {
            'outtmpl': os.path.join(self.output_dir, '%(id)s_%(title)s.%(ext)s'),
            'format': 'best',
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'writeinfojson': include_metadata,
            'writethumbnail': True,
            'postprocessors': [{
                'key': 'FFmpegMetadata',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"\n📥 Descargando: {url}")
                info = ydl.extract_info(url, download=True)

                video_info = {
                    'id': info.get('id'),
                    'title': info.get('title'),
                    'author': info.get('uploader') or info.get('creator'),
                    'views': info.get('view_count'),
                    'likes': info.get('like_count'),
                    'comments': info.get('comment_count'),
                    'shares': info.get('repost_count'),
                    'duration': info.get('duration'),
                    'upload_date': info.get('upload_date'),
                    'description': info.get('description'),
                    'downloaded_at': datetime.now().isoformat(),
                    'url': url
                }

                print(f"✅ Video descargado: {info.get('title')}")
                print(f"   👤 Autor: {video_info['author']}")
                if video_info['views']:
                    print(f"   👁️  Vistas: {video_info['views']:,}")
                if video_info['likes']:
                    print(f"   ❤️  Likes: {video_info['likes']:,}")

                self.downloaded_videos.append(video_info)
                return video_info

        except Exception as e:
            print(f"❌ Error descargando {url}: {str(e)}")
            return None

    def search_and_download_by_hashtag(self, hashtag, count=10, min_views=100000):
        """
        Busca y descarga videos virales por hashtag

        Args:
            hashtag: Hashtag a buscar (sin #)
            count: Número de videos a descargar
            min_views: Mínimo de vistas para considerar viral
        """
        print(f"\n🔍 Buscando videos virales con #{hashtag}")
        print(f"   Buscando top {count} videos con más de {min_views:,} vistas...")

        # URL de búsqueda de TikTok por hashtag
        search_url = f"https://www.tiktok.com/tag/{hashtag}"

        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'skip_download': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"\n📡 Extrayendo videos del hashtag #{hashtag}...")
                result = ydl.extract_info(search_url, download=False)

                if result and 'entries' in result:
                    videos = []
                    for entry in result['entries']:
                        if entry.get('view_count', 0) >= min_views:
                            videos.append({
                                'url': entry.get('url') or entry.get('webpage_url'),
                                'views': entry.get('view_count', 0),
                                'likes': entry.get('like_count', 0),
                                'title': entry.get('title', 'Sin título')
                            })

                    # Ordenar por vistas (más virales primero)
                    videos = sorted(videos, key=lambda x: x['views'], reverse=True)
                    videos = videos[:count]

                    print(f"\n✅ Encontrados {len(videos)} videos virales")
                    print("\n📋 Lista de videos a descargar:")
                    for i, v in enumerate(videos, 1):
                        print(f"   {i}. {v['title'][:50]}... ({v['views']:,} vistas)")

                    # Descargar videos
                    for i, video in enumerate(videos, 1):
                        print(f"\n[{i}/{len(videos)}] Descargando...")
                        self.download_video(video['url'])
                        time.sleep(2)  # Pausa para no sobrecargar

                    self.save_summary()
                    return videos
                else:
                    print("❌ No se pudieron extraer videos. Intenta con otro método.")
                    return []

        except Exception as e:
            print(f"❌ Error en búsqueda: {str(e)}")
            print("\n💡 MÉTODO ALTERNATIVO:")
            self._show_manual_method(hashtag, count)
            return []

    def search_and_download_by_keyword(self, keyword, count=10, min_views=100000):
        """
        Busca y descarga videos virales por palabra clave

        Args:
            keyword: Palabra clave a buscar
            count: Número de videos a descargar
            min_views: Mínimo de vistas para considerar viral
        """
        print(f"\n🔍 Buscando videos virales: '{keyword}'")
        print(f"   Top {count} videos con más de {min_views:,} vistas...")

        # Buscar usando diferentes métodos
        search_url = f"https://www.tiktok.com/search?q={quote(keyword)}"

        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'skip_download': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"\n📡 Buscando '{keyword}' en TikTok...")
                result = ydl.extract_info(search_url, download=False)

                if result and 'entries' in result:
                    videos = []
                    for entry in result['entries']:
                        if entry.get('view_count', 0) >= min_views:
                            videos.append({
                                'url': entry.get('url') or entry.get('webpage_url'),
                                'views': entry.get('view_count', 0),
                                'likes': entry.get('like_count', 0),
                                'title': entry.get('title', 'Sin título')
                            })

                    videos = sorted(videos, key=lambda x: x['views'], reverse=True)
                    videos = videos[:count]

                    print(f"\n✅ Encontrados {len(videos)} videos virales")
                    for i, v in enumerate(videos, 1):
                        print(f"   {i}. {v['title'][:50]}... ({v['views']:,} vistas)")

                    for i, video in enumerate(videos, 1):
                        print(f"\n[{i}/{len(videos)}] Descargando...")
                        self.download_video(video['url'])
                        time.sleep(2)

                    self.save_summary()
                    return videos
                else:
                    print("❌ No se pudieron extraer videos.")
                    self._show_manual_method(keyword, count)
                    return []

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self._show_manual_method(keyword, count)
            return []

    def download_trending_today(self, count=20):
        """
        Descarga los videos más virales del día

        Args:
            count: Número de videos a descargar
        """
        print(f"\n🔥 Buscando los {count} videos MÁS VIRALES de hoy...")

        # Intentar diferentes hashtags trending
        trending_hashtags = [
            'fyp', 'foryou', 'viral', 'trending', 'foryoupage',
            'tiktok', 'parati', 'xyzbca', 'trend'
        ]

        print(f"\n📊 Buscando en hashtags trending: {', '.join(trending_hashtags[:5])}...")

        all_videos = []
        for hashtag in trending_hashtags[:3]:  # Buscar en los top 3
            print(f"\n🔍 Buscando en #{hashtag}...")
            videos = self.search_and_download_by_hashtag(hashtag, count=count//3, min_views=1000000)
            if videos:
                all_videos.extend(videos)
            time.sleep(3)

        if all_videos:
            print(f"\n✅ Total descargados: {len(all_videos)} videos virales")
            self.save_summary()
        else:
            print("\n❌ No se pudieron descargar videos automáticamente")
            self._show_manual_trending_method()

        return all_videos

    def _show_manual_method(self, search_term, count):
        """Muestra método manual alternativo"""
        print(f"\n{'='*60}")
        print("📱 MÉTODO MANUAL ALTERNATIVO:")
        print(f"{'='*60}")
        print(f"\n1. Ve a TikTok: https://www.tiktok.com/tag/{search_term}")
        print(f"2. Copia las URLs de los {count} videos más virales")
        print(f"3. Pégalas en un archivo 'urls.txt' (una por línea)")
        print(f"4. Ejecuta: python tiktok_downloader.py -f urls.txt")
        print(f"\n{'='*60}")

    def _show_manual_trending_method(self):
        """Muestra método manual para trending"""
        print(f"\n{'='*60}")
        print("📱 MÉTODO MANUAL PARA VIDEOS TRENDING:")
        print(f"{'='*60}")
        print("\n1. Ve a TikTok Discover: https://www.tiktok.com/discover")
        print("2. Busca en hashtags trending: #fyp #viral #foryou")
        print("3. Copia URLs de los videos más virales")
        print("4. Pégalas en 'trending_urls.txt'")
        print("5. Ejecuta: python tiktok_downloader.py -f trending_urls.txt")
        print(f"\n{'='*60}")

    def save_summary(self):
        """Guarda un resumen de los videos descargados"""
        if not self.downloaded_videos:
            return

        summary_file = os.path.join(
            self.output_dir,
            f'viral_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )

        # Estadísticas
        total_views = sum(v.get('views', 0) for v in self.downloaded_videos if v.get('views'))
        total_likes = sum(v.get('likes', 0) for v in self.downloaded_videos if v.get('likes'))

        summary = {
            'fecha_descarga': datetime.now().isoformat(),
            'total_videos': len(self.downloaded_videos),
            'estadisticas': {
                'total_vistas': total_views,
                'total_likes': total_likes,
                'promedio_vistas': total_views // len(self.downloaded_videos) if self.downloaded_videos else 0,
                'promedio_likes': total_likes // len(self.downloaded_videos) if self.downloaded_videos else 0
            },
            'videos': self.downloaded_videos
        }

        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"\n📊 RESUMEN DE DESCARGA:")
        print(f"   📁 Archivo: {summary_file}")
        print(f"   📹 Videos: {len(self.downloaded_videos)}")
        print(f"   👁️  Total vistas: {total_views:,}")
        print(f"   ❤️  Total likes: {total_likes:,}")


def main():
    parser = argparse.ArgumentParser(
        description='Busca y descarga automáticamente videos virales de TikTok',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🎯 EJEMPLOS DE USO:

  # Descargar top 20 videos virales de hoy
  python tiktok_auto_downloader.py --trending 20

  # Buscar por hashtag y descargar top 15
  python tiktok_auto_downloader.py --hashtag viral --count 15

  # Buscar por palabra clave
  python tiktok_auto_downloader.py --search "baile viral" --count 10

  # Con vistas mínimas personalizadas
  python tiktok_auto_downloader.py --hashtag fyp --count 20 --min-views 500000

  # Especificar carpeta de salida
  python tiktok_auto_downloader.py --trending 30 -o videos_virales_hoy
        """
    )

    parser.add_argument('--trending', type=int, metavar='N',
                        help='Descargar N videos más virales del día')
    parser.add_argument('--hashtag', type=str,
                        help='Buscar videos por hashtag (sin #)')
    parser.add_argument('--search', type=str,
                        help='Buscar videos por palabra clave')
    parser.add_argument('--count', type=int, default=10,
                        help='Número de videos a descargar (default: 10)')
    parser.add_argument('--min-views', type=int, default=100000,
                        help='Vistas mínimas para considerar viral (default: 100000)')
    parser.add_argument('-o', '--output', default='downloads',
                        help='Directorio de salida (default: downloads)')

    args = parser.parse_args()

    if not any([args.trending, args.hashtag, args.search]):
        parser.print_help()
        print("\n💡 TIP: Usa --trending 20 para empezar a descargar videos virales")
        sys.exit(1)

    downloader = TikTokAutoDownloader(output_dir=args.output)

    if args.trending:
        downloader.download_trending_today(count=args.trending)

    if args.hashtag:
        downloader.search_and_download_by_hashtag(
            args.hashtag,
            count=args.count,
            min_views=args.min_views
        )

    if args.search:
        downloader.search_and_download_by_keyword(
            args.search,
            count=args.count,
            min_views=args.min_views
        )


if __name__ == "__main__":
    main()
