
## python-dotenv: Gerenciamento de variáveis p/ segurança.
## - contextlib: Controle de ciclo de vida da aplicação.
## - FastAPI: Framework p/ construção da API.
## - CORSMiddleware: Comunicação segura entre Frontend e Backend.
## - Pydantic: Integridade e validação de dados de entrada.
from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

## 1. IMPORTAÇÃO DE SERVIÇS MODULARIZADOS: Chama as 
## funções como as de cálculo de ETA ou salvamento em banco.
from services.bus_service import get_bus_data
from services.alert_service import create_alert
from services.db import get_connection
from utils.geo_utils import calculate_distance, calculate_eta

# Domínios para teste
VALID_DOMAINS = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "icloud.com"]


## 2. GERENCIAMENTO DE CICLO DE VIDA(Lifespan): Garante a correta
## execução de ações de setup e encerramento de forma segura.

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando monitoramento...")

    yield

    print("Encerrando aplicação...")
    
app = FastAPI(lifespan=lifespan)

## 3. CONFIGURAÇÃO DE CORS: Permite a comunicação entre as portas
#  de Front e Back sem bloqueios. 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
## 4. SCHEMA DE DADOS: Pydantic para validar garantir que os dados
## enviados pelo usuário estejam corretos.
class Alert(BaseModel):
    email: EmailStr
    line: str
    lat: float
    lon: float
    start_time: str
    end_time: str


def validate_domain(email):
    email_str = str(email)
    domain = email_str.split("@")[-1].lower()
    return domain in VALID_DOMAINS

@app.get("/")
def root():
    return {"message": "Bus Tracker API"}

## 5. ENDPOINT DE STATUS: Polling de ônibus que alimenta o mapa
## em React com posições, distância e tempo estimado (ETA)

@app.get("/status/{line}")
def status(line: str, lat: float, lon: float):
    return get_bus_data(line,lat,lon)

@app.get("/line-status")
def line_status(line: str, lat: float, lng: float):
    result = get_bus_data(line, lat, lng)

    if not result["success"]:
        return []

    buses = result["data"]

    formatted = []

    for bus in buses:
        formatted.append({
            "order": bus["bus_id"],
            "lat": bus["lat"],
            "lng": bus["lon"],
            "speed": bus["speed"],              
            "distance_km": bus["distance_km"], 
            "eta_minutes": bus["eta_min"]
        })

    return formatted

## 6. GESTÃO DE ALERTAS: Separa a crição de alertas e a listagem, convertendo objt
## Pydantic em dicionário Python.

@app.post("/alert")
def create_alert_endpoint(alert: Alert):
    if not validate_domain(alert.email):
        raise HTTPException(status_code=400, detail= "Domínio de email inválido")

    return {
        "message": "Alerta criado com sucesso",
        "data": create_alert(alert.model_dump())
    }

@app.get("/alerts")
def list_alerts():
    from services.alert_service import get_alerts
    alerts = get_alerts()

    return {"total": len(alerts),
            "alerts": alerts
    }

## 7. REMOÇAO DE ALERTAS: Domínio do SQL e gerenciamento de conexões
## garantindo um banco de dados sem travas

@app.delete("/alert/{alert_id}")
def delete_alert(alert_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alerts WHERE id = ?", (alert_id,))
        conn.commit()
        return {"message": "Alerta removido"}
    finally:
        conn.close()