# 🎯 Analizador de Competencia - TikTok

## ¿Qué hace este programa?

✅ **Analiza qué hace tu competencia** en fitness, crossfit, cafeterías, restaurantes, etc.
✅ **Identifica qué contenido funciona mejor** (más comentarios, shares, engagement)
✅ **Genera insights de marketing** para tu estrategia de contenido
✅ **Descarga los mejores videos** según diferentes métricas
✅ **Crea reportes detallados** con recomendaciones

---

## 🚀 Uso Básico

```bash
python3 competencia_analyzer.py SECTOR
```

---

## 📊 Ejemplos por Sector

### 💪 FITNESS
```bash
python3 competencia_analyzer.py fitness
```

### 🏋️ CROSSFIT
```bash
python3 competencia_analyzer.py crossfit 50
```

### ☕ CAFETERÍAS
```bash
python3 competencia_analyzer.py cafeteria
```

### 🍽️ RESTAURANTES
```bash
python3 competencia_analyzer.py restaurante 40
```

### 🏢 GIMNASIOS
```bash
python3 competencia_analyzer.py "gym motivation" 30 100000
```

### 🏭 INDUSTRIA
```bash
python3 competencia_analyzer.py industria
```

---

## 📈 Qué Analiza

### 1. **Promedios del Sector**
- Vistas promedio
- Likes promedio
- Comentarios promedio
- Shares promedio
- **Engagement rate** (métrica clave)

### 2. **Top Videos por Métrica**
- 🏆 **Mejor engagement** (contenido más efectivo)
- 💬 **Más comentados** (generan conversación)
- 🔄 **Más compartidos** (mayor viralidad)
- 💾 **Más guardados** (contenido valioso)
- 👁️ **Más vistos** (mayor alcance)

### 3. **Insights y Recomendaciones**
- Duración óptima de videos
- Palabras clave efectivas
- Engagement rate objetivo
- Tipo de contenido que funciona

---

## 💡 Qué Descubrirás

### Para FITNESS/CROSSFIT:
- ✓ Qué tipo de ejercicios son más virales
- ✓ Videos de transformación vs tutoriales
- ✓ Duración ideal (15s, 30s, 60s)
- ✓ Qué genera más comentarios

### Para CAFETERÍAS/RESTAURANTES:
- ✓ Recetas vs ambientes
- ✓ Presentación de platos virales
- ✓ Behind the scenes vs producto final
- ✓ Qué hace que la gente comparta

### Para GIMNASIOS:
- ✓ Tours del gym vs entrenamientos
- ✓ Testimonios vs resultados
- ✓ Motivación vs educación
- ✓ Contenido que genera engagement

---

## 📊 Ejemplo de Reporte

```
REPORTE DE ANÁLISIS - FITNESS
================================================================================

PROMEDIOS DEL SECTOR
--------------------------------------------------------------------------------
  👁️  Vistas promedio:      250,000
  ❤️  Likes promedio:       15,000
  💬 Comentarios promedio:  450
  🔄 Shares promedio:       1,200
  📊 Engagement rate:       6.7%

TOP 5 VIDEOS CON MEJOR ENGAGEMENT
--------------------------------------------------------------------------------
1. Transformación 90 días - Resultados increíbles
   👤 @fitnesscoach
   📊 Engagement: 12.5% | 👁️  500K | ❤️  50K | 💬 2.1K | 🔄 5K

2. Rutina completa en casa - 15 minutos
   👤 @homeworkout
   📊 Engagement: 11.2% | 👁️  350K | ❤️  35K | 💬 1.8K | 🔄 3.5K

RECOMENDACIONES PARA TU CONTENIDO
--------------------------------------------------------------------------------
1. DURACIÓN ÓPTIMA
   ✓ Los videos exitosos duran aproximadamente 35 segundos
   📊 35 segundos en promedio

2. PALABRAS CLAVE EFECTIVAS
   ✓ Estas palabras aparecen frecuentemente en videos virales
   📝 transformacion, rutina, resultados, casa, rapido

3. ENGAGEMENT RATE OBJETIVO
   ✓ Los videos más exitosos tienen este nivel de engagement
   📊 8.5%+
```

---

## 🎯 Opciones de Descarga

Después del análisis, puedes descargar:

1. **Top por ENGAGEMENT** → Contenido más efectivo
2. **Top por COMENTARIOS** → Contenido que genera conversación
3. **Top por SHARES** → Contenido más viral
4. **Top por VISTAS** → Contenido más visto

---

## 📁 Archivos Generados

```
analisis_competencia/
├── analisis_fitness_1234567890.json    # Datos completos
├── reporte_fitness_1234567890.txt      # Reporte legible
└── [videos descargados].mp4            # Top videos
```

---

## 💼 Casos de Uso

### 🏋️ Dueño de Gimnasio
```bash
python3 competencia_analyzer.py "gym promotion" 50
```
**Descubrirás:** Qué tipo de promociones funcionan, qué horarios publicar, qué formato usar

### ☕ Cafetería
```bash
python3 competencia_analyzer.py "coffee shop" 40
```
**Descubrirás:** Recetas virales, presentaciones que funcionan, tendencias de café

### 🍽️ Restaurante
```bash
python3 competencia_analyzer.py "restaurant food" 30
```
**Descubrirás:** Platos más compartidos, presentaciones virales, tipo de contenido

### 💪 Coach Personal
```bash
python3 competencia_analyzer.py "personal trainer" 50
```
**Descubrirás:** Qué servicios mostrar, testimonios vs resultados, formato ideal

---

## 🔍 Tips para Mejores Resultados

1. **Usa términos en inglés** (mayor cantidad de resultados)
   ```bash
   python3 competencia_analyzer.py "fitness transformation"
   ```

2. **Combina palabras clave**
   ```bash
   python3 competencia_analyzer.py "crossfit workout"
   ```

3. **Analiza nichos específicos**
   ```bash
   python3 competencia_analyzer.py "vegan restaurant"
   ```

4. **Ajusta el mínimo de vistas** según tu objetivo
   ```bash
   python3 competencia_analyzer.py fitness 50 500000
   ```

---

## 📊 Métricas Clave

### Engagement Rate
- **< 3%**: Bajo engagement
- **3-7%**: Promedio
- **7-10%**: Bueno
- **> 10%**: Excelente

### Comentarios
- Indica qué contenido genera conversación
- Ideal para contenido controversial o educativo

### Shares
- Indica viralidad real
- El contenido que la gente quiere mostrar a otros

### Saves
- Contenido valioso que guardan para después
- Ideal para tutoriales, recetas, tips

---

## 🎯 Próximos Pasos

1. **Analiza tu sector**
2. **Revisa los insights**
3. **Descarga los mejores videos**
4. **Estudia qué funciona**
5. **Aplica a tu contenido**

---

**¡Ahora sabes exactamente qué crear para tu negocio!** 🚀
