from services.db import get_connection
from datetime import datetime
import pytz
import os

## 1. SINCRONIZAÇÃO DE TEMPO E PERSISTÊNCIA: Garante que os
## registros de último alerta no banco estejam no fuso local, 
## controlados por cooldown.
TIMEZONE = os.getenv("TIMEZONE", "UTC")
tz = pytz.timezone(TIMEZONE)

print("ALERT_SERVICE CARREGANDO DE:", __file__)

## 2. CRIAÇÃO DE REGISTROS: Transforma dados da API para dentro do banco,
## através do uso do 'INSERT INTO'.
def create_alert(alert_data):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (
                email, line, lat, lon, start_time, end_time,
                last_bus_id, last_alert_time, notified
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,(
            alert_data["email"],
            alert_data["line"],
            alert_data["lat"],
            alert_data["lon"],
            alert_data["start_time"],
            alert_data["end_time"],
            None,
            None,
            0
        ))

        conn.commit()
        return alert_data
    finally:
        conn.close()
## 3. RECUPERAÇÃO: Alimenta o worker, convertendo as linha 
## do SQLite em dicionários Python. 
def get_alerts():
    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, email, line, lat, lon, start_time, end_time, last_bus_id, last_alert_time, notified
            FROM alerts
        """)

        rows = cursor.fetchall()
        
        # Resultado do SQL para chaves nomeadas
        alerts = [
            {
                "id": row[0],
                "email": row[1],
                "line": row[2],
                "lat": row[3],
                "lon": row[4],
                "start_time": row[5],
                "end_time": row[6],
                "last_bus_id": row[7],
                "last_alert_time": row[8],
                "notified": row[9]
            }
            for row in rows
        ]
        
        return alerts
    finally:
        conn.close()

## 4. ATUALIZAÇÃO DE ESTADO: Fundamental para evitar spam, salva
## o último ônibus notificado e a hora exata do envio.
def update_last_bus_id(alert_id, bus_id):

    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE alerts
            SET last_bus_id = ?, last_alert_time = ?
            WHERE id = ?
        """,   (
                bus_id,
                datetime.now(tz).replace(microsecond=0).isoformat(),
                alert_id,
        ))

        conn.commit()
    finally:
        conn.close() 