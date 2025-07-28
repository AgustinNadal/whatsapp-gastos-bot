# 🧾 WhatsApp Gastos Bot

Este proyecto es un bot de WhatsApp desarrollado en Python que permite registrar y visualizar los gastos mensuales en supermercados a través de mensajes simples. Está pensado para funcionar de manera automatizada, accesible desde cualquier celular, sin necesidad de descargar aplicaciones adicionales.

## 🚀 Funcionalidades principales

- ✅ Registro de gastos enviando:  
  `NombreSupermercado Monto`  
  Ejemplo: `Carrefour 2532.50`

- 📊 Generación de gráficos mensuales con resumen por supermercado:
  - Muestra cantidad de visitas por lugar
  - Suma total de gasto por cada uno

- 🔁 Comando `/resumen`: genera el gráfico del mes actual
- ℹ️ Comando `/ayuda`: explica el funcionamiento del bot
- 👋 Mensaje de bienvenida automático al primer contacto

## 🧠 Tecnologías utilizadas

- **Python** con **Flask** para el servidor web
- **Twilio** para integración con WhatsApp
- **SQLite** como base de datos embebida
- **Matplotlib** para gráficos
- **ImgBB API** para alojar las imágenes generadas
- **Render** como plataforma de despliegue gratuita

## ⚙️ Configuración y despliegue

1. Cloná el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/whatsapp_gastos_bot.git
   ```

2. Instalá las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Creá un archivo `.env` con tus credenciales:
   ```env
   TWILIO_ACCOUNT_SID=...
   TWILIO_AUTH_TOKEN=...
   TWILIO_NUMBER=whatsapp:+14155238886
   IMGBB_API_KEY=...
   DB_PATH=gastos.db
   ```

4. Iniciá el servidor local:
   ```bash
   python main.py
   ```

5. O bien desplegalo en [Render](https://render.com) usando `gunicorn`.

## 📦 Estructura del proyecto

```
whatsapp_gastos_bot/
├── main.py                  # Servidor Flask y lógica principal
├── db.py                    # Funciones para manejo de SQLite
├── grafico.py               # Generación de gráficos con matplotlib
├── imgbb.py                 # Subida de imágenes a ImgBB
├── .env                     # Variables de entorno (no se sube)
├── requirements.txt         # Dependencias
├── Procfile                 # Instrucciones para Render
└── .gitignore               # Exclusión de archivos sensibles
```

## 🛡️ Licencia

Este proyecto se distribuye bajo licencia MIT.