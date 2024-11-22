import time
import requests
import socket
from config import BOT_TOKEN, CHAT_ID

# URL da API do Telegram
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def is_connected():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Usando o DNS público do Google
            local_ip = s.getsockname()[0]  # Obtém o IP local usado na conexão
        return local_ip
    except Exception as e:
        print(f"Erro ao obter o IP local: {e}")
        return "IP local desconhecido"

def get_external_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        external_ip = response.json().get("ip", "IP externo desconhecido")
        return external_ip
    except Exception as e:
        print(f"Erro ao obter o IP externo: {e}")
        return "IP externo desconhecido"

def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(TELEGRAM_URL, json=payload)
        if response.status_code == 200:
            print("Mensagem enviada com sucesso!")
        else:
            print(f"Falha ao enviar mensagem: {response.text}")
    except Exception as e:
        print(f"Erro ao conectar ao Telegram: {e}")

if __name__ == "__main__":
    print("Aguardando conexão com a internet...")
    wait_time = 5  # Tempo inicial de espera em segundos

    while not is_connected():
        print(f"Sem conexão. Tentando novamente em {wait_time} segundos...")
        time.sleep(wait_time)
        wait_time = min(wait_time * 2, 60)  # Aumenta o intervalo até no máximo 60 segundos

    print("Conexão detectada! Obtendo IPs...")
    local_ip = get_local_ip()
    #external_ip = get_external_ip()

    print("Enviando IPs para o Telegram...")
    message = (
        f"Raspberry Pi conectado\n\n"
        f"IP Local: {local_ip}\n"
        #f"IP Externo: {external_ip}"
    )
    send_message(CHAT_ID, message)
