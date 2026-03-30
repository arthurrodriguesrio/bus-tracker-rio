from celery_instance import celery_app
from workers.alert_checker import check_alerts_logic

## 1. Função para testes/erro de função
def check_alerts_logic():
    print("Iniciando GPS dos ônibus...")
    pass


## 2. DEFINIÇÃO DE TAREFA AGENDADA: Garante que o Celery Beat
## localize a função (@celery_app.task) no Docker.
@celery_app.task(name="tasks.alert_tasks.run_alert_check")
def run_alert_check():
    try:
        print("Executando verificação de alertas...")
        check_alerts_logic()
    # Execução lógica através do processamento do bando de dados
    # e da API do Rio.
    except Exception as e:
        ## 3. TRATAMENTO DE ERROS: Uso do 'traceback' para identificar erros,
        ## facilitando manutenção, e evitando erros 
        ## que podem travar o Worker.
        print("ERRO NA TASK", e)
        import traceback
        traceback.print_exc()