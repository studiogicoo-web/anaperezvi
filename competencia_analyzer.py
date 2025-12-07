#!/usr/bin/env python3
"""
TikTok Competitor Analysis Tool
Analiza qué contenido viral funciona mejor en tu sector/competencia
"""
import sys
import os
import requests
import time
import json
from urllib.parse import quote
from datetime import datetime

class CompetitorAnalyzer:
    def __init__(self, output_dir="analisis_competencia"):
        self.output_dir = output_dir
        self.downloaded = 0
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def calculate_engagement_rate(self, video):
        """Calcula el engagement rate del video"""
        views = video.get('play_count', 0)
        if views == 0:
            return 0

        likes = video.get('digg_count', 0)
        comments = video.get('comment_count', 0)
        shares = video.get('share_count', 0)

        # Engagement rate = (likes + comments + shares) / views * 100
        engagement = ((likes + comments + shares) / views) * 100
        return round(engagement, 2)

    def analyze_sector(self, sector, count=30, min_views=50000):
        """Analiza videos virales de un sector y obtiene métricas"""
        print(f"\n{'='*80}")
        print(f"🔍 ANÁLISIS DE COMPETENCIA - {sector.upper()}")
        print(f"{'='*80}")
        print(f"📊 Buscando {count} videos con mínimo {min_views:,} vistas...")
        print(f"🎯 Analizando: engagement, comentarios, shares, tipo de contenido\n")

        videos = []

        # Buscar videos
        try:
            api_url = f"https://www.tikwm.com/api/feed/search?keywords={quote(sector)}&count=100&hd=1"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'Accept': 'application/json'
            }

            print("📡 Extrayendo videos de TikTok...")
            response = requests.get(api_url, headers=headers, timeout=20)
            data = response.json()

            if data.get('code') == 0 and data.get('data', {}).get('videos'):
                for item in data['data']['videos']:
                    views = item.get('play_count', 0)

                    if views >= min_views:
                        engagement_rate = self.calculate_engagement_rate(item)

                        video_info = {
                            'video_id': item.get('video_id'),
                            'title': item.get('title', 'Sin título'),
                            'author': item.get('author', {}).get('unique_id', 'user'),
                            'author_name': item.get('author', {}).get('nickname', 'Usuario'),
                            'url': f"https://www.tiktok.com/@{item.get('author', {}).get('unique_id', 'user')}/video/{item.get('video_id')}",
                            'views': views,
                            'likes': item.get('digg_count', 0),
                            'comments': item.get('comment_count', 0),
                            'shares': item.get('share_count', 0),
                            'saves': item.get('collect_count', 0),
                            'duration': item.get('duration', 0),
                            'engagement_rate': engagement_rate,
                            'music': item.get('music', ''),
                            'hashtags': item.get('hashtags', []),
                            'create_time': item.get('create_time', 0)
                        }

                        videos.append(video_info)

                print(f"✅ Encontrados {len(videos)} videos para analizar\n")
            else:
                print("⚠️  No se encontraron videos con esos criterios\n")

        except Exception as e:
            print(f"❌ Error en búsqueda: {e}\n")

        return videos

    def get_top_by_metric(self, videos, metric, count=10):
        """Obtiene los top videos por una métrica específica"""
        return sorted(videos, key=lambda x: x.get(metric, 0), reverse=True)[:count]

    def generate_insights(self, sector, videos):
        """Genera insights de marketing del análisis"""
        if not videos:
            return None

        print(f"\n{'='*80}")
        print(f"📊 GENERANDO INSIGHTS DE MARKETING")
        print(f"{'='*80}\n")

        # Calcular promedios
        total_videos = len(videos)
        avg_views = sum(v['views'] for v in videos) / total_videos
        avg_likes = sum(v['likes'] for v in videos) / total_videos
        avg_comments = sum(v['comments'] for v in videos) / total_videos
        avg_shares = sum(v['shares'] for v in videos) / total_videos
        avg_engagement = sum(v['engagement_rate'] for v in videos) / total_videos

        # Top videos por diferentes métricas
        top_engagement = self.get_top_by_metric(videos, 'engagement_rate', 10)
        top_comments = self.get_top_by_metric(videos, 'comments', 10)
        top_shares = self.get_top_by_metric(videos, 'shares', 10)
        top_saves = self.get_top_by_metric(videos, 'saves', 10)
        top_views = self.get_top_by_metric(videos, 'views', 10)

        insights = {
            'sector': sector,
            'fecha_analisis': datetime.now().isoformat(),
            'total_videos_analizados': total_videos,

            'promedios': {
                'vistas': int(avg_views),
                'likes': int(avg_likes),
                'comentarios': int(avg_comments),
                'shares': int(avg_shares),
                'engagement_rate': round(avg_engagement, 2)
            },

            'top_engagement': top_engagement,
            'top_comentarios': top_comments,
            'top_compartidos': top_shares,
            'top_guardados': top_saves,
            'top_vistas': top_views,

            'recomendaciones': self.generate_recommendations(videos)
        }

        return insights

    def generate_recommendations(self, videos):
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []

        # Encontrar patrones en títulos
        common_words = {}
        for v in videos[:20]:  # Top 20 por engagement
            words = v['title'].lower().split()
            for word in words:
                if len(word) > 3:
                    common_words[word] = common_words.get(word, 0) + 1

        top_words = sorted(common_words.items(), key=lambda x: x[1], reverse=True)[:10]

        # Análisis de duración
        durations = [v['duration'] for v in videos if v['duration'] > 0]
        avg_duration = sum(durations) / len(durations) if durations else 0

        # Videos con mejor engagement
        high_engagement = [v for v in videos if v['engagement_rate'] > 5]

        recommendations.append({
            'tipo': 'Duración óptima',
            'dato': f"{int(avg_duration)} segundos en promedio",
            'insight': f"Los videos exitosos en {videos[0].get('author', 'este sector')} duran aproximadamente {int(avg_duration)}s"
        })

        recommendations.append({
            'tipo': 'Palabras clave efectivas',
            'dato': [word for word, count in top_words[:5]],
            'insight': 'Estas palabras aparecen frecuentemente en videos virales del sector'
        })

        recommendations.append({
            'tipo': 'Engagement rate objetivo',
            'dato': f"{sum(v['engagement_rate'] for v in high_engagement) / len(high_engagement):.2f}%" if high_engagement else "5%+",
            'insight': 'Los videos más exitosos tienen este nivel de engagement'
        })

        # Análisis de comentarios
        high_comments = [v for v in videos if v['comments'] > 100]
        if high_comments:
            recommendations.append({
                'tipo': 'Videos que generan conversación',
                'dato': f"{len(high_comments)} videos con 100+ comentarios",
                'insight': 'Estos videos generan más interacción y debate'
            })

        return recommendations

    def print_analysis(self, insights):
        """Imprime el análisis de forma legible"""
        print(f"\n{'='*80}")
        print(f"📊 REPORTE DE ANÁLISIS - {insights['sector'].upper()}")
        print(f"{'='*80}")
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📹 Videos analizados: {insights['total_videos_analizados']}")

        print(f"\n{'─'*80}")
        print(f"📈 PROMEDIOS DEL SECTOR")
        print(f"{'─'*80}")
        print(f"  👁️  Vistas promedio:      {insights['promedios']['vistas']:,}")
        print(f"  ❤️  Likes promedio:       {insights['promedios']['likes']:,}")
        print(f"  💬 Comentarios promedio:  {insights['promedios']['comentarios']:,}")
        print(f"  🔄 Shares promedio:       {insights['promedios']['shares']:,}")
        print(f"  📊 Engagement rate:       {insights['promedios']['engagement_rate']}%")

        print(f"\n{'─'*80}")
        print(f"🏆 TOP 5 VIDEOS CON MEJOR ENGAGEMENT")
        print(f"{'─'*80}")
        for i, v in enumerate(insights['top_engagement'][:5], 1):
            print(f"\n{i}. {v['title'][:60]}")
            print(f"   👤 @{v['author']}")
            print(f"   📊 Engagement: {v['engagement_rate']}% | 👁️  {v['views']:,} | ❤️  {v['likes']:,} | 💬 {v['comments']:,} | 🔄 {v['shares']:,}")

        print(f"\n{'─'*80}")
        print(f"💬 TOP 5 VIDEOS MÁS COMENTADOS (Mayor interacción)")
        print(f"{'─'*80}")
        for i, v in enumerate(insights['top_comentarios'][:5], 1):
            print(f"\n{i}. {v['title'][:60]}")
            print(f"   👤 @{v['author']}")
            print(f"   💬 {v['comments']:,} comentarios | 👁️  {v['views']:,} vistas | 📊 {v['engagement_rate']}% engagement")

        print(f"\n{'─'*80}")
        print(f"🔄 TOP 5 VIDEOS MÁS COMPARTIDOS (Mayor viralidad)")
        print(f"{'─'*80}")
        for i, v in enumerate(insights['top_compartidos'][:5], 1):
            print(f"\n{i}. {v['title'][:60]}")
            print(f"   👤 @{v['author']}")
            print(f"   🔄 {v['shares']:,} shares | 👁️  {v['views']:,} vistas | 📊 {v['engagement_rate']}% engagement")

        print(f"\n{'─'*80}")
        print(f"💡 RECOMENDACIONES PARA TU CONTENIDO")
        print(f"{'─'*80}")
        for i, rec in enumerate(insights['recomendaciones'], 1):
            print(f"\n{i}. {rec['tipo'].upper()}")
            print(f"   ✓ {rec['insight']}")
            if isinstance(rec['dato'], list):
                print(f"   📝 Palabras clave: {', '.join(rec['dato'])}")
            else:
                print(f"   📊 {rec['dato']}")

        print(f"\n{'='*80}\n")

    def download_top_videos(self, videos, count=10, metric='engagement_rate'):
        """Descarga los mejores videos según una métrica"""
        print(f"\n{'='*80}")
        print(f"⬇️  DESCARGANDO TOP {count} VIDEOS POR {metric.upper()}")
        print(f"{'='*80}\n")

        top_videos = self.get_top_by_metric(videos, metric, count)

        for i, video in enumerate(top_videos, 1):
            print(f"\n[{i}/{len(top_videos)}] Descargando video {i}...")
            self.download_video(video)

            if i < len(top_videos):
                print(f"\n   ⏳ Esperando 2 segundos...")
                time.sleep(2)

        print(f"\n{'='*80}")
        print(f"✅ DESCARGA COMPLETADA")
        print(f"📊 Videos descargados: {self.downloaded}/{count}")
        print(f"📁 Ubicación: {os.path.abspath(self.output_dir)}/")
        print(f"{'='*80}\n")

    def download_video(self, video_info):
        """Descarga un video"""
        url = video_info['url']

        try:
            api_url = f"https://www.tikwm.com/api/?url={quote(url)}&hd=1"
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

            response = requests.get(api_url, headers=headers, timeout=15)
            data = response.json()

            if data.get('code') == 0 and data.get('data'):
                video_data = data['data']
                video_url = video_data.get('hdplay') or video_data.get('play')

                if video_url:
                    print(f"   📝 {video_info['title'][:50]}")
                    print(f"   👤 @{video_info['author']}")
                    print(f"   📊 Engagement: {video_info['engagement_rate']}% | 💬 {video_info['comments']:,} comentarios | 🔄 {video_info['shares']:,} shares")
                    print(f"   ⬇️  Descargando...")

                    video_response = requests.get(video_url, headers=headers, stream=True, timeout=30)

                    # Nombre de archivo con métricas
                    filename = f"{self.output_dir}/{self.downloaded+1}_eng{video_info['engagement_rate']}_@{video_info['author']}.mp4"
                    filename = filename.replace('/', '_').replace('?', '').replace(':', '')

                    with open(filename, 'wb') as f:
                        for chunk in video_response.iter_content(8192):
                            if chunk:
                                f.write(chunk)

                    print(f"   ✅ Guardado!")
                    self.downloaded += 1
                    return True

            print(f"   ❌ No disponible")
            return False

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def save_report(self, insights):
        """Guarda el reporte en JSON y TXT"""
        timestamp = int(time.time())

        # JSON completo
        json_file = f"{self.output_dir}/analisis_{insights['sector']}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(insights, f, indent=2, ensure_ascii=False)

        # TXT legible
        txt_file = f"{self.output_dir}/reporte_{insights['sector']}_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"REPORTE DE ANÁLISIS - {insights['sector'].upper()}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Videos analizados: {insights['total_videos_analizados']}\n\n")

            f.write(f"PROMEDIOS DEL SECTOR\n")
            f.write(f"{'-'*80}\n")
            f.write(f"Vistas promedio:      {insights['promedios']['vistas']:,}\n")
            f.write(f"Likes promedio:       {insights['promedios']['likes']:,}\n")
            f.write(f"Comentarios promedio: {insights['promedios']['comentarios']:,}\n")
            f.write(f"Shares promedio:      {insights['promedios']['shares']:,}\n")
            f.write(f"Engagement rate:      {insights['promedios']['engagement_rate']}%\n\n")

            f.write(f"TOP 10 VIDEOS CON MEJOR ENGAGEMENT\n")
            f.write(f"{'-'*80}\n")
            for i, v in enumerate(insights['top_engagement'][:10], 1):
                f.write(f"\n{i}. {v['title']}\n")
                f.write(f"   @{v['author']}\n")
                f.write(f"   Engagement: {v['engagement_rate']}% | Vistas: {v['views']:,} | Comentarios: {v['comments']:,}\n")
                f.write(f"   URL: {v['url']}\n")

        print(f"\n📄 Reportes guardados:")
        print(f"   JSON: {json_file}")
        print(f"   TXT:  {txt_file}")

