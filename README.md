# 📈 LACC Growth Dashboard

**Latin America Cybersecurity Challenge (LACC) – Business Intelligence & Forecasting**

![LACC Banner](docs/banner-lacc.png)

> Un tablero interactivo en **Streamlit** que cuantifica –y predice– el impacto de la comunidad LACC
> en redes sociales. Incluye analíticas de crecimiento histórico, embudo de conversión y proyecciones
> automáticas con **Prophet**.

---

## 🚀  Características

| Módulo | Descripción |
|--------|-------------|
| **Métricas clave** | Seguidores totales, CAGR, incremento absoluto, red dominante y progreso hacia la meta. |
| **Visuales BI** | Línea histórica por red, área acumulada, heatmap de nuevos seguidores, pie de distribución. |
| **Embudo de conversión** | Awareness → Newsletter → Participantes CTF → Leads corporativos. |
| **Forecast automático** | Deslizador 3-24 meses con Prophet; muestra la proyección y valor estimado final. |
| **UX Premium** | Dark-mode, tarjetas con sombra, logo personalizable, menú oculto, responsive 100 %. |

---

## 🖥️  Demo

![Demo GIF](docs/demo.gif)

Prueba la versión en producción: **<https://lacc-growth-dashboard.streamlit.app>**

---

## 📂  Estructura del repositorio

.
├─ lacc_growth_dashboard.py # Script principal de Streamlit
├─ requirements.txt # Dependencias exactas
├─ logo_lacc.png # Logo utilizado en el header
└─ docs/
├─ banner-lacc.png # Imagen hero para el README
└─ demo.gif # Grabación del dashboard en acción

yaml
Copiar
Editar

---

## ⚙️  Instalación local

```bash
# 1. Clona el repositorio
git clone https://github.com/<tu-usuario>/lacc-growth-dashboard.git
cd lacc-growth-dashboard

# 2. Crea un entorno virtual (opcional pero recomendado)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Ejecuta la app
streamlit run lacc_growth_dashboard.py
La aplicación se abrirá en tu navegador por defecto en http://localhost:8501.

☁️ Despliegue en Streamlit Cloud
Sube todos los archivos a un repositorio público o privado de GitHub.

Ve a https://share.streamlit.io, elige “New app” y conecta tu repo.

Selecciona lacc_growth_dashboard.py como Main file.

Haz clic en Deploy. ¡Listo! Obtendrás una URL pública para compartir.

🔮 Cómo funciona el forecast
Paso	Acción
1	Se construye la serie temporal con el total de seguidores por mes.
2	Prophet se entrena sin estacionalidad diaria/semanal.
3	El usuario elige el horizonte (3-24 meses) mediante un deslizador.
4	Se genera la tabla forecast con yhat (valor esperado) y se grafica.
5	Se muestra la métrica con el valor proyectado en la última fecha.

🤝 Contribuciones
¡Pull Requests y Issues son bienvenidos!
Antes de abrir un PR, crea un branch descriptivo y asegúrate de:

Pasar flake8 / black.

Mantener compatibilidad con Python ≥ 3.10.

Añadir/actualizar pruebas si fuera necesario.

📜 Licencia
Distribuido bajo licencia MIT. Consulta el archivo LICENSE para más detalles.
