# 🚀 GUÍA RÁPIDA - TikTok Auto Downloader

## ⚡ INSTALACIÓN (1 minuto)

```bash
pip install yt-dlp requests
```

---

## 🎯 USO BÁSICO

### Descargar videos virales de HOY
```bash
python tiktok_auto_downloader.py --trending 20
```

### Buscar por hashtag
```bash
python tiktok_auto_downloader.py --hashtag viral --count 15
```

### Buscar por palabra clave
```bash
python tiktok_auto_downloader.py --search "baile" --count 10
```

---

## 📂 ARCHIVOS

- `tiktok_auto_downloader.py` → Descarga automática (RECOMENDADO)
- `tiktok_scraper.py` → Extrae solo las URLs
- `tiktok_downloader.py` → Descarga manual desde URLs

---

## 🔥 COMANDO MÁS USADO

```bash
# Descargar 30 videos virales del día
python tiktok_auto_downloader.py --trending 30
```

---

## 📊 EJEMPLOS

```bash
# Solo videos con +500k vistas
python tiktok_auto_downloader.py --hashtag fyp --count 20 --min-views 500000

# Guardar en carpeta específica
python tiktok_auto_downloader.py --trending 25 -o mis_videos

# Buscar nicho específico
python tiktok_auto_downloader.py --search "comedia" --count 15
```

---

## 💡 TIP

Los videos se guardan en `downloads/` con:
- ✅ Video MP4
- ✅ Miniatura JPG
- ✅ Metadatos JSON (vistas, likes, etc.)

---

¡Listo! Así de fácil. 🎉