def main():
    if len(sys.argv) < 2:
        print("\n🎯 USO:")
        print("  python3 competencia_analyzer.py SECTOR [CANTIDAD] [MIN_VISTAS]")
        print("\n📝 EJEMPLOS:")
        print("  python3 competencia_analyzer.py fitness")
        print("  python3 competencia_analyzer.py crossfit 50")
        print("  python3 competencia_analyzer.py 'gym motivation' 30 100000")
        print("  python3 competencia_analyzer.py cafeteria 40")
        print("  python3 competencia_analyzer.py restaurante 25")
        print("\n💡 SECTORES SUGERIDOS:")
        print("   fitness, crossfit, gym, cafeteria, restaurante, cocina")
        print("   marketing, emprendimiento, industria, construccion, etc.")
        print("\n📊 QUÉ HACE:")
        print("   ✓ Analiza qué contenido funciona mejor en tu sector")
        print("   ✓ Identifica videos con más engagement, comentarios, shares")
        print("   ✓ Genera insights y recomendaciones para tu contenido")
        print("   ✓ Descarga los mejores videos de la competencia")
        sys.exit(0)

    sector = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    min_views = int(sys.argv[3]) if len(sys.argv) > 3 else 50000

    analyzer = CompetitorAnalyzer()

    # Analizar sector
    videos = analyzer.analyze_sector(sector, count, min_views)

    if not videos:
        print("\n❌ No se encontraron suficientes videos para analizar")
        print("\n💡 INTENTA:")
        print("   - Reducir el mínimo de vistas")
        print("   - Usar términos en inglés")
        print("   - Probar con otros términos relacionados")
        sys.exit(1)

    # Generar insights
    insights = analyzer.generate_insights(sector, videos)

    # Mostrar análisis
    analyzer.print_analysis(insights)

    # Guardar reporte
    analyzer.save_report(insights)

    # Preguntar si quiere descargar videos
    print(f"\n{'='*80}")
    print(f"⬇️  OPCIONES DE DESCARGA")
    print(f"{'='*80}")
    print(f"1. Descargar top 10 por ENGAGEMENT (contenido más efectivo)")
    print(f"2. Descargar top 10 por COMENTARIOS (contenido que genera conversación)")
    print(f"3. Descargar top 10 por SHARES (contenido más viral)")
    print(f"4. Descargar top 10 por VISTAS (contenido más visto)")
    print(f"5. No descargar videos\n")

    try:
        choice = input("Elige una opción (1-5): ").strip()

        if choice == '1':
            analyzer.download_top_videos(videos, 10, 'engagement_rate')
        elif choice == '2':
            analyzer.download_top_videos(videos, 10, 'comments')
        elif choice == '3':
            analyzer.download_top_videos(videos, 10, 'shares')
        elif choice == '4':
            analyzer.download_top_videos(videos, 10, 'views')
        else:
            print("\n✅ Análisis completado sin descargar videos")

    except KeyboardInterrupt:
        print("\n\n✅ Análisis completado")

if __name__ == "__main__":
    main()
