from celery_instance import celery_app
from services.alert_service import get_alerts, update_last_bus_id
from services.bus_service import get_bus_data
from tasks.email_tasks import send_email_task
from datetime import datetime, timedelta
import pytz
import os

## 1. SINCRONIA DE TEMPO: Garante funcionamento dos alertas com
## assimetria entre horário do servidor e do usuário.
TIMEZONE = os.getenv("TIMEZONE", "America/Sao_Paulo")
tz = pytz.timezone(TIMEZONE)

def is_within_time_window(start, end):
    # Verifica horários atual/janela do usuário
    now = datetime.now(tz).time()
    try:
        start_t = datetime.strptime(start, "%H:%M").time()
        end_t = datetime.strptime(end, "%H:%M").time()
        return start_t <= now <= end_t
    except:
        return False
    
def check_alerts_logic():
    ## 2. Busca dados de alertas ativos no SQLite 
    ## para processar em lote.
    print(f"DEBUG: {datetime.now(tz)} Verificando alertas...")

    alerts = get_alerts()

    if not alerts:
        print("DEBUG: Nenhum alerta no banco. Cancelando busca.")
        return
    
    print(f"DEBUG ALERTS: {len(alerts)}")

    for alert in alerts:
        ## 3. LÓGICA DE COOLDOWN: Limita o recebimento de e-mails
        ## pelo usuário sobre o mesmo ônibus, ignorando alertas
        ## enviados há menos de 5 min.
        print("DEBUG LAST TIME:", alert.get("last_alert_time"))
        
        start_time = alert.get("start_time")
        end_time = alert.get("end_time")

        if not is_within_time_window(start_time, end_time):
            print("DEBUG: Fora da janela de horário")
            continue
        
        last_time = alert.get("last_alert_time")
        if last_time:
            try:
                last_time_dt = datetime.fromisoformat(last_time)
                if last_time_dt.tzinfo is None:
                    last_time_dt = tz.localize(last_time_dt)
                if datetime.now(tz) - last_time_dt < timedelta(minutes=5):
                    print("DEBUG: Cooldown ativo, pulando alerta")
                    continue
            except Exception as e:
                print("DEBUG: erro ao analisar last_alert_time:", e)

               
        line = alert["line"]
        
        ## 4. INTEGRAÇÃO DE DADOS EM TEMPO REAL: Consulta posições
        ## de frota filtrada (linha/alertas)
        result = get_bus_data(line, alert["lat"], alert["lon"])
        print(f"DEBUG ALERTA - linha: {line}")
        print(f"DEBUG ALERTA - retorno buses: {result}")

        # Garantia de retorno em lista
        if not result["success"]:
            print(f"DEBUG ERRO API: {result['error']}")
            continue
        buses = result.get("data",[])
        print(f"DEBUG ALERTA - buses filtrados: {buses}")

        if not buses:
            continue

        ## 5. SELEÇÃO DE MELHOR ÔNIBUS: Uso da função lambda para
        ## encontrar ônibus com menor tempo de chegada.
        best_bus = min(buses, key=lambda x: x.get("eta_min", 999))
        
        eta = best_bus.get("eta_min")
        bus_id = best_bus.get("bus_id")

        print(f"BUS DETECTADO - ETA: {eta} | ID: {bus_id}")

        ## 6. DISPARO ASSÍNCRONO DE NOTIFICAÇÕES: Cria as condições
        ## para envio de alerta (ETA <= 10 e Bus_ID != do ultimo notificado),
        ## além do '.delay()' mandando o envio para outro worker, liberando
        ## a próxima verificação.
        if (
            eta is not None
            and eta <= 10 
            and bus_id is not None
            and bus_id != alert.get("last_bus_id")
        ):
            message = f"Ônibus da linha {line} chega em {eta} minutos."
            print("DEBUG: ENVIANDO EMAIL...")

            send_email_task.delay(
                alert["email"],
                "Alerta de Ônibus - Rio",
                message
            )

            ## Evita duplicidade no cíclo de 30s.
            update_last_bus_id(alert["id"], bus_id)

## 7. DEFINIÇÃO DA TASK CELERY: Função no Celery Beat, com 
## try/except e 'traceback' no monitoramento de falhas no
## agendamento no Docker.
@celery_app.task(name="tasks.alert_tasks.run_alert_check")
def run_alert_check():
    """Esta é a função que o Celery Beat vai chamar no Docker"""
    try:
        print("Executando tarefa agendada de verificação...")
        check_alerts_logic()
    except Exception as e:
        print("ERRO CRÍTICO NA TASK:", e)
        import traceback
        traceback.print_exc()