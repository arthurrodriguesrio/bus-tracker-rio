import smtplib
import os
from email.mime.text import MIMEText

## 1. INTEGRAÇÃO C/ SERVIDOR DE E-MAIL (SMTP): Função isola
## complexidades de conexão, transforma strings em objetos MIME, padrão
## universal para mensagens de e-mail.
def send_email(to_email, subject, message):
    # Credenciais contidas no arquivo .env
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASS")

    print("DEBUG ENV EMAIL:", sender_email)
    print("DEBUG EMAIL CONFIG OK")

    # Criação do corpo do e-mail, garantindo conformidade na
    # recepção do servidor destinatário.
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    print("DEBUG EMAIL:", to_email, subject, message)
    ## 2. PROTOCOLO DE CONEXÃO: Tratamento das falhas de rede
    ## com try/except, com 'starttls()' garantindo a segurança
    ## na interação.
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print(f"EMAIL enviado para {to_email}")
        return True

    except Exception as e:
        # Log de Erro p/ identificar possíveis problemas de envio.
        print(f"ERRO ao enviar email:{e}")
        return False

