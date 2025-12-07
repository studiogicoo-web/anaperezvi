# 🎵 TikTok Viral Video Downloader

Programa en Python para descargar videos virales de TikTok de forma masiva.

## 🚀 Características

- ✅ Descarga videos de TikTok en alta calidad
- ✅ Descarga múltiples videos desde un archivo de texto
- ✅ Guarda metadatos del video (vistas, likes, comentarios, etc.)
- ✅ Guarda miniaturas
- ✅ Genera resumen JSON con estadísticas
- ✅ Interfaz de línea de comandos fácil de usar

## 📋 Requisitos

- Python 3.7 o superior
- ffmpeg (opcional, pero recomendado para mejor procesamiento)

## 🔧 Instalación

1. **Clonar o descargar este repositorio**

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Instalar ffmpeg (opcional pero recomendado):**

En Ubuntu/Debian:
```bash
sudo apt install ffmpeg
```

En macOS:
```bash
brew install ffmpeg
```

En Windows:
Descarga desde https://ffmpeg.org/download.html

## 💻 Uso

### Descargar un solo video

```bash
python tiktok_downloader.py -u https://www.tiktok.com/@user/video/123456789
```

### Descargar múltiples videos desde un archivo

1. Crea un archivo de texto (ej: `mis_videos.txt`) con las URLs:
```
https://www.tiktok.com/@user/video/123456789
https://www.tiktok.com/@user/video/987654321
https://www.tiktok.com/@user/video/456789123
```

2. Ejecuta el descargador:
```bash
python tiktok_downloader.py -f mis_videos.txt
```

### Especificar directorio de salida

```bash
python tiktok_downloader.py -f mis_videos.txt -o videos_virales
```

### Descargar sin metadatos

```bash
python tiktok_downloader.py -u URL --no-metadata
```

## 📂 Estructura de archivos descargados

```
downloads/
├── 1234567890_video_title.mp4       # Video
├── 1234567890_video_title.jpg       # Miniatura
├── 1234567890_video_title.info.json # Metadatos
└── summary_20231207_120000.json     # Resumen de descarga
```

## 📊 Información guardada

El programa guarda la siguiente información de cada video:

- 🆔 ID del video
- 📝 Título
- 👤 Autor
- 👁️ Vistas
- ❤️ Likes
- 💬 Comentarios
- 🔄 Compartidos
- ⏱️ Duración
- 📅 Fecha de subida
- 📄 Descripción
- 🕒 Fecha de descarga

## 🎯 Casos de uso

### Para creadores de contenido:
- Guardar videos de referencia para inspiración
- Analizar tendencias virales
- Crear biblioteca de contenido de competidores

### Para marketers:
- Investigar tendencias del mercado
- Analizar contenido viral de marcas
- Crear informes de análisis competitivo

### Para investigadores:
- Recopilar datos para análisis de redes sociales
- Estudiar patrones de viralidad
- Archivar contenido para estudios longitudinales

## ⚙️ Opciones avanzadas

### Uso como módulo de Python

```python
from tiktok_downloader import TikTokDownloader

# Crear instancia
downloader = TikTokDownloader(output_dir="mis_videos")

# Descargar un video
info = downloader.download_video("https://www.tiktok.com/@user/video/123")

# Descargar desde archivo
results = downloader.download_from_file("urls.txt")
```

## 🐛 Solución de problemas

### Error: "Unable to download video"
- Verifica que la URL sea correcta y pública
- Algunos videos privados o restringidos no se pueden descargar
- Prueba actualizar yt-dlp: `pip install -U yt-dlp`

### Error: "ffmpeg not found"
- Instala ffmpeg siguiendo las instrucciones de instalación
- El programa funcionará sin ffmpeg pero con limitaciones

### Videos muy lentos
- Verifica tu conexión a internet
- TikTok puede limitar descargas masivas, espera entre descargas

## 📜 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## ⚠️ Advertencia legal

Este software es solo para uso educativo y personal. Respeta los derechos de autor y los términos de servicio de TikTok. No uses este software para:

- Redistribuir contenido sin permiso del creador
- Violar los términos de servicio de TikTok
- Descargar contenido con fines comerciales sin autorización

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un issue en el repositorio.

---

**Hecho con ❤️ para la comunidad de TikTok**
