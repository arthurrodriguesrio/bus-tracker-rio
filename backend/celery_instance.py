
from celery import Celery
from dotenv import load_dotenv
import os

## 1. CARREGAMENTO DE AMBIENTE: URL do Redis+Timerzone 
## do Docker Compose/.env com valor padronizado garantindo
## funcionamento mesmo s/ variável. 
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL","redis://redis:6379/0")

## 2. INSTALAÇÃO DO CELERY: broker com a fila de tarefas; 
## backend com armazenamento das tarefas; aém do Include
## registrando as tarefas para o Worker executar.

celery_app = Celery(
    "bus-tracker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks.alert_tasks",
             "tasks.email_tasks"]
)

## 3. CONFIG TÉCNICAS: Padronizando o Worker, garantindo
## monitoramento e de tarefas e trafego de dados entre
## os containers.

celery_app.conf.update(
    # Corrigido: America/Sao_Paulo (com _) e adicionada a vírgula no final
    timezone=os.getenv("TIMEZONE", "America/Sao_Paulo"), 
    enable_utc=True, # Adicionada a vírgula que faltava aqui
    task_track_started=True, # Corrigido de 'starded' para 'started'
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json'
)

## 4. AGENDAMENTO AUTOMÁTICO: Configuração do Beat para
## disparar a cada 30 segundos, garantindo monitoramento
## em tempo real.
celery_app.conf.beat_schedule = {
    "check-alerts-every-30-seconds": {
        "task": "tasks.alert_tasks.run_alert_check",
        "schedule": 30.0,
    },
}
