from dotenv import load_dotenv

## 1. CARREGAMENTO DO AMBIENTE: Garante credenciais e config de rede (Redis)
## disponíveis antes do agendador de tarefas.
load_dotenv()

## 2. IMPORT DA INSTÂNCIA CENTRALIDAZA: Importação do celery_app
## configurado para Worker (execut) e Beat (agendamento).
from backend.celery_instance import celery_app

## 3. SINCRONIA TEMPORAL (Timerzone), garantindo fuso horário
## do Rio de Janeiro (local) funcione independente de onde
## o servidor Docker esteja.
celery_app.conf.update(
    timezone="America/Sao_Paulo",
    enable_utc=True
)

## 4. DEF DO BEAT: Relógio com disparos de funcionamento,
## a cada 30 seg, das tasks.
celery_app.conf.beat_schedule = {
    "check-alerts-every-30-seconds":{
        "task": "tasks.alert_tasks.run_alert_check",
        "schedule": 30.0,
    },
}