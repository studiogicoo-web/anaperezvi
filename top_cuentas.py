#!/usr/bin/env python3
"""
TikTok Top Accounts Finder
Encuentra las cuentas más seguidas de un sector específico
"""
import sys
import os
import requests
import json
import time
from urllib.parse import quote
from datetime import datetime

class TopAccountsFinder:
    def __init__(self):
        self.output_dir = "top_cuentas"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def search_accounts(self, sector, min_followers=10000):
        """Busca cuentas en un sector específico"""
        print(f"\n{'='*80}")
        print(f"🔍 BUSCANDO CUENTAS TOP - {sector.upper()}")
        print(f"{'='*80}")
        print(f"📊 Mínimo de seguidores: {min_followers:,}")
        print(f"🎯 Buscando cuentas relevantes...\n")

        accounts = []
        seen_users = set()

        # Método 1: Buscar a través de videos del sector
        try:
            print("📡 Extrayendo cuentas de videos populares...")
            api_url = f"https://www.tikwm.com/api/feed/search?keywords={quote(sector)}&count=100"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'Accept': 'application/json'
            }

            response = requests.get(api_url, headers=headers, timeout=20)
            data = response.json()

            if data.get('code') == 0 and data.get('data', {}).get('videos'):
                for item in data['data']['videos']:
                    author_info = item.get('author', {})
                    unique_id = author_info.get('unique_id')

                    if unique_id and unique_id not in seen_users:
                        seen_users.add(unique_id)

                        follower_count = author_info.get('follower_count', 0)

                        if follower_count >= min_followers:
                            account = {
                                'username': unique_id,
                                'nickname': author_info.get('nickname', 'Usuario'),
                                'followers': follower_count,
                                'following': author_info.get('following_count', 0),
                                'total_likes': author_info.get('total_favorited', 0),
                                'video_count': author_info.get('video_count', 0),
                                'verified': author_info.get('verified', False),
                                'bio': author_info.get('signature', ''),
                                'url': f"https://www.tiktok.com/@{unique_id}",
                            }

                            # Calcular engagement rate estimado
                            if account['followers'] > 0 and account['video_count'] > 0:
                                avg_likes_per_video = account['total_likes'] / account['video_count']
                                engagement_rate = (avg_likes_per_video / account['followers']) * 100
                                account['engagement_rate'] = round(engagement_rate, 2)
                            else:
                                account['engagement_rate'] = 0

                            accounts.append(account)

                print(f"✅ Encontradas {len(accounts)} cuentas relevantes\n")
            else:
                print("⚠️  No se encontraron cuentas en este sector\n")

        except Exception as e:
            print(f"❌ Error en búsqueda: {e}\n")

        # Ordenar por seguidores
        accounts = sorted(accounts, key=lambda x: x['followers'], reverse=True)

        return accounts

    def show_top_accounts(self, sector, accounts):
        """Muestra las cuentas top del sector"""
        if not accounts:
            print("❌ No se encontraron cuentas")
            return

        print(f"\n{'='*80}")
        print(f"👥 TOP CUENTAS - {sector.upper()}")
        print(f"{'='*80}")
        print(f"📊 Total de cuentas encontradas: {len(accounts)}\n")

        # Estadísticas generales
        total_followers = sum(a['followers'] for a in accounts)
        avg_followers = total_followers // len(accounts) if accounts else 0
        avg_engagement = sum(a['engagement_rate'] for a in accounts) / len(accounts) if accounts else 0

        print(f"📈 ESTADÍSTICAS GENERALES:")
        print(f"   Total seguidores combinados: {total_followers:,}")
        print(f"   Promedio de seguidores: {avg_followers:,}")
        print(f"   Engagement rate promedio: {avg_engagement:.2f}%\n")

        # Top 20 cuentas
        print(f"{'─'*80}")
        print(f"🏆 TOP 20 CUENTAS MÁS SEGUIDAS")
        print(f"{'─'*80}\n")

        for i, account in enumerate(accounts[:20], 1):
            verified = "✓" if account['verified'] else ""
            print(f"{i:2}. @{account['username']} {verified}")
            print(f"    {account['nickname']}")
            print(f"    👥 {account['followers']:,} seguidores | 📹 {account['video_count']:,} videos | ❤️  {account['total_likes']:,} likes totales")
            print(f"    📊 Engagement: {account['engagement_rate']}%")
            if account['bio']:
                print(f"    📝 {account['bio'][:60]}...")
            print(f"    🔗 {account['url']}\n")

        # Top por engagement
        top_engagement = sorted(accounts, key=lambda x: x['engagement_rate'], reverse=True)[:10]

        print(f"{'─'*80}")
        print(f"🔥 TOP 10 MEJOR ENGAGEMENT (Más activa la audiencia)")
        print(f"{'─'*80}\n")

        for i, account in enumerate(top_engagement, 1):
            print(f"{i:2}. @{account['username']}")
            print(f"    📊 Engagement: {account['engagement_rate']}% | 👥 {account['followers']:,} seguidores")
            print(f"    🔗 {account['url']}\n")

        # Cuentas verificadas
        verified_accounts = [a for a in accounts if a['verified']]
        if verified_accounts:
            print(f"{'─'*80}")
            print(f"✓ CUENTAS VERIFICADAS ({len(verified_accounts)})")
            print(f"{'─'*80}\n")

            for account in verified_accounts[:10]:
                print(f"   @{account['username']} - {account['followers']:,} seguidores")

        print(f"\n{'='*80}\n")

    def save_report(self, sector, accounts):
        """Guarda el reporte de cuentas"""
        if not accounts:
            return

        timestamp = int(time.time())

        # JSON completo
        json_file = f"{self.output_dir}/top_cuentas_{sector}_{timestamp}.json"
        report_data = {
            'sector': sector,
            'fecha_analisis': datetime.now().isoformat(),
            'total_cuentas': len(accounts),
            'estadisticas': {
                'total_seguidores': sum(a['followers'] for a in accounts),
                'promedio_seguidores': sum(a['followers'] for a in accounts) // len(accounts),
                'promedio_engagement': sum(a['engagement_rate'] for a in accounts) / len(accounts),
                'cuentas_verificadas': len([a for a in accounts if a['verified']])
            },
            'cuentas': accounts
        }

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        # TXT legible
        txt_file = f"{self.output_dir}/top_cuentas_{sector}_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"TOP CUENTAS DE TIKTOK - {sector.upper()}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total cuentas: {len(accounts)}\n\n")

            f.write(f"TOP 20 CUENTAS MÁS SEGUIDAS:\n")
            f.write(f"{'-'*80}\n\n")

            for i, account in enumerate(accounts[:20], 1):
                f.write(f"{i}. @{account['username']}\n")
                f.write(f"   Nombre: {account['nickname']}\n")
                f.write(f"   Seguidores: {account['followers']:,}\n")
                f.write(f"   Videos: {account['video_count']:,}\n")
                f.write(f"   Likes totales: {account['total_likes']:,}\n")
                f.write(f"   Engagement: {account['engagement_rate']}%\n")
                f.write(f"   URL: {account['url']}\n\n")

        print(f"📄 Reportes guardados:")
        print(f"   JSON: {json_file}")
        print(f"   TXT:  {txt_file}\n")

    def show_recommendations(self, accounts):
        """Muestra recomendaciones basadas en el análisis"""
        if not accounts:
            return

        print(f"{'='*80}")
        print(f"💡 RECOMENDACIONES PARA TU ESTRATEGIA")
        print(f"{'='*80}\n")

        # Analizar engagement
        high_engagement = [a for a in accounts if a['engagement_rate'] > 5]

        print(f"1. CUENTAS A SEGUIR COMO REFERENCIA:")
        print(f"   → Top 5 con mejor engagement (audiencia más activa)\n")
        top_eng = sorted(accounts, key=lambda x: x['engagement_rate'], reverse=True)[:5]
        for acc in top_eng:
            print(f"      @{acc['username']} - {acc['engagement_rate']}% engagement")

        print(f"\n2. BENCHMARK DE CONTENIDO:")
        avg_videos = sum(a['video_count'] for a in accounts[:10]) / 10
        print(f"   → Las top 10 cuentas tienen promedio de {int(avg_videos):,} videos")
        print(f"   → Esto indica consistencia en publicaciones\n")

        print(f"3. COLABORACIONES POTENCIALES:")
        mid_tier = [a for a in accounts if 10000 <= a['followers'] <= 100000]
        if mid_tier:
            print(f"   → Encontradas {len(mid_tier)} cuentas mid-tier (10k-100k seguidores)")
            print(f"   → Estas son ideales para colaboraciones accesibles\n")

        print(f"4. NICHOS ESPECÍFICOS:")
        print(f"   → Revisa las biografías de las top cuentas")
        print(f"   → Identifica sub-nichos específicos dentro de {accounts[0].get('sector', 'este sector')}\n")

        print(f"{'='*80}\n")

