import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

DB_PATH = os.getenv("DB_PATH") or "gastos.db"

def generar_grafico_resumen(numero_usuario):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    ahora = datetime.now()
    mes_actual = f"{ahora.month:02d}"
    anio_actual = str(ahora.year)

    cursor.execute("""
        SELECT supermercado, COUNT(*) AS cantidad_visitas, SUM(monto) AS total_gastado
        FROM gastos
        WHERE celular = ?
          AND strftime('%m', fecha) = ?
          AND strftime('%Y', fecha) = ?
        GROUP BY supermercado
    """, (numero_usuario, mes_actual, anio_actual))
    
    datos = cursor.fetchall()
    conn.close()

    if not datos:
        print("No hay datos para generar gráfico.")
        return None

    supermercados = [fila[0] for fila in datos]
    visitas = [fila[1] for fila in datos]
    totales = [fila[2] for fila in datos]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(supermercados, totales, color='skyblue')
    
    ax.set_title(f"Gastos de {ahora.strftime('%B %Y')} por supermercado")
    ax.set_xlabel("Supermercado")
    ax.set_ylabel("Total gastado ($)")
    ax.grid(axis='y')

    for i, bar in enumerate(bars):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                f"${totales[i]:.0f}\n({visitas[i]} visitas)",
                ha='center', va='bottom', fontsize=9)

    archivo_salida = f"resumen_{numero_usuario}.png"
    plt.tight_layout()
    plt.savefig(archivo_salida)
    plt.close()

    return archivo_salida
