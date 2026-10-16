# 📰 Newsletter Testing Automator

**Versión:** 1.0.0

Automatizador de pruebas y simulación de aperturas (opens) y clics para campañas de newsletters utilizando Playwright y Streamlit.

---

## 🚀 Características (v1.0.0)

- **Simulación Multiplataforma**: Emulación de aperturas tanto en entorno de escritorio (Desktop / Chromium) como en dispositivos móviles (iPhone / Safari).
- **Interfaz Web Interactiva**: Panel de control con Streamlit para la creación y gestión de campañas de testing.
- **Base de Datos Local**: Persistencia de campañas e historial de ejecuciones mediante SQLite.
- **Programador de Tareas (Scheduler)**: Estructura base para ejecuciones periódicas automáticas de campañas.
- **Pruebas Rápidas Independientes**: Script `test_single.py` para validar enlaces específicos con métricas detalladas en consola.

---

## 🛠️ Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd newsletter-tester
   ```

2. **Crear y activar el entorno virtual**:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar navegadores de Playwright**:
   ```bash
   playwright install chromium
   ```

---

## 💻 Uso

### Panel de Control (Streamlit)
Para lanzar la interfaz gráfica:
```bash
streamlit run app.py
```

### Script de Prueba Individual
Para probar un enlace puntual sin levantar el servidor:
1. Abre `test_single.py`.
2. Actualiza la variable `email_link` con el enlace deseado.
3. Ejecuta:
   ```bash
   python test_single.py
   ```

---

## 📁 Estructura del Proyecto

```text
newsletter-tester/
├── app.py              # Interfaz web con Streamlit
├── automator.py        # Lógica de automatización con Playwright
├── database.py         # Conexión y esquema SQLite
├── scheduler.py        # Planificador de tareas recurrentes
├── test_single.py      # Script de prueba rápida individual
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación del proyecto
```

---

## 📄 Licencia

MIT License.
