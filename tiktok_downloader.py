#!/usr/bin/env python3
"""
TikTok Viral Video Downloader
Descarga videos virales de TikTok usando yt-dlp
"""

import os
import sys
import json
import argparse
from datetime import datetime
import yt_dlp


class TikTokDownloader:
    def __init__(self, output_dir="downloads"):
        """
        Inicializa el descargador de TikTok

        Args:
            output_dir: Directorio donde se guardarán los videos
        """
        self.output_dir = output_dir
        self.create_output_dir()

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
                print(f"   👁️  Vistas: {video_info['views']:,}" if video_info['views'] else "")
                print(f"   ❤️  Likes: {video_info['likes']:,}" if video_info['likes'] else "")

                return video_info

        except Exception as e:
            print(f"❌ Error descargando {url}: {str(e)}")
            return None

    def download_from_file(self, file_path, include_metadata=True):
        """
        Descarga múltiples videos desde un archivo de texto

        Args:
            file_path: Ruta al archivo con URLs (una por línea)
            include_metadata: Si es True, guarda también los metadatos

        Returns:
            list: Lista de información de videos descargados
        """
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            return []

        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        print(f"\n📋 Encontradas {len(urls)} URLs para descargar")

        results = []
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Procesando...")
            result = self.download_video(url, include_metadata)
            if result:
                results.append(result)

        # Guardar resumen
        self.save_summary(results)

        return results

    def download_trending(self, hashtag=None, count=10):
        """
        Descarga videos de tendencia (requiere implementación con API)

        Args:
            hashtag: Hashtag específico para buscar
            count: Número de videos a descargar
        """
        print("⚠️  Función de tendencias requiere API de TikTok")
        print("💡 Por ahora, usa download_from_file() con una lista de URLs")

    def save_summary(self, results):
        """
        Guarda un resumen de los videos descargados

        Args:
            results: Lista de información de videos
        """
        summary_file = os.path.join(self.output_dir, f'summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')

        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n📊 Resumen guardado en: {summary_file}")
        print(f"   Total descargados: {len(results)} videos")


def main():
    parser = argparse.ArgumentParser(
        description='Descarga videos virales de TikTok',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Descargar un solo video
  python tiktok_downloader.py -u https://www.tiktok.com/@user/video/123456789

  # Descargar desde un archivo de URLs
  python tiktok_downloader.py -f urls.txt

  # Especificar directorio de salida
  python tiktok_downloader.py -f urls.txt -o mis_videos

  # Sin metadatos
  python tiktok_downloader.py -u URL --no-metadata
        """
    )

    parser.add_argument('-u', '--url', help='URL del video de TikTok')
    parser.add_argument('-f', '--file', help='Archivo con URLs de TikTok (una por línea)')
    parser.add_argument('-o', '--output', default='downloads', help='Directorio de salida (default: downloads)')
    parser.add_argument('--no-metadata', action='store_true', help='No guardar metadatos')

    args = parser.parse_args()

    if not args.url and not args.file:
        parser.print_help()
        sys.exit(1)

    downloader = TikTokDownloader(output_dir=args.output)

    if args.url:
        downloader.download_video(args.url, include_metadata=not args.no_metadata)

    if args.file:
        downloader.download_from_file(args.file, include_metadata=not args.no_metadata)


if __name__ == "__main__":
    main()
