from celery_instance import celery_app
from services.email_service import send_email

## 1. DEFINIÇÃO DA TASK DE NOTIFICAÇÃO (Email Worker): Garante que o Worker de localização
## trabalhe independente da resposta do servidor de email (SMTP).
@celery_app.task(name="tasks.email_tasks.send_email_task")
def send_email_task(to_email, subject, message):
    ## Executa serviço de email, independente de falha em servidor.
    send_email(to_email, subject, message)