def main():
    if len(sys.argv) < 2:
        print("\n🎯 USO:")
        print("  python3 top_cuentas.py SECTOR [MIN_SEGUIDORES]")
        print("\n📝 EJEMPLOS:")
        print("  python3 top_cuentas.py barista")
        print("  python3 top_cuentas.py 'coffee shop'")
        print("  python3 top_cuentas.py cafeteria")
        print("  python3 top_cuentas.py fitness 50000")
        print("  python3 top_cuentas.py crossfit")
        print("  python3 top_cuentas.py 'functional training'")
        print("  python3 top_cuentas.py restaurante")
        print("  python3 top_cuentas.py gastronomia")
        print("\n💡 SECTORES SUGERIDOS:")
        print("   barista, coffee shop, cafeteria, fitness, crossfit")
        print("   restaurante, chef, cocina, gym, yoga, etc.")
        print("\n📊 QUÉ HACE:")
        print("   ✓ Encuentra las cuentas más seguidas del sector")
        print("   ✓ Muestra engagement rate de cada cuenta")
        print("   ✓ Identifica cuentas verificadas")
        print("   ✓ Genera reporte con estadísticas")
        print("   ✓ Da recomendaciones para tu estrategia")
        sys.exit(0)

    sector = sys.argv[1]
    min_followers = int(sys.argv[2]) if len(sys.argv) > 2 else 10000

    finder = TopAccountsFinder()

    # Buscar cuentas
    accounts = finder.search_accounts(sector, min_followers)

    if not accounts:
        print("\n❌ No se encontraron cuentas en este sector")
        print("\n💡 INTENTA:")
        print("   - Reducir el mínimo de seguidores")
        print("   - Usar términos en inglés")
        print("   - Probar con palabras clave relacionadas")
        sys.exit(1)

    # Mostrar resultados
    finder.show_top_accounts(sector, accounts)

    # Mostrar recomendaciones
    finder.show_recommendations(accounts)

    # Guardar reporte
    finder.save_report(sector, accounts)

    print(f"✅ Análisis completado!")
    print(f"📁 Reportes guardados en: {os.path.abspath(finder.output_dir)}/\n")

if __name__ == "__main__":
    main()
