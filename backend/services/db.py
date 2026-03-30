import sqlite3

## 1. GERENCIAMENTO DE PERSISTÊNCIA (SQLite): Garante que funcionamento
## do sistema, mesmo em contextos de quantidades grandes de tarefas
## simultâneas.
def get_connection():
    # Estabelece conexão com 'alerts.bd', criando arquivo, caso não exista.
    conn = sqlite3.connect("alerts.db", check_same_thread=False)

    cursor = conn.cursor()
    ## 2. CRIAÇÃO DE TABELA: Garante o banco de dados, com parâmetros,
    ## de forma auto-sustentável.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            line TEXT,
            lat REAL,
            lon REAL,
            start_time TEXT,
            end_time TEXT,
            last_bus_id TEXT,
            last_alert_time TEXT,
            notified INTEGER
        )
    """)
    
    conn.commit()

    return conn