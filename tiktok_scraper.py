#!/usr/bin/env python3
"""
TikTok Trending Scraper
Extrae URLs de videos trending de TikTok y las guarda en un archivo
"""

import os
import sys
import json
import argparse
from datetime import datetime
import yt_dlp


class TikTokScraper:
    """Scraper para obtener URLs de videos trending de TikTok"""

    def __init__(self):
        self.videos = []

    def scrape_hashtag(self, hashtag, max_videos=50):
        """
        Extrae URLs de videos de un hashtag

        Args:
            hashtag: Hashtag a buscar (sin #)
            max_videos: Máximo de videos a extraer
        """
        print(f"\n🔍 Extrayendo URLs del hashtag #{hashtag}...")

        url = f"https://www.tiktok.com/tag/{hashtag}"

        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'skip_download': True,
            'playlist_items': f'1-{max_videos}',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=False)

                if result and 'entries' in result:
                    for entry in result['entries'][:max_videos]:
                        video_url = entry.get('url') or entry.get('webpage_url')
                        if video_url and 'tiktok.com' in video_url:
                            self.videos.append({
                                'url': video_url,
                                'title': entry.get('title', 'Sin título'),
                                'views': entry.get('view_count', 0),
                                'likes': entry.get('like_count', 0),
                                'author': entry.get('uploader', 'Desconocido')
                            })

                    print(f"✅ Extraídas {len(self.videos)} URLs")
                else:
                    print("❌ No se pudieron extraer videos")

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("\n💡 Intenta acceder manualmente a:")
            print(f"   https://www.tiktok.com/tag/{hashtag}")

    def scrape_trending_hashtags(self, max_videos=20):
        """Extrae videos de múltiples hashtags trending"""

        trending = ['fyp', 'viral', 'foryou', 'trending', 'parati']

        print(f"\n🔥 Extrayendo videos de hashtags trending...")
        print(f"   Hashtags: {', '.join(trending)}\n")

        for hashtag in trending:
            print(f"\n📌 Procesando #{hashtag}...")
            self.scrape_hashtag(hashtag, max_videos=max_videos//len(trending))

    def save_urls(self, filename='trending_urls.txt'):
        """Guarda las URLs en un archivo de texto"""

        if not self.videos:
            print("❌ No hay URLs para guardar")
            return

        # Ordenar por vistas (más virales primero)
        sorted_videos = sorted(self.videos, key=lambda x: x['views'], reverse=True)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Videos virales de TikTok - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total: {len(sorted_videos)} videos\n\n")

            for i, video in enumerate(sorted_videos, 1):
                f.write(f"# {i}. {video['title'][:60]}\n")
                f.write(f"#    👤 {video['author']} | 👁️  {video['views']:,} vistas | ❤️  {video['likes']:,} likes\n")
                f.write(f"{video['url']}\n\n")

        print(f"\n✅ URLs guardadas en: {filename}")
        print(f"   Total: {len(sorted_videos)} videos")
        print(f"\n💡 Ahora ejecuta:")
        print(f"   python tiktok_downloader.py -f {filename}")

    def save_json(self, filename='trending_videos.json'):
        """Guarda la información en formato JSON"""

        if not self.videos:
            return

        data = {
            'fecha_extraccion': datetime.now().isoformat(),
            'total_videos': len(self.videos),
            'videos': sorted(self.videos, key=lambda x: x['views'], reverse=True)
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ JSON guardado en: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Extrae URLs de videos virales de TikTok',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EJEMPLOS:

  # Extraer videos trending generales
  python tiktok_scraper.py --trending

  # Extraer de un hashtag específico
  python tiktok_scraper.py --hashtag viral --max 30

  # Especificar archivo de salida
  python tiktok_scraper.py --trending -o mis_urls.txt
        """
    )

    parser.add_argument('--trending', action='store_true',
                        help='Extraer de hashtags trending populares')
    parser.add_argument('--hashtag', type=str,
                        help='Extraer de un hashtag específico')
    parser.add_argument('--max', type=int, default=20,
                        help='Máximo de videos a extraer (default: 20)')
    parser.add_argument('-o', '--output', default='trending_urls.txt',
                        help='Archivo de salida (default: trending_urls.txt)')
    parser.add_argument('--json', action='store_true',
                        help='También guardar en formato JSON')

    args = parser.parse_args()

    if not args.trending and not args.hashtag:
        parser.print_help()
        sys.exit(1)

    scraper = TikTokScraper()

    if args.trending:
        scraper.scrape_trending_hashtags(max_videos=args.max)

    if args.hashtag:
        scraper.scrape_hashtag(args.hashtag, max_videos=args.max)

    scraper.save_urls(args.output)

    if args.json:
        json_file = args.output.replace('.txt', '.json')
        scraper.save_json(json_file)


if __name__ == "__main__":
    main()
