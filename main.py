from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from db import insertar_gasto
from grafico import generar_grafico_resumen
from imgbb import subir_imagen_imgbb  # función que vamos a crear ahora
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    sender = request.form.get("From", "")
    message = request.form.get("Body", "").strip()
    celular = sender.replace("whatsapp:", "")
    resp = MessagingResponse()

    if message.lower() == "/resumen":
        path = generar_grafico_resumen(celular)
        if path:
            url_img = subir_imagen_imgbb(path)  # Sube la imagen y devuelve el link
            if url_img:
                client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
                client.messages.create(
                    body="📊 Acá está tu resumen de gastos:",
                    from_=os.getenv("TWILIO_NUMBER"),
                    to=sender,
                    media_url=[url_img]
                )
                os.remove(path)  # Borra el archivo local después de subirlo
            else:
                resp.message("❌ Ocurrió un error al subir el gráfico.")
        else:
            resp.message("❌ No hay datos registrados aún.")
        return str(resp)
    
    elif message.lower() == "/ayuda":
        resp.message(
            "🤖 *Ayuda del bot de gastos*\n\n"
            "Este bot te ayuda a registrar y visualizar tus gastos en supermercados.\n\n"
            "📌 *Para registrar un gasto:*\n"
            "Escribí el nombre del supermercado seguido del monto. Ejemplo:\n"
            "`Carrefour 1234.56`\n\n"
            "📊 *Para ver tu resumen del mes:*\n"
            "Escribí: `/resumen`\n\n"
            "ℹ️ *Comandos disponibles:*\n"
            "`/resumen` - Ver resumen del mes actual\n"
            "`/ayuda` - Mostrar esta ayuda"
        )
        return str(resp)
    
    elif es_saludo(message):
        resp.message(
            "👋 ¡Hola! Bienvenido al bot de control de gastos.\n\n"
            "📌 Podés registrar tus compras escribiendo:\n"
            "`NombreSupermercado 1234.56`\n\n"
            "📊 Para ver tu resumen mensual, escribí `/resumen`\n"
            "ℹ️ Para más info, escribí `/ayuda`"
        )
        return str(resp)


    # Si no es /resumen, se espera que sea supermercado + monto
    supermercado, monto = parsear_mensaje(message)
    if supermercado and monto:
        insertar_gasto(celular, supermercado, monto)
        resp.message(f"✅ Gasto registrado:\nSupermercado: {supermercado}\nMonto: ${monto}")
    else:
        resp.message("❌ Formato inválido. Enviá algo como:\n`Carrefour 12345.50`")

    return str(resp)

def parsear_mensaje(msg):
    partes = msg.split()
    if len(partes) >= 2:
        supermercado = " ".join(partes[:-1])
        try:
            monto = float(partes[-1])
            return supermercado, monto
        except ValueError:
            return None, None
    return None, None

def es_saludo(texto):
    saludos = ["hola", "buenas", "qué tal", "buen día", "holis", "saludos", "hello"]
    texto = texto.lower()
    return any(s in texto for s in saludos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

