# 🎵 TikTok Auto Viral Video Downloader

**Programa en Python que BUSCA y DESCARGA AUTOMÁTICAMENTE videos virales de TikTok** 🔥

## 🚀 ¿Qué hace este programa?

✅ **BUSCA automáticamente** videos virales en TikTok
✅ **DESCARGA** los videos más populares sin intervención manual
✅ Busca por hashtags trending (#fyp, #viral, #foryou)
✅ Busca por palabras clave
✅ Extrae los videos más virales del día
✅ Guarda metadatos (vistas, likes, comentarios)
✅ Genera reportes con estadísticas

---

## 📋 INSTALACIÓN RÁPIDA

### 1. Instalar Python
- Descarga Python 3.7+ desde: https://www.python.org/downloads/

### 2. Instalar dependencias
```bash
pip install yt-dlp requests
```

¡Listo! Ya puedes usar el programa.

---

## 💻 USO SÚPER FÁCIL

### 🔥 OPCIÓN 1: Descargar videos virales de HOY (automático)

```bash
python tiktok_auto_downloader.py --trending 20
```

**Esto descargará los 20 videos MÁS VIRALES del día automáticamente.**

---

### 🎯 OPCIÓN 2: Buscar por HASHTAG

```bash
# Buscar videos virales con #viral
python tiktok_auto_downloader.py --hashtag viral --count 15

# Buscar con #fyp
python tiktok_auto_downloader.py --hashtag fyp --count 20

# Buscar con #parati
python tiktok_auto_downloader.py --hashtag parati --count 10
```

---

### 🔍 OPCIÓN 3: Buscar por PALABRA CLAVE

```bash
# Buscar "baile viral"
python tiktok_auto_downloader.py --search "baile viral" --count 10

# Buscar "comedia"
python tiktok_auto_downloader.py --search "comedia" --count 15

# Buscar "recetas"
python tiktok_auto_downloader.py --search "recetas" --count 10
```

---

### ⚙️ OPCIONES PERSONALIZADAS

```bash
# Solo videos con más de 500,000 vistas
python tiktok_auto_downloader.py --hashtag viral --count 20 --min-views 500000

# Guardar en carpeta específica
python tiktok_auto_downloader.py --trending 30 -o mis_videos_virales

# Solo videos MUY virales (1+ millón de vistas)
python tiktok_auto_downloader.py --hashtag fyp --count 50 --min-views 1000000
```

---

## 🛠️ MÉTODO ALTERNATIVO (2 Pasos)

Si el método automático no funciona, usa este proceso en 2 pasos:

### PASO 1: Extraer URLs de videos virales

```bash
# Extraer de hashtags trending
python tiktok_scraper.py --trending --max 30

# Extraer de un hashtag específico
python tiktok_scraper.py --hashtag viral --max 50
```

Esto creará un archivo `trending_urls.txt` con las URLs.

### PASO 2: Descargar los videos

```bash
python tiktok_downloader.py -f trending_urls.txt
```

---

## 📂 ¿Dónde se guardan los videos?

Los videos se guardan en la carpeta `downloads/` (o la que especifiques):

```
downloads/
├── 7123456789_baile_viral.mp4           # Video
├── 7123456789_baile_viral.jpg           # Miniatura
├── 7123456789_baile_viral.info.json     # Metadatos
└── viral_summary_20251207_143000.json   # Resumen con estadísticas
```

---

## 📊 Resumen de estadísticas

El programa genera un archivo JSON con:

```json
{
  "total_videos": 20,
  "estadisticas": {
    "total_vistas": 50000000,
    "total_likes": 10000000,
    "promedio_vistas": 2500000,
    "promedio_likes": 500000
  },
  "videos": [...]
}
```

---

## 🎯 EJEMPLOS DE USO REAL

### Caso 1: Investigar tendencias de baile
```bash
python tiktok_auto_downloader.py --search "baile 2025" --count 30 -o bailes_virales
```

### Caso 2: Descargar challenges populares
```bash
python tiktok_auto_downloader.py --hashtag challenge --count 25 --min-views 200000
```

### Caso 3: Análisis de contenido viral diario
```bash
python tiktok_auto_downloader.py --trending 50 -o analisis_diario
```

### Caso 4: Recopilar videos de un nicho específico
```bash
python tiktok_auto_downloader.py --search "marketing digital" --count 20
```

---

## 🔧 COMANDOS DISPONIBLES

### tiktok_auto_downloader.py (Descarga automática)

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `--trending N` | Descarga N videos virales del día | `--trending 20` |
| `--hashtag TAG` | Busca por hashtag | `--hashtag viral` |
| `--search "TEXTO"` | Busca por palabra clave | `--search "comedia"` |
| `--count N` | Número de videos a descargar | `--count 30` |
| `--min-views N` | Vistas mínimas | `--min-views 500000` |
| `-o DIR` | Carpeta de salida | `-o mis_videos` |

### tiktok_scraper.py (Extractor de URLs)

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `--trending` | Extrae de hashtags trending | `--trending` |
| `--hashtag TAG` | Extrae de un hashtag | `--hashtag viral` |
| `--max N` | Máximo de URLs | `--max 50` |
| `-o FILE` | Archivo de salida | `-o urls.txt` |
| `--json` | Guardar también en JSON | `--json` |

### tiktok_downloader.py (Descarga manual)

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `-u URL` | Descarga un video | `-u https://...` |
| `-f FILE` | Descarga desde archivo | `-f urls.txt` |
| `-o DIR` | Directorio de salida | `-o videos` |
| `--no-metadata` | Sin metadatos | `--no-metadata` |

---

## 🐛 Solución de problemas

### ❌ "No se pudieron extraer videos"

**Solución:** Usa el método en 2 pasos (scraper + downloader)

### ❌ "Unable to download video"

**Causas posibles:**
- Video privado o eliminado
- Límite de descarga de TikTok

**Solución:** Espera unos minutos e intenta de nuevo

### ❌ "python no se reconoce"

**Solución:** Instala Python desde python.org

---

## 💡 TIPS Y TRUCOS

1. **Para videos MUY virales:** Usa `--min-views 1000000`
2. **Para descargar muchos videos:** Hazlo en lotes de 20-30
3. **Organiza por categorías:** Usa `-o` para crear carpetas separadas
4. **Espera entre descargas:** El programa ya tiene delays automáticos

---

## ⚠️ NOTAS IMPORTANTES

- **Uso educativo/personal:** Respeta los derechos de autor
- **No redistribuyas** contenido sin permiso
- **Respeta los términos** de servicio de TikTok
- **Créditos:** Menciona a los creadores originales

---

## 🎬 Casos de uso

### Para creadores de contenido
- 📊 Analizar tendencias para crear contenido similar
- 🎨 Inspiración para nuevos videos
- 📈 Estudiar qué funciona y qué no

### Para marketers
- 🔍 Investigación de mercado
- 📊 Análisis de competencia
- 💡 Ideas para campañas

### Para investigadores
- 📚 Estudios de viralidad
- 📊 Análisis de redes sociales
- 🎓 Investigación académica

---

## 📞 Soporte

Si tienes problemas:

1. Verifica que Python esté instalado: `python --version`
2. Verifica las dependencias: `pip list`
3. Actualiza yt-dlp: `pip install -U yt-dlp`

---

## 🚀 INICIO RÁPIDO (Resumen)

```bash
# 1. Instalar
pip install yt-dlp requests

# 2. Descargar videos virales de hoy
python tiktok_auto_downloader.py --trending 20

# ¡Listo! Los videos estarán en la carpeta downloads/
```

---

**🎉 ¡Disfruta descargando videos virales automáticamente!**

**Hecho con ❤️ para la comunidad de TikTok**
